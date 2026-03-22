# import os
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import ChatHistory
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def chat_page(request):
#     return render(request, "chat.html")


# def chat_api(request):
#     if request.method == "POST":
#         user_input = request.POST.get("message")

#         # Get previous chats (memory)
#         history = ChatHistory.objects.all().order_by('-created_at')[:5]

#         messages = [
#             {"role": "system", "content": "You are a helpful personalized assistant."}
#         ]

#         # Add memory
#         for chat in reversed(history):
#             messages.append({"role": "user", "content": chat.user_message})
#             messages.append({"role": "assistant", "content": chat.ai_response})

#         messages.append({"role": "user", "content": user_input})

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages
#         )

#         ai_reply = response.choices[0].message.content

#         # Save to DB
#         ChatHistory.objects.create(
#             user_message=user_input,
#             ai_response=ai_reply
#         )

#         return JsonResponse({"response": ai_reply})
    
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import Conversation, Message
# from .services import get_ai_response

# @login_required
# def chat_page(request):
#     conversations = Conversation.objects.filter(user=request.user)
#     return render(request, "chat.html", {"conversations": conversations})


# @login_required
# def create_conversation(request):
#     convo = Conversation.objects.create(user=request.user)
#     return redirect('chat')


# @login_required
# def chat_api(request, convo_id):
#     if request.method == "POST":
#         message = request.POST.get("message")

#         convo = Conversation.objects.get(id=convo_id, user=request.user)

#         Message.objects.create(conversation=convo, role="user", content=message)

#         # Fetch conversation history
#         msgs = Message.objects.filter(conversation=convo)

#         messages = [{"role": m.role, "content": m.content} for m in msgs]

#         ai_reply = get_ai_response(messages)

#         Message.objects.create(conversation=convo, role="assistant", content=ai_reply)

#         return JsonResponse({"response": ai_reply})

from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conversation, Message
from .services import AIService


class ChatPageView(LoginRequiredMixin, View):
    def get(self, request):
        convo_id = request.GET.get("convo_id")

        if convo_id:
            conversation = Conversation.objects.get(id=convo_id, user=request.user)
        else:
            conversation = Conversation.objects.filter(user=request.user).first()

            if not conversation:
                conversation = Conversation.objects.create(user=request.user)

        conversations = Conversation.objects.filter(user=request.user)
        messages = Message.objects.filter(conversation=conversation)

        return render(request, "assistant/chat.html", {
            "conversation": conversation,
            "messages": messages,
            "conversations": conversations
        })

class CreateConversationView(LoginRequiredMixin, View):
    def get(self, request):
        convo = Conversation.objects.create(user=request.user)
        return redirect('chat')


class ChatAPIView(LoginRequiredMixin, View):
    def post(self, request, convo_id):
        user_message = request.POST.get("message")

        conversation = Conversation.objects.get(
            id=convo_id, user=request.user
        )

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_message
        )

        # Fetch history
        messages = Message.objects.filter(conversation=conversation)

        formatted_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        # AI Response
        ai_service = AIService()
        ai_reply = ai_service.get_response(formatted_messages)

        # Save AI message
        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=ai_reply
        )

        return JsonResponse({"response": ai_reply})