Core
=======

Core is a Django app to manage web app base-utilities.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "chatbotapp.core" to your INSTALLED_APPS setting like this:

```python
    INSTALLED_APPS = [
        ...
        'chatbotapp.core',
    ]
```

2. Include the core URLconf in your project urls.py like this:

```python
    path('core/', include('core.urls')),
```

3. Run ``python manage.py migrate`` to create the core models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/core/ to access its main page.