from rich.console import Console
from rich.progress import Spinner
from enum import Enum, auto
import time
import re

# TODO proper service names and definition
from services.service_a import ServiceA

# TODO - format and make nice
help = '''
Flow modifiers (keeps the mode saved after first prompt)
/n /normal <write your prompt> normal mode
/d /dig <write your prompt> dig mode. Default: b/7. See sub modifiers below
b/5 <prompt or list index> breakdown concept in 5 bullet points (number is optional, default 7)
p/5 <prompt or list index> plan for concept in 5 bullet points (number is optional, default 7)
e/ <prompt or list index> explain the concept in detail with examples
ap/2/100 <prompt or list index> auto-mode plan with 2 level depth - 100 points (so if 1 level breakdown in 100, if 2 levels break down in 10 and each sublevel in another 10, if 3 levels …:
Uses plan mode first
Uses plan mode on each subtopic
Uses breakdown on each sub-subtopic
ae/2/20 <prompt or list index> auto-mode explain with 2 level depth - 20 points
Uses breakdown first
Uses breakdown on each subtopic
Uses explain on each sub-subtopic
/b /brainstorm <write your prompt> brainstorm mode
/s /summarize <path to file / website url> summarize mode
/s+ /summarize+ <website url> summarize mode using sitemap to scrape
/t /terminal <prompt> writes answer in terminal as if user would write it
/q /question <path to file / website url> loads data for Q/A
/q+ /question+ <path to file / website url> loads data for Q/A
/r /reset start new session in current terminal
/cost returns the total cost from API
Mode modifiers (can be used in combination /ng+, /ng- or independent)
d+ distillation <write your prompt [optional]> enable distillation use
d- distillation- <write your prompt [optional]> disable distillation use
g+ google+ <write your prompt [optional]> enable google use
g- google- <write your prompt [optional]> disable google use
c+ creative+ <write your prompt [optional]> enable creative level inference
c- creative- <write your prompt [optional]> disable creative level inference
c<n> creative <n> <write your prompt [optional]> set creative level
x+ <write your prompt [optional]> code mode enabled
x- <write your prompt [optional]> code mode disabled
v+ <write your prompt [optional]> enable verbose
v- <write your prompt [optional]> disable verbose
'''


# CLI class to handle command parsing, state management, and terminal interaction
class CLI:
    class Mode(Enum):
        NORMAL = auto()
        DIG = auto()
        BRAINSTORM = auto()
        SUMMARIZE = auto()
        SUMMARIZE_PLUS = auto()
        TERMINAL = auto()
        QUESTION = auto()
        QUESTION_PLUS = auto()
        RESET = auto()
        COST = auto()
        HELP = auto()

    # color scheme
    class CLIStyle(Enum):
        DEFAULT = "#ffffff"
        REPLY = "#f0ed48"
        USER = "#3ce671"

    def __init__(self):
        self.state = None
        self.console = Console()
        self.reset()

        # wire up services
        self.service_a = ServiceA()

        self.command_patterns = {
            CLI.Mode.NORMAL: r'/(n|normal)\s*(.*)',
            CLI.Mode.DIG: r'/(d|dig)\s*(.*)',
            CLI.Mode.BRAINSTORM: r'/(b|brainstorm)\s*(.*)',
            CLI.Mode.SUMMARIZE_PLUS: r'/(s\+|summarize\+)\s*(.*)',
            CLI.Mode.SUMMARIZE: r'/(s|summarize)\s*(.*)',
            CLI.Mode.QUESTION_PLUS: r'/(q\+|question\+)\s*(.*)',
            CLI.Mode.QUESTION: r'/(q|question)\s*(.*)',
            CLI.Mode.TERMINAL: r'/(t|terminal)\s*(.*)',
            CLI.Mode.RESET: r'/(r|reset)\s*(.*)',
            CLI.Mode.COST: r'/(c|cost)\s*(.*)',
            CLI.Mode.HELP: r'/(h|help)\s*(.*)',
        }
        self.modifier_patterns = [
            (r'(d\+)', 'distillation', True),
            (r'(d\-)', 'distillation', False),
            (r'(g\+)', 'google', True),
            (r'(g\-)', 'google', False),
            (r'(c\+)', 'creative_level', -1),  # means auto mode - manual values are 1-5
            (r'(c\-)', 'creative_level', 0),  # disabled
            (r'(c(\d+))', None, None),  # handled separately due to the dynamic value
            (r'(x\+)', 'code_mode', True),
            (r'(x\-)', 'code_mode', False),
            (r'(v\+)', 'verbose', True),
            (r'(v\-)', 'verbose', False),
        ]

        # this is for display purposes only
        self.modifiers_map = {
            "distillation": "d",
            "google": "g",
            "creative_level": "c",
            "code_mode": "x",
            "verbose": "v",
        }
        self.spinner = Spinner('dots', text='Thinking...')
        self.user_input = ""

    # reset console, set default state
    def reset(self):
        self.state = {
            "mode": CLI.Mode.NORMAL,
            "modifiers": {
                "distillation": True,
                "google": False,
                "creative_level": 0,
                "code_mode": False,
                "verbose": False,
            },
            "cost": 0.0,
        }
        self.console.clear()
        self.console.style = self.CLIStyle.DEFAULT.value

    # print messages to the user in style :)
    def print_with_delay(self, text, delay=0.01):
        self.console.show_cursor(False)
        self.console.style = self.CLIStyle.REPLY.value
        self.console.print(end="\n")
        self.console.print("AI   > ", end="")
        for char in text:
            self.console.print(char, end="")
            time.sleep(delay)

        self.console.print()
        self.console.print()
        self.console.style = self.CLIStyle.DEFAULT.value
        self.console.show_cursor(True)

    # here is where the magic happens
    def process_command(self, command):
        # we need this in case we have state change to parse user message without the first part
        state_change = False
        first_part = command.split(" ")[0]

        # check if we change mode
        if first_part.startswith("/"):
            # Iterate over the command_patterns dictionary
            for mode, pattern in self.command_patterns.items():
                match = re.match(pattern, command)
                if match:
                    state_change = True
                    if mode == CLI.Mode.RESET:
                        self.reset()
                        return None
                    elif mode == CLI.Mode.COST:
                        return None
                    elif mode == CLI.Mode.HELP:
                        self.console.print(help)
                        return None
                    else:
                        self.state["mode"] = mode
                        break

        # check if we change modifiers
        if "|" in first_part:
            # Iterate over the modifier_patterns array
            for pattern, modifier_key, value in self.modifier_patterns:
                match = re.search(pattern, command)
                if match:
                    state_change = True
                    if modifier_key is not None:
                        self.state["modifiers"][modifier_key] = value
                    else:
                        # Handle c<n> modifier separately
                        creative_level = int(match.groups()[1])
                        self.state["modifiers"]["creative_level"] = creative_level

        # capture stuff after <space>
        if state_change:
            args = re.search(r'(?<=\s)\S+', command)
            if args is None:
                return
            args = args[0]
        else:
            args = command

        # print again user prompt
        self.console.print("\nUSER > ", end="")
        self.console.print(args, end="\n")

        # show spinner and call services # TODO add business logic and integrate
        with self.console.status(self.spinner):
            # Perform actions based on the current mode
            if self.state["mode"] == CLI.Mode.NORMAL:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.DIG:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.BRAINSTORM:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.SUMMARIZE:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.SUMMARIZE_PLUS:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.QUESTION:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.QUESTION_PLUS:
                result = self.service_a.perform_operation(args)
            elif self.state["mode"] == CLI.Mode.TERMINAL:
                result = self.service_a.perform_operation(args)

        return result

    # tricky part to paste multi-line or write multi-line in terminal
    # default on enter it submits
    # if first character is " " [space] it enters multi-line mode and requires double enter to submit
    def get_multiline_input(self):
        lines = []
        line_time = int(time.time() * 1000)
        multi_mode = False
        while True:
            try:
                line = input()
                lines.append(line)

                if line.startswith(" "):  # checks if we want multi-line mode or not
                    multi_mode = True

                if not multi_mode:
                    break

                if 10 < int(time.time() * 1000) - line_time < 400:
                    break
                else:
                    line_time = int(time.time() * 1000)
            except KeyboardInterrupt:
                return None

        return "\n".join(lines)

    def print_prompt(self):
        self.console.style = self.CLIStyle.DEFAULT.value
        self.console.print(f"{self.state['cost']:.2f}$ [yellow]{self.state['mode'].name.lower()}[/yellow] | ", end="")
        for modifier, value in self.state["modifiers"].items():
            if modifier == "creative_level" and value > 0:
                self.console.print(f"{self.modifiers_map[modifier]}{value}", style="cyan", end="")
            elif value:
                self.console.print(self.modifiers_map[modifier], style="cyan", end="")
        self.console.print(" > ", end="")
        self.console.style = self.CLIStyle.USER.value

    def main_loop(self):
        while True:
            # show initial updated prompt
            self.print_prompt()

            # get the command from the user
            command = ""
            while command == "":
                command = self.get_multiline_input()
                if command is None:
                    self.console.print("  Bye!")
                    return

                command = command.strip()

            # parse, update state, call services, get result
            result = self.process_command(command)

            if result is None:
                continue

            # if we have some smart stuff coming back print it really fast
            self.print_with_delay(result, 0.0005)


# Main function to run the CLI
def main():
    cli = CLI()
    cli.main_loop()


if __name__ == "__main__":
    main()
