from django.urls import path
from .views import BirthdayReminderView, ChatPageView, CreateConversationView, ChatAPIView,DashboardView


urlpatterns = [
    path('', ChatPageView.as_view(), name='chat'),
    path('new/', CreateConversationView.as_view(), name='new_chat'),
    path('chat/<int:convo_id>/', ChatAPIView.as_view(), name='chat_api'),
    path('birthday-reminder/', BirthdayReminderView.as_view(), name='birthday_reminder'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]