/**
 * This IIFE as object is responsible for the app management.
 */
(function App(window, document) {
  let ResponseHandler = {};
  // http://127.0.0.1:8000
  const generateURL = (ending) =>
    `https://chatbot-patient.herokuapp.com/conversation/question=${encodeURIComponent(
      ending
    )}`;
  const SUCCESS_MESSAGE = "internal command successful";
  const OFF_MESSAGE = "Em, eu já volto";
  const OFF_COMMAND = "INTERNAL COMMAND CONNECTION ISSUE";
  const BACK_COMMAND = "INTERNAL COMMAND RECOVERED CONNECTION";
  let server_on = true;

  /**
   * This IIFE as object is responsible for attaching HTML elements to objects.
   * - Poscondition: All available elements must exist as objects.
   * @returns {Object} An object with all available elements.
   */
  const HTMLElements = (function HTMLElements() {
    return {
      body: document.body,
      btnMenu: document.getElementById("btnMenu"),
      btnHome: document.getElementById("btnHome"),
      btnAccessibility: document.getElementById("btnAccessibility"),
      btnChat: document.getElementById("btnChat"),
      btnProfile: document.getElementById("btnProfile"),
      btnLogin: document.getElementById("btnLogin"),
      btnLogout: document.getElementById("btnLogout"),
      btnIntro: document.getElementById("btnIntro"),
      contentWrapper: document.getElementById("contentWrapper"),
      contact: document.getElementById("contact"),
      chat: document.getElementById("chat"),
      smallerFontSize: document.getElementById("smallerFontSize"),
      defaultFontSize: document.getElementById("defaultFontSize"),
      largerFontSize: document.getElementById("largerFontSize"),
      btnSkipMessages: document.getElementById("btnSkipMessages"),
      btnLoadMessages: document.getElementById("btnLoadMessages"),
      chatMessages: document.getElementById("chatMessages"),
      btnsVolumeUp: document.getElementsByClassName("btnVolumeUp"),
      messageField: document.getElementById("messageField"),
      btnSend: document.getElementById("btnSend"),
      idName: document.getElementById("id_name"),
      footer: document.getElementById("footer"),
    };
  })();

  /**
   * This IIFE as object is responsible for attaching HTML elements to objects.
   * @returns {Object} An object with all accessibility methods.
   */
  const AccessibilityHandler = (function AccessibilityHandler() {
    const synth = window.speechSynthesis;
    const utterThis = new SpeechSynthesisUtterance();
    utterThis.lang = "pt-BR";
    const escapeType = ["text", "password", "email"];
    const focusableElements = ["A", "BUTTON", "INPUT", "TEXTAREA", "ARTICLE"];
    let tabIndexPath = [];
    let accesskey = false;
    let index = 0;

    /**
     * This recursive function generates the tab index path of the current page.
     * @param {HTMLElement} node The body element from HTML.
     * @param {Number} leaf The number child handled.
     */
    const generateTabIndexPath = (node = HTMLElements.body, leaf = 0) => {
      if (node.childElementCount) {
        if (node.className !== "btnVolumeUp") {
          generateTabIndexPath(node.children.item(0), 0);
        }
      }
      if (node.parentElement) {
        if (leaf < node.parentElement.childElementCount) {
          if (focusableElements.includes(node.tagName)) {
            if (node.type !== "hidden") {
              tabIndexPath.push(node);
            }
          }
          if (node.nextElementSibling)
            generateTabIndexPath(node.nextElementSibling, ++leaf);
        }
      }
    };

    /**
     * This function updates the tab index path of the current page.
     * @param {HTMLElement} node The new HTML element to be added to the list.
     */
    const updateTabIndexPath = (node) => {
      if (HTMLElements.chat) {
        const chatIndex = tabIndexPath.indexOf(HTMLElements.chat);
        const tail = tabIndexPath.slice(chatIndex);
        tabIndexPath.length = chatIndex;
        tabIndexPath.push(node);
        tabIndexPath.push(...tail);
      }
    };

    /**
     * This function handles the menu access.
     * @param {Number} next A index from the tab index path.
     * @param {Number} direction The direction to move in the tab index path.
     */
    const handleMenuAccess = (next, direction) => {
      if (HTMLElements.body.clientWidth < 993) {
        if (!HTMLElements.btnMenu.checked) {
          while (tabIndexPath[next].parentNode.tagName === "LI") {
            next += direction;
          }
        } else {
          if (tabIndexPath[next].parentNode.tagName !== "LI") {
            HTMLElements.btnMenu.click();
          }
        }
      }
      return next;
    };

    /**
     * This function manages the tab-index path index.
     * @param {Number} direction The direction to move in the tab index path.
     */
    const handleIndex = (direction) => {
      if (direction === 1) {
        if (index === tabIndexPath.length - 1) {
          index = -1;
        }
        if (tabIndexPath[index] === HTMLElements.largerFontSize) {
          index = tabIndexPath.indexOf(HTMLElements.chat) - 1;
        }
      } else if (direction === -1 && index === 0) {
        index = tabIndexPath.length;
      }
      if (
        tabIndexPath[index + direction] === HTMLElements.btnMenu &&
        HTMLElements.body.clientWidth >= 992
      ) {
        index += direction;
      }
      index += direction;
      index = handleMenuAccess(index, direction);
    };

    /**
     * This function handles the arrow navigation in the page.
     * @param {String} eventKey The pressed key name.
     * @param {Boolean} ctrlKey The control key press state.
     * @param {HTMLElement} onFocus The HTML element which holds the focus.
     */
    const navigateByArrow = (eventKey, ctrlKey, onFocus) => {
      if (
        ctrlKey ||
        (onFocus.tagName !== "TEXTAREA" && !escapeType.includes(onFocus.type))
      ) {
        // eventKey === "ARROWRIGHT"
        let direction = 1;
        let element = HTMLElements.messageField;
        if (eventKey === "ARROWLEFT") {
          direction = -1;
          element = HTMLElements.largerFontSize;
        }
        if (ctrlKey && onFocus.className === "btnVolumeUp") {
          index = tabIndexPath.indexOf(element);
        } else {
          handleIndex(direction);
        }
        tabIndexPath[index].focus();
      }
    };

    /**
     * This function handles the tab navigation in the page.
     * @param {Boolean} shiftKey The shift key press state.
     */
    const navigateByTab = (shiftKey) => {
      const lastIndex = index;
      if (!shiftKey) {
        if (tabIndexPath[index] === HTMLElements.largerFontSize) {
          index = tabIndexPath.indexOf(HTMLElements.chat);
          HTMLElements.chat.focus();
        } else if (tabIndexPath[index] === HTMLElements.chat) {
          index = tabIndexPath.indexOf(HTMLElements.messageField);
          HTMLElements.messageField.focus();
        } else {
          handleIndex(1);
          if (index > lastIndex + 1) {
            tabIndexPath[--index].focus();
          }
        }
      } else {
        handleIndex(-1);
        if (index < lastIndex - 1) {
          tabIndexPath[++index].focus();
        }
      }
    };

    /**
     * This function handles the page navigation improvement.
     * @param {HTMLElement} onFocus The HTML element which holds the focus.
     * @param {String} eventKey The pressed key name.
     * @param {Boolean} ctrlKey The control key press state.
     * @param {Boolean} shiftKey The shift key press state.
     */
    const improveKeyboardNavigation = (
      onFocus,
      eventKey,
      ctrlKey,
      shiftKey
    ) => {
      index = tabIndexPath.indexOf(onFocus);
      if (eventKey === "TAB") {
        navigateByTab(shiftKey);
      } else if (eventKey === "ARROWRIGHT" || eventKey === "ARROWLEFT") {
        navigateByArrow(eventKey, ctrlKey, onFocus);
      }
    };

    /**
     * This function handles the menu click, which updates its display state.
     * @param {Array} eventPath The triggered event path.
     */
    const handleMenuOnClick = (eventPath) => {
      if (HTMLElements.btnMenu.checked) {
        if (
          [...eventPath].reduce(
            (accumulator, currentValue) =>
              accumulator === currentValue.id ? false : accumulator,
            "header"
          )
        ) {
          HTMLElements.btnMenu.click();
        }
      }
    };

    /**
     * This function handles the menu visibility, which updates its display state.
     * @param {String} eventKey The pressed key name.
     * @param {HTMLElement} eventTarget The triggered event target.
     */
    const handleMenuVisibility = (eventKey, eventTarget) => {
      if (eventKey === "ENTER") {
        if (eventTarget === HTMLElements.btnMenu) {
          HTMLElements.btnMenu.click();
        }
      }
    };

    /**
     * This function handles the font size update.
     */
    const handleFontSize = () => {
      const changeFontStyle = (size, selected) => {
        if (selected) {
          HTMLElements[size + "FontSize"].className = "selected";
        } else {
          HTMLElements[size + "FontSize"].className = "not-selected";
        }
      };
      const changeFontSize = (size) => {
        if (HTMLElements.chat.className.includes("font-size-")) {
          const className = HTMLElements.chat.className.split("font-size-");
          className.pop();
          className.push(size);
          HTMLElements.chat.className = className.join("font-size-");
          changeFontStyle(size, true);
          HTMLElements.chat.scrollTop = HTMLElements.chat.scrollHeight;
        }
      };
      HTMLElements.smallerFontSize.onclick = () => {
        changeFontSize("smaller");
        changeFontStyle("default");
        changeFontStyle("larger");
      };
      HTMLElements.defaultFontSize.onclick = () => {
        changeFontSize("default");
        changeFontStyle("smaller");
        changeFontStyle("larger");
      };
      HTMLElements.largerFontSize.onclick = () => {
        changeFontSize("larger");
        changeFontStyle("default");
        changeFontStyle("smaller");
      };
    };

    /**
     * This function sets up the page accessibilities approaches.
     * @param {String} path The current window location path name.
     * @param {HTMLElement} focusedElement The HTML element which holds the focus.
     */
    const load = (path, focusedElement) => {
      generateTabIndexPath();
      if (path.includes("conversation")) {
        handleFontSize();
        index = tabIndexPath.indexOf(focusedElement);
      }
      if (path === "/") {
        let allowScroll = false;
        HTMLElements.btnIntro.onfocus = () => {
          window.scrollBy(0, -HTMLElements.contentWrapper.scrollHeight);
          allowScroll = true;
        };
        HTMLElements.idName.onfocus = () => {
          if (allowScroll) {
            window.scrollBy(
              0,
              HTMLElements.contact.scrollTop +
                2 * HTMLElements.footer.scrollHeight
            );
            allowScroll = false;
          }
        };
      }
    };

    /**
     * This function handles the shortcut keys to access the menu items.
     * @param {String} eventKey The pressed key name.
     */
    const handleMenuAccessKey = (eventKey) => {
      if (accesskey) {
        eventKey = eventKey.toUpperCase();
        if (eventKey === "I") {
          HTMLElements.btnHome.focus();
          HTMLElements.btnHome.click();
        } else if (eventKey === "A") {
          HTMLElements.btnAccessibility.focus();
          HTMLElements.btnAccessibility.click();
        }
        if (HTMLElements.btnLogout) {
          if (eventKey === "C") {
            HTMLElements.btnChat.focus();
            HTMLElements.btnChat.click();
          } else if (eventKey === "M") {
            HTMLElements.btnProfile.focus();
            HTMLElements.btnProfile.click();
          } else if (eventKey === "S") {
            HTMLElements.btnLogout.focus();
            HTMLElements.btnLogout.click();
          }
        } else if (eventKey === "E") {
          HTMLElements.btnLogin.focus();
          HTMLElements.btnLogin.click();
        }
        accesskey = false;
      }
      if (eventKey === "/") {
        accesskey = true;
      }
    };

    /**
     * This function synthesizes text.
     * @param {String} text The text to be synthesized.
     */
    const textToSpeech = (text) => {
      utterThis.text = text;
      synth.speak(utterThis);
    };

    return {
      handleMenuAccessKey,
      handleMenuOnClick,
      handleMenuVisibility,
      textToSpeech,
      updateTabIndexPath,
      improveKeyboardNavigation,
      load,
    };
  })();

  /**
   * This IIFE as object is responsible for the chat presentation and functionality.
   * @returns {Object} An object which controls the chat presentation and functionality.
   */
  const ChatHandler = (function ChatHandler() {
    /**
     * This function performs the page scroll.
     */
    const scrollChatView = () =>
      (HTMLElements.chat.scrollTop = HTMLElements.chat.scrollHeight);

    /**
     * This function finds the message to be synthesized.
     * @param {HTMLElement} eventOrigin The element that generated the event.
     */
    const textToSpeech = (eventOrigin) => {
      if (eventOrigin.nextElementSibling) {
        if (eventOrigin.nextElementSibling.tagName === "SPAN") {
          AccessibilityHandler.textToSpeech(
            eventOrigin.nextElementSibling.textContent
          );
        }
      }
    };

    /**
     * This function attaches a message to the chat view.
     * @param {String} divClassName A class name attribute.
     * @param {String} hiddenAuthor The message author.
     * @param {String} messageContent The message content or the message itself.
     */
    const appendMessage = (divClassName, hiddenAuthor, messageContent) => {
      const div = document.createElement("div");
      div.className = divClassName;
      const p = document.createElement("p");
      p.className = "hidden";
      p.innerText = hiddenAuthor;
      div.appendChild(p);
      if (divClassName.split("-")[0] === "bot") {
        const button = document.createElement("button");
        button.className = "btnVolumeUp";
        const icon = document.createElement("i");
        icon.className = "fa fa-volume-up";
        icon.setAttribute("aria-hidden", "true");
        button.appendChild(icon);
        const hiddenSpan = document.createElement("span");
        hiddenSpan.className = "hidden";
        hiddenSpan.innerText = "Ouvir mensagem.";
        button.appendChild(hiddenSpan);
        button.onclick = function () {
          return textToSpeech(this);
        };
        div.appendChild(button);
        AccessibilityHandler.updateTabIndexPath(button);
      }
      const span = document.createElement("span");
      span.innerText = messageContent;
      div.appendChild(span);
      return div;
    };

    /**
     * This function handles the received message.
     * @param {String} divClassName A class name attribute.
     * @param {String} hiddenAuthor The message author.
     * @param {String} messageContent The message content or the message itself.
     */
    const handleMessage = (divClassName, hiddenAuthor, messageContent) => {
      HTMLElements.chatMessages.appendChild(
        appendMessage(divClassName, hiddenAuthor, messageContent)
      );
      scrollChatView();
    };

    /**
     * This function handles the user message publishing.
     */
    const publishQuestion = () => {
      HTMLElements.messageField.focus();
      if (HTMLElements.messageField.value.length > 1) {
        handleMessage(
          "user-message-field",
          "Tu enviaste:",
          HTMLElements.messageField.value
        );
        const message = HTMLElements.messageField.value;
        HTMLElements.messageField.value = "";
        return message;
      }
      return false;
    };

    /**
     * This function handles the chatbot message publishing.
     * @param {String} response The message from the chatbot.
     */
    const publishResponse = (response) => {
      handleMessage("bot-message-field tmp", "Chatbot disse:", "Digitando...");
      setTimeout(() => {
        HTMLElements.chatMessages.removeChild(
          HTMLElements.chatMessages.getElementsByClassName("tmp")[0]
        );
        handleMessage("bot-message-field", "Chatbot disse:", response);
        ResponseHandler.dispatch();
      }, (response.length / 6) * 1000);
    };

    /**
     * This function handles the old messages load.
     */
    const loadMessages = () => {
      if (Messages) {
        if (Messages.all) {
          const hr = document.createElement("hr");
          for (
            let loaded = 0;
            loaded < Messages.load && Messages.all.length;
            loaded++
          ) {
            if (loaded === 0) {
              hr.tabIndex = 0;
              HTMLElements.chatMessages.insertBefore(
                hr,
                HTMLElements.btnLoadMessages.nextElementSibling
              );
            }
            const message = Messages.all.pop();
            let divClassName = "user-message-field";
            let hiddenAuthor = "Tu enviaste:";
            if (message.is_bot) {
              divClassName = "bot-message-field";
              hiddenAuthor = "Chatbot disse:";
            }
            HTMLElements.chatMessages.insertBefore(
              appendMessage(divClassName, hiddenAuthor, message.content),
              HTMLElements.btnLoadMessages.nextElementSibling
            );
            if (loaded === 9 || Messages.all.length === 0) hr.focus();
          }
          if (!Messages.all.length && HTMLElements.btnLoadMessages) {
            HTMLElements.btnLoadMessages.className =
              HTMLElements.btnLoadMessages.className + " hidden";
            HTMLElements.btnLoadMessages.disabled = true;
          }
        }
      }
    };

    return {
      loadMessages,
      publishQuestion,
      publishResponse,
      scrollChatView,
      textToSpeech,
    };
  })();

  /**
   * This IIFE as object is responsible for the Local Storage management.
   * @returns {Object} An object which manage the Local Storage.
   */
  const LocalStorage = (function LocalStorage() {
    const KEY = "ChatbotAppMessages";
    const user = Object.create(null);
    user.username = "";
    user.messages = [];

    /**
     * This function sets up the Local Storage state.
     */
    const setUp = () => {
      const inStorage = [];
      const currentItem = localStorage.getItem(KEY);
      if (currentItem) {
        inStorage.push(...JSON.parse(currentItem));
      }
      const newItem = inStorage.filter((item) => {
        if (item.username == user.username) {
          user.messages = item.messages;
        } else {
          return item;
        }
      });
      if (inStorage.length !== newItem.length) {
        localStorage.setItem(KEY, JSON.stringify(newItem));
      }
    };

    /**
     * This function appends a message to the message list.
     * @param {String} message A message sent by the user.
     */
    const append = (message) => user.messages.push(message);

    /**
     * This function updates the associated Local Storage data.
     */
    const post = () => {
      let item = localStorage.getItem(KEY) || [];
      item = JSON.parse(item);
      item.push(user);
      localStorage.setItem(KEY, JSON.stringify(item));
    };

    /**
     * This function maps the message list with the given function.
     * @param {Function} fun A function to be mapped into the message list.
     */
    const apply = (fun) => {
      user.messages.map((message) =>
        //fun(JSON.stringify({ username: user.username, message: message }))
        fun(message)
      );
      user.messages.length = 0;
    };

    /**
     * This function loads the current username into the Local Storage.
     * @param {String} username The current user username.
     */
    const load = (username) => {
      if (user.username != username) {
        user.username = username;
      }
      if (!localStorage.getItem(KEY)) {
        localStorage.setItem(KEY, JSON.stringify([]));
      }
    };

    return { append, apply, load, post, setUp };
  })();

  /**
   * This function handles the chatbot response.
   * @returns {Object} An object which manage the chatbot response.
   */
  function responseHandler() {
    let aError = false;
    const messages = [];
    let hasQueue = false;

    /**
     * This function releases a message in the queue to be shown in the chat.
     */
    const dispatch = () => {
      if (messages.length) {
        ChatHandler.publishResponse(messages.shift());
      } else {
        hasQueue = false;
      }
    };

    /**
     * This function appends a message in the message queue if it exists,
     * or it is directly released to the chat.
     * @param {String} message The message to be sent to the chat.
     */
    const append = (message) => {
      if (message !== SUCCESS_MESSAGE) {
        messages.push(message);
        if (!hasQueue) {
          hasQueue = true;
          dispatch();
        }
      }
    };

    /**
     * This function handles a message from the user whose sending
     * to the server failed.
     * @param {String} message The message to be sent to the chat.
     */
    const error = (message) => {
      if (!aError || message) {
        LocalStorage.setUp();
        if (message) {
          LocalStorage.append(message);
        }
        if (!aError) {
          LocalStorage.append(OFF_COMMAND);
          LocalStorage.append(BACK_COMMAND);
          ChatHandler.publishResponse(OFF_MESSAGE);
          aError = true;
        }
        LocalStorage.post();
      }
    };

    /**
     * This function handles the actions to be performed when the server
     * has recovered from a failed request attempt.
     */
    const recovered = () => {
      LocalStorage.setUp();
      LocalStorage.apply(request);
      aError = false;
    };

    return { append, dispatch, error, recovered };
  }

  /**
   * This IIFE as object is responsible for the worker management.
   * @returns {Object} An object which manage the worker.
   */
  const Manager = (function Manager() {
    const worker = (function () {
      const instance = new Worker("./service-worker.js");
      instance.onmessage = onMessage;
      return instance;
    })();

    /**
     * This function listens to the worker sent messages.
     * @param {Event} event An event received from the worker.
     */
    function onMessage(event) {
      if (event.data === "back") {
        server_on = true;
        ResponseHandler.recovered();
      }
    }

    /**
     * This function sends a message to the worker.
     * @param {state} state A state defined in the shared-data.js.
     */
    const postMessage = (state) => worker.postMessage(state);

    /**
     * This function terminates the worker.
     */
    const terminate = () => worker.terminate();

    return { postMessage, terminate };
  })();

  /**
   * This function make a request to the server.
   * @param {String} message The message to be sent to the server.
   */
  function request(message) {
    if (!server_on) {
      ResponseHandler.error(message);
    } else {
      const xhr =
        new XMLHttpRequest() || new ActiveXObject("Microsoft.XMLHTTP");

      /**
       * This function handles the success response of the sent request.
       */
      xhr.onload = () => {
        if (xhr.responseText) {
          try {
            console.log(xhr.responseText);
            ResponseHandler.append(JSON.parse(xhr.responseText).response);
          } catch (error) {
            ResponseHandler.append("Ei, atualize a página por favor");
          }
        }
      };

      /**
       * This function handles the failed response of the sent request.
       */
      xhr.onerror = () => {
        ResponseHandler.error(message);
        server_on = false;
        Manager.postMessage("off");
      };

      xhr.open("GET", generateURL(message));
      xhr.send();
    }
  }

  /**
   * This function handles the window click.
   * @param {Event} event An event triggered in the window.
   */
  window.onclick = (event) => {
    AccessibilityHandler.handleMenuOnClick(event.path);
  };

  /**
   * This function handles the window key down event.
   * @param {Event} event An event triggered in the window.
   */
  window.onkeydown = (event) => {
    if (event.key) {
      if (
        event.key === "Tab" &&
        (event.target === HTMLElements.chat ||
          event.target === HTMLElements.largerFontSize)
      ) {
        event.preventDefault();
      }
      AccessibilityHandler.improveKeyboardNavigation(
        document.activeElement,
        event.key.toUpperCase(),
        event.ctrlKey,
        event.shiftKey
      );
      AccessibilityHandler.handleMenuVisibility(
        event.key.toUpperCase(),
        event.target
      );
      AccessibilityHandler.handleMenuAccessKey(event.key);
    }
  };

  /**
   * This function handles the site set up.
   */
  window.onload = () => {
    ResponseHandler = responseHandler();
    const undefined = void 0;

    if (typeof Storage === undefined) {
      alert("Sorry, no Storage support!");
    }

    if (navigator.serviceWorker !== undefined) {
      navigator.serviceWorker
        .register("/service-worker.js")
        .catch(function (err) {
          console.log(err);
        });
    } else {
      console.log("Service Worker is not supported");
    }

    AccessibilityHandler.load(window.location.pathname, document.activeElement);

    if (window.location.pathname.includes("conversation")) {
      const xhr =
        new XMLHttpRequest() || new ActiveXObject("Microsoft.XMLHTTP");
      xhr.onload = () => {
        if (xhr.responseText) {
          LocalStorage.load(JSON.parse(xhr.responseText).username);
        }
      };

      xhr.open("GET", generateURL("test connection"));
      xhr.send();

      const sendMessageEvent = () => {
        const question = ChatHandler.publishQuestion();
        if (question) {
          request(question);
        }
      };
      HTMLElements.messageField.onkeydown = (event) => {
        if (event.key.toUpperCase() === "ENTER") {
          sendMessageEvent();
        }
      };
      if (HTMLElements.btnLoadMessages) {
        HTMLElements.btnLoadMessages.onclick = () => ChatHandler.loadMessages();
      }
      HTMLElements.btnSend.onclick = sendMessageEvent;
      HTMLElements.btnSkipMessages.onclick = () =>
        HTMLElements.messageField.focus();
      HTMLElements.footer.className = "mobile";

      if (HTMLElements.btnsVolumeUp) {
        [...HTMLElements.btnsVolumeUp].map((btn) => {
          btn.onclick = function () {
            return ChatHandler.textToSpeech(this);
          };
        });
      }

      ChatHandler.scrollChatView();
    } else {
      HTMLElements.footer.removeAttribute("class");
    }

    if (HTMLElements.btnLogout) {
      HTMLElements.btnLogout.onclick = () => {
        Manager.terminate();
      };
    }
  };
})(window, document);
