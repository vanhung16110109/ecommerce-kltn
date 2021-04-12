from django.shortcuts import render


# Create your views here.
#chat-bot
def chatbot(request):
    return render(request, 'chatbot/chatbot.html', {})

