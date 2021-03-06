# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Message
from chatbotapp.accounts.models import User
import json
import sys
from .botbrain.aimlbot import AimlChatbot

template = 'chatbot/'
bot = AimlChatbot("windows", "botbrain")
INTERNAL_COMMANDS = {
    'issue': 'Em, eu já volto',
    'back': 'Voltei kk'
}


@login_required
def conversation(request):
    """Definition of the chat view.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    messages = Message.objects.filter(
        owner=request.user).values('is_bot', 'content').reverse()

    messages_length = len(messages)
    messages_load = 150
    context = {
        'messages': list(messages),
        'show_button': messages_length >= messages_load,
        'messages_load': messages_load,
        'last_messages': messages[messages_length-150:] if messages_length >= messages_load else messages
    }
    return render(request, template + 'conversation.html', context)


def handle_message(request, message):
    """Management definition of the client message to the chatbot.

    Parameters
    ----------
    request : HttpRequest
        The client request to the server.
    message : str
        The message received from the client to the chatbot.

    Returns
    -------
    HttpResponse
        The server response to the client.
    """
    response = "test approved"

    if message != "test connection":
        # if '{"username":"' in str(message):
        #     tmp = json.loads(message)
        #     # global user
        #     # user = User.objects.get(username=tmp["username"])
        #     message = tmp["message"]
        if 'INTERNAL COMMAND' in message:
            new_message = ''
            response = "internal command successful"
            if 'ISSUE' in message:
                new_message = INTERNAL_COMMANDS["issue"]
            elif 'RECOVERED' in message:
                new_message = INTERNAL_COMMANDS["back"]
                response = new_message
            Message(content=new_message, owner=request.user, is_bot=True).save()
        else:
            try:
                Message(content=message, owner=request.user).save()
                response = bot.retrieve_message(str(message))
                response = response.replace('\n', ' ')
                if response[-1:] == ".":
                    response = response[:-1]
                Message(content=response, owner=request.user,
                        is_bot=True).save()
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
            except:
                print("Unexpected error:", sys.exc_info()[0])
    reply = {
        "username": request.user.username,
        "response": response
    }
    return HttpResponse(json.dumps(reply, ensure_ascii=False), status=200)
