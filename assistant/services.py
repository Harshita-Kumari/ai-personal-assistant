# import os
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def get_ai_response(messages):
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return response.choices[0].message.content

import os
from openai import OpenAI


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content