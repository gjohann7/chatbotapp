Accounts
========

Accounts is a Django app to manage user utilities.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "chatbotapp.accounts" to your INSTALLED_APPS setting like this:

```python
    INSTALLED_APPS = [
        ...
        'chatbotapp.accounts',
    ]
```

2. Include the accounts URLconf in your project urls.py like this:

```python
    path('accounts/', include('accounts.urls')),
```

3. Run ``python manage.py migrate`` to create the accounts models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/accounts/ to access its main page.