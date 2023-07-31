from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation
from .forms import MessageForm
from django.contrib.auth.models import User
from django.db.models import Q
from notifications.models import Notification
from accounts.forms import UserSearchForm

# Create your views here.

@login_required
def conversations_view(request):
    form = UserSearchForm(request.GET)
    users = User.objects.none()

    if form.is_valid():
        users = User.objects.filter(username__icontains=form.cleaned_data['username'])

    conversations1 = request.user.conversations1.all()
    conversations2 = request.user.conversations2.all()
    conversations = conversations1.union(conversations2)
    return render(request, 'messaging/conversations.html', {'conversations': conversations, 'form': form, 'users': users})

@login_required
def conversation_view(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            Notification.objects.create(user=conversation.other_user(request.user), type=Notification.MESSAGE, extra_id=conversation.id, extra_info=request.user)
            form = MessageForm()
    else:
        form = MessageForm()
    messages = conversation.messages.all()
    return render(request, 'messaging/conversation.html', {'conversation': conversation, 'messages': messages, 'form': form})

@login_required
def start_conversation_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    try:
        conversation = Conversation.objects.get(
            (Q(user1=request.user) & Q(user2=other_user)) | (Q(user1=other_user) & Q(user2=request.user))
        )
    except Conversation.DoesNotExist:
        conversation = Conversation.objects.create(user1=request.user, user2=other_user)
    return redirect('conversation', conversation_id=conversation.id)