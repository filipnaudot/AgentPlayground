import random
import base64
import time
from openai import OpenAI


from dotenv import load_dotenv
load_dotenv()

client = OpenAI()



class OpenAIAgent:
    """
    An agent that uses OpenAI's function calling to decide and execute actions.
    """

    def __init__(self, game_instance, model_name="gpt-4o", temperature=0.4):
        """
        :param openai_api_key: Your OpenAI API key (string).
        :param game_instance: An instance of the game with movement methods.
        :param model_name: The name of the OpenAI model, e.g., "gpt-4-0613".
        :param temperature: Sampling temperature.
        """
        self.game = game_instance
        self.model_name = model_name
        self.temperature = temperature


        self.tools = [
        {
            "type": "function",
            "function": {
                "name": "move_up",
                "description": "Move the player up by one cell.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_down",
                "description": "Move the player down by one cell.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_left",
                "description": "Move the player left by one cell.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_right",
                "description": "Move the player right by one cell.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]
        

    def generate(self, system_message: dict, user_message_content: str, base64_image: str):
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                system_message,
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message_content,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            tools=self.tools,
            tool_choice="required",
        )

        return completion.choices[0].message.tool_calls[0].function.name


    def step(self, world: str = None, steps_taken=0):
        ascii: bool = False
        base64_image: str = ""
        if not ascii: base64_image = self._encode_image(world)

        # System message
        img_system_message = {
            "role": "system",
            "content": (
                "You are an AI agent controlling a player in a 2D grid-based game. Your player is denoted with a BLUE squere. "
                "Your goal is to move the BLUE squere from start (RED squere) to the GREEN squere (goal) without crossing BLACK squeres (walls). "
                "You can not move to or through a BLACK squere (wall). It is simply not possible. If atempted, the BLUE squere (you) will simply not move (which is bad). "
                "You have won when the BLUE squere (you) and the GREEN squere (goal) are on the same cell/squere, i.e. the BLUE squere is on top of the GREEN and the GREEN is not visible. "
                "The current game grid is provided as an image. "
                "Use the available movement functions to move the BLUE squere in order to reach goal (the GREEN squere)."
            )
        }

        ascii_system_message = {
            "role": "system",
            "content": (
                "You are an AI agent controlling a player in a 2D grid-based game. Your player is denoted 'P'."
                "Your goal is to move 'P' from 'S' (start) to 'G' (goal) without crossing walls (#). "
                "It is not possible to move towards a wall '#', you will simple stand still if this is attempted. "
                "You have won when 'P' and 'G' are in the same cell, i.e. 'P' is on top of 'G'. "
                "The current grid is provided in ASCII. "
                "Use the available movement functions to decide where to move 'P' in order to reach 'G'."
            )
        }

        system_message = {}
        user_message_content = f"Steps taken so far: {steps_taken}\nYour move history: {self.game.move_history}"
        print(user_message_content)

        if ascii:
            system_message = ascii_system_message
            user_message_content += f"ASCII Map:\n```\n{world}\n```"
        else:
            system_message = img_system_message

        function_name = self.generate(system_message, user_message_content, base64_image)
        print(f"FUNCTION: {function_name}\n\n")

        method = getattr(self.game, function_name, None)
        if callable(method):
            method()
        else:
            print(f"Unknown function: {function_name}. Falling back to random action.")
            self.execute_random_action()


    def execute_random_action(self):
        """Execute a random movement action."""
        action = random.choice(["move_up", "move_down", "move_left", "move_right"])
        getattr(self.game, action)()


    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")