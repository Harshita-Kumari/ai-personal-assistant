import os
from openai import OpenAI
from datetime import date
from .models import Birthday
from .models import UserMemory


class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    # 🎂 Check today's birthdays
    def check_birthdays(self, user):
        today = date.today()

        birthdays = Birthday.objects.filter(
            user=user,
            date__month=today.month,
            date__day=today.day
        )

        if birthdays.exists():
            names = ", ".join([b.name for b in birthdays])
            return f"🎉 Today is {names}'s birthday!"

        return ""

    # 🤖 AI Response
    

    def get_response(self, messages, user):
        try:
            # 🧠 Fetch memory
            memories = UserMemory.objects.filter(user=user)
            memory_text = "\n".join([f"{m.key}: {m.value}" for m in memories])

            system_prompt = f"""
            You are a smart assistant.

            User info:
            {memory_text}

            Use this information when answering.
            """

            full_messages = [{"role": "system", "content": system_prompt}] + messages

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=full_messages
            )

            return response.choices[0].message.content

        except Exception as e:
            print(e)
            return "Error"