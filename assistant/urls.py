from django.urls import path
from .views import ChatPageView, CreateConversationView, ChatAPIView

urlpatterns = [
    path('', ChatPageView.as_view(), name='chat'),
    path('new/', CreateConversationView.as_view(), name='new_chat'),
    path('new/', CreateConversationView.as_view(), name='new_chat'),
    path('chat/<int:convo_id>/', ChatAPIView.as_view(), name='chat_api'),
]