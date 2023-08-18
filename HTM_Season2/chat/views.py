from django.shortcuts import render

# Create your views here.


def chat_box(request, chat_box_name):
    return render(
        request,
        'chat/chat_box.html',
        {"chat_box_name": chat_box_name}
    )
