import time
import random
import string


# call services from UI - in the future we can call them from API endpoint
# services implement the business logic, uses models and utils
class ServiceA:
    def __init__(self):
        pass

    def perform_operation(self, input_data):
        # Simulate some processing delay
        time.sleep(random.uniform(1.2, 2))

        # Perform a fake operation on the input data (e.g., reverse the input string)
        result = self._generate_word(random.randint(120, 500))

        return result

    def _generate_word(self, length):
        """Generate a random word of given length."""
        letters = string.ascii_lowercase*2 + " "*7 + "\n"
        return ''.join(random.choice(letters) for _ in range(length))
