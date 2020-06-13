# Welcome to the Chatbot-App documentation!

*Guilherme Alexandre dos Santos Johann*

>JavaScript source code documentation starts [here](#javascript-source-code-documentation).

# Python source code documentation

## Accounts
### Models

#### class chatbotapp.accounts.models.*PasswordReset*(models.Model)
Definition of the password reset model.
- Inherits models.Model (class), a base definition of a model class.

<br/>

#### class chatbotapp.accounts.models.*User*(AbstractBaseUser, PermissionsMixin)
Definition of the user model.

**Parameters**
- *AbstractBaseUser (class)* – The base of the user model.
- *PermissionsMixin (class)* – Add the fields and methods necessary to support the Group and Permission models using the ModelBackend.

<br/>

### Forms

#### class chatbotapp.accounts.forms.*EditAccountForm*(forms.ModelForm)
Definition of the user password reset form.

**Parameters**
- forms.ModelForm (class) – The main implementation of all the Model Form logic.

**Raises**
- forms.ValidationError – An email found exception occurs when the entered email already exists in the database.

<br/>


#### *clean_email()*
Validation of the email consistency.

**Returns** - The user email entered in the form.

**Return type** - str

**Raises**
- forms.ValidationError – An email found exception occurs when the entered email already exists in the database.

<br/>


#### class chatbotapp.accounts.forms.*PasswordResetForm*(forms.Form)
Definition of the user password reset form.

**Parameters**
- forms.Form (class) – A collection of Fields, plus their associated data.

**Raises**
- forms.ValidationError – An email not found exception occurs when the entered email doesn’t exist in the database.

<br/>


#### *clean_email()*
Validation of the email consistency.

**Returns** - The user email entered in the form.

**Return type** - str

**Raises**\
forms.ValidationError – An email not found exception occurs when the entered email doesn’t exist in the database.

<br/>


#### *save()*
Persists the password reset request in the database.

#### class chatbotapp.accounts.forms.*RegisterForm*(forms.ModelForm)
Definition of the user registration form.

- Inherits from forms.ModelForm (class), the main implementation of all the Model Form logic.

**Raises**
- forms.ValidationError – A password mismatch exception occurs when both password fields don’t match.

<br/>

#### *clean_password2()*
Validation of the password match.

**Returns** - The user password entered in the form.

**Return type** - str

**Raises**
- forms.ValidationError – A password mismatch exception occurs when both password fields don’t match.

<br/>

#### *save()*
Persists the user in the database.

<br/>

### Views
#### chatbotapp.accounts.views.*change_password*(request)
Definition of the user password change view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.accounts.views.*editable_profile*(request)
Definition of the user profile view.

- This view also allows the user to edit its profile.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.accounts.views.*password_reset*(request)
Definition of the user password reset view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.accounts.views.*password_reset_confirmation*(request, key)
Definition of the user password reset confirmation view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.accounts.views.*register*(request)
Definition of the user registration view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

---

## Chatbot
### Models
#### class chatbotapp.chatbot.models.*Message*(models.Model)
Definition of the message model.

- Inherits models.Model (class), a base definition of a model class.

<br/>

### Views
#### chatbotapp.chatbot.views.*conversation*(request)
Definition of the chat view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.chatbot.views.*handle_message*(request, message)
Management definition of the client message to the chatbot.

**Parameters**
- request (HttpRequest) – The client request to the server.

- message (str) – The message received from the client to the chatbot.

**Returns** - The server response to the client.

**Return type** - HttpResponse

---

## Botbrain
### AIML bot
#### class chatbotapp.chatbot.botbrain.aimlbot.*AimlChatbot*(platform="windows", chatbot="")
Definition of the AIML chatbot class.

- This class acts as the bridge between the server and the chatbot engine. It also provides methods to handle the client messages and retrieve the chatbot responses. It inherits from EmbeddedDataFileBot (class), the base to create the AIML chatbot class.

**Parameters**
- platform (str, optional) – The operating system that hosts the app, by default windows.

- chatbot (str, optional) – The chatbot filename, by default an empty string.

<br/>

#### *retrieve_message(message="")*
Retrieves a response message from the chatbot.

- Send the message to the chatbot engine; if it gets a non-UDC response, it is sent to the server. Hence, if the response is a UDC one, send a transformed message; if it gets a non-UDC response, it is sent to the server. Although, if the response still is an UDC one, store the message as a previous one, send it to the chatbot engine and send the UDC response do the server.

**Parameters**
- message (str) – The message sent from the server to the chatbot.

**Returns** - The response message from the chatbot.

**Return type** - str

<br/>

#### *set_previous_message(previous_message="")*
Storing of the last message before retrieving a UDC response.

- If retrieving a UDC response, the previous message is stored and resend to the chatbot engine to maintain the close context (that tag). It also adds single spaces in the beginning and end of the message.

**Parameters**
- previous_message (str) – The message to be changed.

<br/>

#### *set_settings()*
Sets up the chatbot settings.

#### *transform_message(message)*
Changes the message if it includes gerunds.

**Parameters**
- message (str) – The message to be analysed.

**Returns** - The message with or without alteration.

**Return type** - str

---

## Core
### Models
#### class chatbotapp.core.models.*Contact*(models.Model)
Definition of the contact model.

- Inherits from Model (class), a base definition of a model class.

<br/>

### Forms
#### class chatbotapp.core.forms.*ContactForm*(forms.Form)
Definition of the contact form.

- Inherits from Form (class), a collection of Fields, plus their associated data.

**Raises**
- forms.ValidationError – A minimum word exception occurs when the user entered less than two words in the message field of the contact form.

<br/>

#### *clean_message()*
Validation of the message length.

**Returns** - The user entered message.

**Return type** - str

**Raises**
- forms.ValidationError – A minimum word exception occurs when the user entered less than two words in the message field of the contact form.

<br/>

#### *save()*
Persists the contact message in the database, send emails to the site contact email about the new message and to the user who sent the message.

<br/>

### Views
#### class chatbotapp.core.views.*CustomAuthenticationForm*(AuthenticationForm)
Definition of a Django-authentication-form-based form.

- Inherits from AuthenticationForm (class), a base class for authenticating users.

**error_messages** - Error message key-value pair.

**Type** - dict

<br/>

#### chatbotapp.core.views.*error_500_view*(request)
Definition of the 500 error view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

#### chatbotapp.core.views.*index*(request)
Definition of the app index view.

**Parameters**
- request (HttpRequest) – The client request to the server.

**Returns** - The server response to the client.

**Return type** - HttpResponse

<br/>

### Mail
#### chatbotapp.core.mail.*send_mail_template*(subject, template_name, context, recipient_list, from_email="chatbot.app.contact@gmail.com", fail_silently=False)
Send mail definition.

**Parameters**
- subject (str) – The email subject.

- template_name (str) – The email template path.

- context (dict) – The context of the email message, which holds the email information.

- recipient_list (list) – An email list to send the emails.

- from_email (str, optional) – The sender email, by default settings.DEFAULT_FROM_EMAIL

- fail_silently (bool, optional) – Defines whether an error occurred when sending the email is raised, by default False

<br/>

### Utils
#### class chatbotapp.core.utils.*CustomMinimumLengthValidator*(min_length=6)
Definition of a password validator, which validates if the password isn’t too short.

**Parameters**
- min_length (int, optional) – The minimum length of the password, by defaul 6.

<br/>

#### *get_help_text()*
Definition of the help text in case of a fail validation.

**Returns** - The help text.

**Return type** - str

<br/>

#### *validate(password, user=None)*
Definition of the validation method.

**Parameters**
- password (str) – The password entered in a form.

- user (dict, optional) – The user data, by default None

**Raises**
- ValidationError – The invalid password exceptions occurs when a password is too short.

<br/>

#### class chatbotapp.core.utils.*CustomNumericPasswordValidator*
Definition of a password validator, which validates if the password isn’t composed only by numbers.

<br/>

#### *get_help_text()*
Definition of the help text in case of a fail validation.

**Returns** - The help text.

**Return type** - str

<br/>

#### *validate(password, user=None)*
Definition of the validation method.

**Parameters**
- password (str) – The password entered in a form.

- user (dict, optional) – The user data, by default None

**Raises**
- ValidationError – The password entirely numeric exceptions occurs when a password if composed only by numbers.

<br/>

#### chatbotapp.core.utils.*generate_hash_key*(salt, random_str_size=6)\
Generates a hash key.

**Parameters**
- salt (str) – A user personal information.

- random_str_size (int, optional) – The length of the random key, by default 6

**Returns** - A hash object digested as a string.

**Return type** - str

<br/>

#### chatbotapp.core.utils.*introductory_messages*(user)
Persists the chatbot introductory messages to a new user.

**Parameters**
- user (class) – The new user data.

<br/>


# JavaScript source code documentation

## Script file

### window

This IIFE as object is responsible for the app management.

<br/>

#### *onclick*
This function handles the window click.

**Parameters**

-   `event`: **[Event][73]** An event triggered in the window.

<br/>

#### *onkeydown*
This function handles the window key down event.

<br/>

**Parameters**

-   `event`: **[Event][73]** An event triggered in the window.

<br/>

#### *onload*
This function handles the site set up.

---

<br/>

### HTMLElements

This IIFE as object is responsible for attaching HTML elements to objects.

-   **Postcondition:** All available elements must exist as objects.

**Returns** - **[Object][74]** An object with all available elements.

---

<br/>

### AccessibilityHandler

This IIFE as object is responsible for attaching HTML elements to objects.

**Returns** - **[Object][74]** An object with all accessibility methods.

#### *generateTabIndexPath*
This recursive function generates the tab index path of the current page.

**Parameters**

-   `node`: **[HTMLElement][75]** The body element from HTML. (optional, default `HTMLElements.body`)
-   `leaf`: **[Number][76]** The number child handled. (optional, default `0`)

<br/>

#### *updateTabIndexPath*
This function updates the tab index path of the current page.

**Parameters**

-   `node`: **[HTMLElement][75]** The new HTML element to be added to the list.

<br/>

#### *handleMenuAccess*
This function handles the menu access.

**Parameters**

-   `next`; **[Number][76]** A index from the tab index path.
-   `direction`: **[Number][76]** The direction to move in the tab index path.

<br/>

#### *handleIndex*
This function manages the tab-index path index.

**Parameters**

-   `direction`: **[Number][76]** The direction to move in the tab index path.

<br/>

#### *navigateByArrow*
This function handles the arrow navigation in the page.

**Parameters**

-   `eventKey`: **[String][77]** The pressed key name.
-   `ctrlKey`: **[Boolean][78]** The control key press state.
-   `onFocus`: **[HTMLElement][75]** The HTML element which holds the focus.

<br/>

#### *navigateByTab*
This function handles the tab navigation in the page.

**Parameters**

-   `shiftKey`: **[Boolean][78]** The shift key press state.

<br/>

#### *improveKeyboardNavigation*
This function handles the page navigation improvement.

**Parameters**

-   `onFocus`: **[HTMLElement][75]** The HTML element which holds the focus.
-   `eventKey`: **[String][77]** The pressed key name.
-   `ctrlKey`: **[Boolean][78]** The control key press state.
-   `shiftKey`: **[Boolean][78]** The shift key press state.

<br/>

#### *handleMenuOnClick*
This function handles the menu click, which updates its display state.

**Parameters**

-   `eventPath`: **[Array][79]** The triggered event path.

<br/>

#### *handleMenuVisibility*
This function handles the menu visibility, which updates its display state.

**Parameters**
-   `eventKey`: **[String][77]** The pressed key name.
-   `eventTarget`: **[HTMLElement][75]** The triggered event target.

<br/>

#### *handleFontSize*
This function handles the font size update.

<br/>

#### *load*
This function sets up the page accessibilities approaches.

**Parameters**

-   `path`: **[String][77]** The current window location path name.
-   `focusedElement`: **[HTMLElement][75]** The HTML element which holds the focus.

<br/>

#### *handleMenuAccessKey*
This function handles the shortcut keys to access the menu items.

**Parameters**

-   `eventKey`: **[String][77]** The pressed key name.

<br/>

#### *textToSpeech*
This function synthesizes text.

**Parameters**

-   `text`: **[String][77]** The text to be synthesized.

---

<br/>

### ChatHandler

This IIFE as object is responsible for the chat presentation and functionality.

**Returns** - **[Object][74]** An object which controls the chat presentation and functionality.

<br/>

#### *scrollChatView*
This function performs the page scroll.

<br/>

#### *textToSpeech*
This function finds the message to be synthesized.

**Parameters**

-   `eventOrigin`: **[HTMLElement][75]** The element that generated the event.

<br/>

#### *appendMessage*
This function attaches a message to the chat view.

**Parameters**

-   `divClassName`: **[String][77]** A class name attribute.
-   `hiddenAuthor`: **[String][77]** The message author.
-   `messageContent`: **[String][77]** The message content or the message itself.

<br/>

#### *handleMessage*
This function handles the received message.

**Parameters**

-   `divClassName`: **[String][77]** A class name attribute.
-   `hiddenAuthor`: **[String][77]** The message author.
-   `messageContent`: **[String][77]** The message content or the message itself.

<br/>

#### *publishQuestion*
This function handles the user message publishing.

<br/>

#### *publishResponse*
This function handles the chatbot message publishing.

**Parameters**

-   `response`: **[String][77]** The message from the chatbot.

<br/>

#### *loadMessages*
This function handles the old messages load.

---

<br/>

### LocalStorage

This IIFE as object is responsible for the Local Storage management.

**Returns** - **[Object][74]** An object which manage the Local Storage.

<br/>

#### *setUp*
This function sets up the Local Storage state.

<br/>

#### *append*
This function appends a message to the message list.

**Parameters**

-   `message`: **[String][77]** A message sent by the user.

<br/>

#### *post*
This function updates the associated Local Storage data.

<br/>

#### *apply*
This function maps the message list with the given function.

**Parameters**

-   `fun`: **[Function][80]** A function to be mapped into the message list.

<br/>

#### *load*
This function loads the current username into the Local Storage.

**Parameters**

-   `username`: **[String][77]** The current user username.

---

<br/>

### responseHandler

This function handles the chatbot response.

**Returns** - **[Object][74]** An object which manage the chatbot response.

<br/>

#### *dispatch*
This function releases a message in the queue to be shown in the chat.

<br/>

#### *append*
This function appends a message in the message queue if it exists,
or it is directly released to the chat.

**Parameters**

-   `message`: **[String][77]** The message to be sent to the chat.

<br/>

#### *error*
This function handles a message from the user whose sending
to the server failed.

**Parameters**

-   `message`: **[String][77]** The message to be sent to the chat.

<br/>

#### *recovered*
This function handles the actions to be performed when the server has recovered from a failed request attempt.

---

<br/>

### Manager

This IIFE as object is responsible for the worker management.

**Returns** - **[Object][74]** An object which manage the worker.

<br/>

#### *onMessage*
This function listens to the worker sent messages.

**Parameters**

-   `event`: **[Event][73]** An event received from the worker.

<br/>

#### *postMessage*
This function sends a message to the worker.

**Parameters**

-   `state`: **state** A state defined in the shared-data.js.

<br/>

#### *terminate*
This function terminates the worker.

---

<br/>

### REQUEST

This function make a request to the server.

**Parameters**

-   `message`: **[String][77]** The message to be sent to the server.

<br/>

#### *onload*
This function handles the success response of the sent request.

<br/>

#### *onerror*
This function handles the failed response of the sent request.

---

<br/>

## Service Worker file

### Task

This IIFE as object is responsible for the worker job.

**Returns** - **[Object][13]** An object with the update state method.

<br/>

#### *clear*
This function clear all the active timeouts.

<br/>

#### *onLoad*
This function handles the success response of the sent request.

<br/>

#### *onError*
This function handles the failed response of the sent request.

<br/>

#### *run*
This function make the request to the server.

**Parameters**

-   `command`: **[String][14]** A command defined in the shared-data.js.

<br/>

#### *update*
This function updates the worker state and can be used outside of its scope.

**Parameters**

-   `state`: **[Number][15]** A state defined in the shared-data.js.

<br/>

#### *selfUpdate*
This function updates the worker state and can be used only inside its scope.

**Parameters**

-   `state`: **[Number][15]** A state defined in the shared-data.js.

<br/>

#### *onmessage*
This function handles the script messages.

**Parameters**

-   `event`: **[Event][16]** An event received from the script.


<br/>

>End of document.

[73]: https://developer.mozilla.org/docs/Web/API/Event

[74]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[75]: https://developer.mozilla.org/docs/Web/HTML/Element

[76]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[77]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[78]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[79]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[80]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[13]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[14]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[15]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[16]: https://developer.mozilla.org/docs/Web/API/Event