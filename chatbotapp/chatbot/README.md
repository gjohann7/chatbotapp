Chatbot
=======

Chatbot is a Django app to manage AIML chatbot utilities.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "chatbotapp.chatbot" to your INSTALLED_APPS setting like this:

```python
    INSTALLED_APPS = [
        ...
        'chatbotapp.chatbot',
    ]
```

2. Include the chatbot URLconf in your project urls.py like this:

```python
    path('chatbot/', include('chatbot.urls')),
```

3. Run ``python manage.py migrate`` to create the chatbot models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/chatbot/conversation/ to access its main page.