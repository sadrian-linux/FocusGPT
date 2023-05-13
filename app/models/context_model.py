class PromptContext:
    def __init__(self, creativity_level, role):
        self.creativity_level = creativity_level
        self.role = role
    
    @property
    def response_type(self):
        response_types = {
            1: "Concise, accurate, relevant and on point",
            2: "Concise, accurate and relevant",
            3: "Accurate, relevant and somewhat exploring new ideas",
            4: "Relevant while going out of the box, coming up with innovative new ways and approaches",
            5: "Full on out of this world, out of all boxes, full of innovation, creativity and imagination"
        }

        response = response_types.get(self.creativity_level)
        return response
