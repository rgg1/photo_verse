from django.urls import path
from .views import conversations_view, conversation_view, start_conversation_view

urlpatterns = [
    path('', conversations_view, name='conversations'),
    path('start/<int:user_id>/', start_conversation_view, name='start_conversation'),
    path('<int:conversation_id>/', conversation_view, name='conversation'),
]