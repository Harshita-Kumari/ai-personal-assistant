from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from .models import Conversation, Message, Birthday
from .services import AIService


from .models import UserMemory


# 🧠 Chat Page
class ChatPageView(LoginRequiredMixin, View):
    def get(self, request):
        convo_id = request.GET.get("convo_id")

        if convo_id:
            try:
                conversation = Conversation.objects.get(
                    id=convo_id,
                    user=request.user
                )
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.filter(
                    user=request.user
                ).first()
        else:
            conversation = Conversation.objects.filter(
                user=request.user
            ).first()

        if not conversation:
            conversation = Conversation.objects.create(user=request.user)

        conversations = Conversation.objects.filter(user=request.user)
        messages = Message.objects.filter(conversation=conversation)

        return render(request, "assistant/chat.html", {
            "conversation": conversation,
            "messages": messages,
            "conversations": conversations
        })


# ➕ New Chat
class CreateConversationView(LoginRequiredMixin, View):
    def get(self, request):
        Conversation.objects.create(user=request.user)
        return redirect('chat')


# 🤖 Chat API
class ChatAPIView(LoginRequiredMixin, View):
    def post(self, request, convo_id):
        user_message = request.POST.get("message")

        if not user_message:
            return JsonResponse({"response": "⚠️ Empty message"}, status=400)

        # 🎂 ADD BIRTHDAY COMMAND
        if "add birthday" in user_message.lower():
            try:
                # Format: Add birthday Rahul 2002-05-10
                parts = user_message.split()
                name = parts[2]
                date_obj = datetime.strptime(parts[3], "%Y-%m-%d").date()

                Birthday.objects.create(
                    user=request.user,
                    name=name,
                    date=date_obj
                )

                return JsonResponse({
                    "response": f"✅ Birthday saved for {name}"
                })

            except:
                return JsonResponse({
                    "response": "⚠️ Use format: Add birthday Rahul 2002-05-10"
                })

        # 🎂 SHOW BIRTHDAYS
        if "show birthdays" in user_message.lower():
            birthdays = Birthday.objects.filter(user=request.user)

            if not birthdays.exists():
                return JsonResponse({
                    "response": "No birthdays saved."
                })

            data = "\n".join([
                f"{b.name} - {b.date}" for b in birthdays
            ])

            return JsonResponse({"response": data})

        # 💬 NORMAL CHAT FLOW
        try:
            conversation = Conversation.objects.get(
                id=convo_id,
                user=request.user
            )
        except Conversation.DoesNotExist:
            return JsonResponse({
                "response": "⚠️ Conversation not found"
            }, status=404)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_message
        )

        # Set title (first message)
        if conversation.title == "New Chat":
            conversation.title = user_message[:30]
            conversation.save()

        # Get chat history
        messages = Message.objects.filter(conversation=conversation)

        formatted_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]


        # 🧠 Detect memory
        if "my name is" in user_message.lower():
            name = user_message.split("is")[-1].strip()

            UserMemory.objects.update_or_create(
                user=request.user,
                key="name",
                defaults={"value": name}
            )

            return JsonResponse({"response": f"Nice to meet you, {name} 😊"})        

        # 🤖 AI RESPONSE
        ai_service = AIService()

        try:
            ai_reply = ai_service.get_response(
                formatted_messages,
                request.user
            )
        except Exception as e:
            print("AI ERROR:", e)
            return JsonResponse({
                "response": "⚠️ AI error occurred"
            }, status=500)

        # Save AI message
        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=ai_reply
        )

        return JsonResponse({"response": ai_reply})
    
from datetime import date

class BirthdayReminderView(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()

        birthdays = Birthday.objects.filter(
            user=request.user,
            date__month=today.month,
            date__day=today.day
        )

        if birthdays.exists():
            names = ", ".join([b.name for b in birthdays])
            return JsonResponse({
                "message": f"🎉 Today is {names}'s birthday!"
            })

        return JsonResponse({"message": ""})
    
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conversation, Message, Birthday


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        conversations = Conversation.objects.filter(user=user)
        messages = Message.objects.filter(conversation__user=user)
        birthdays = Birthday.objects.filter(user=user)

        context = {
            "total_conversations": conversations.count(),
            "total_messages": messages.count(),
            "total_birthdays": birthdays.count(),
            "recent_chats": conversations.order_by('-created_at')[:5]
        }

        return render(request, "assistant/dashboard.html", context)