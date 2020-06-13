# Chatbot-App

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://gjohann7.github.io/chatbot_app_doc/)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://chatbot-patient.herokuapp.com/)
[![MIT license](https://img.shields.io/badge/License-BSD-blue.svg)](https://gitlab.com/gjohann7/chatbotapp/-/blob/master/LICENSE)

Chatbot-App is a Django app to handle an AIML chatbot. The app default
use case is about psychopathology and its practical study.

Detailed source code documentation is in this [page](https://gjohann7.github.io/chatbot_app_doc/).

## Installation

Download the chatbotapp in add it into your project directory and 
run `python manage.py -r requirements.txt` to install the app requirements.

## Usage

Add "chatbotapp" to your INSTALLED_APPS setting:

```python
   INSTALLED_APPS = [
        ...,
        'chatbotapp',
   ]
```

Include the chatbotapp URLconf in your project `urls.py`:

```python
    path('chatbotapp/', include('chatbotapp.urls')),
```

Run `python manage.py makemigrations` and then `python manage.py migrate` to create the chatbotapp models.

Visit `http://127.0.0.1:PORT/chatbotapp/` to access the home page.

## Author

Guilherme Alexandre dos Santos Johann (2020).

Contact: <a href="https://www.linkedin.com/in/guilherme-johann/" target="_blank">Linkedin</a> or <a href="mailto:g.johann98@gmail.com" target="_blank">Email</a>.

## License

[BSD-3-Clause Licensed](https://opensource.org/licenses/BSD-3-Clause) (file [LICENSE](https://gitlab.com/gjohann7/chatbotapp/-/blob/master/LICENSE)). © Guilherme Alexandre dos Santos Johann, 2020.

## Project status

Project under development. Test phase.
