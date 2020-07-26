# -*- coding: utf-8 -*-
import os
from django.conf import settings
from programy.clients.embed.datafile import EmbeddedDataFileBot


class AimlChatbot(EmbeddedDataFileBot):
    """Definition of the AIML chatbot class.

    This class acts as the bridge between the server and the chatbot
    engine. It also provides methods to handle the client messages
    and retrieve the chatbot responses.
    It inherits from EmbeddedDataFileBot (class), the base to create
    the AIML chatbot class.

    Parameters
    ----------
    platform : str, optional
        The operating system that hosts the app, by default `windows`.
    chatbot : str, optional
        The chatbot filename, by default an empty string.
    """

    def __init__(self, platform="windows", chatbot=""):
        self.platform = platform
        self.chatbot = chatbot
        self.set_settings()
        super().__init__(files=self.files, logging_filename=self.logging)
        super().load_configuration(self.config)
        """
        list : Ultimate Default Category (UDC) responses.
            Default: 
                'Não entendi, podes me falar de outra forma?',
                'O que? kk.',
                'Como assim? kk.'
        """
        self.ultimate_default_category = [
            'Não entendi, podes me falar de outra forma?', 'O que? kk.', 'Como assim? kk.',
            'Então', 'O que mais tu gostarias de saber? kk', 'De nada', 'Obrigado!', 'Uhum',
            'Tudo bem', 'Tchau tchau', 'kk', 'kkk', 'kkkk', 'kkkkk', 'ha', 'haha', 'hahaha'
        ]
        self.previous_message = ''
        self.is_first_message = True

    def transform_message(self, message):
        """Changes the message if it includes gerunds.

        Parameters
        ----------
        message : str
            The message to be analysed.

        Returns
        -------
        str
            The message with or without alteration.
        """
        message_words = message.strip().split()
        transformed_words = []
        for word in message_words:
            word = word.lower()
            if len(word) > 5:
                if 'ando' in word:
                    word = word.replace('ando', 'ar')
                if 'endo' in word:
                    word = word.replace('endo', 'er')
            if 'indo' in word:
                word = word.replace('indo', 'ir')
            transformed_words.append(word)

        return ' '.join(transformed_words)

    def set_previous_message(self, previous_message=""):
        """Storing of the last message before retrieving a UDC response.

        If retrieving a UDC response, the previous message is stored and
        resend to the chatbot engine to maintain the close context
        (`that` tag).
        It also adds single spaces in the beginning and end of the message.

        Parameters
        ----------
        previous_message : str
            The message to be changed.
        """
        self.previous_message = " " + previous_message + " "

    def retrieve_message(self, message=""):
        """Retrieves a response message from the chatbot.

        Send the message to the chatbot engine; if it gets a non-UDC
        response, it is sent to the server.

        Hence, if the response is a UDC one, send a transformed message;
        if it gets a non-UDC response, it is sent to the server.

        Although, if the response still is an UDC one, store the
        message as a previous one, send it to the chatbot engine and
        send the UDC response do the server.

        Parameters
        ----------
        message : str
            The message sent from the server to the chatbot.

        Returns
        -------
        str
            The response message from the chatbot.
        """
        original = False
        message = message.replace("?", "").strip()

        transformed_message = self.transform_message(message)
        self.retrieved_message = self.ask_question(transformed_message)

        if self.retrieved_message in self.ultimate_default_category:

            self.retrieved_message = self.ask_question(message)

            if self.retrieved_message in self.ultimate_default_category:

                if self.is_first_message:
                    self.set_previous_message(message)

                self.ask_question(self.previous_message)

        else:
            self.set_previous_message(message)

        self.is_first_message = False
        return self.retrieved_message

    def set_settings(self):
        """
        Sets up the chatbot settings.
        """
        sep = os.sep
        # filepath = settings.BASE_DIR + "/chatbotapp/chatbot" + \
        #     ("" if not self.chatbot else "/" + self.chatbot)
        filepath = sep.join([settings.BASE_DIR, 'chatbotapp', 'chatbot'])
        if self.chatbot:
            filepath = sep.join([filepath, self.chatbot])
        self.files = {
            'aiml': [sep.join([filepath, 'storage', 'categories'])],
            'learnf': [sep.join([filepath, 'storage', 'learnf'])],
            'patterns': sep.join([filepath, 'storage', 'nodes', 'pattern_nodes.conf']),
            'templates': sep.join([filepath, 'storage', 'nodes', 'template_nodes.conf']),
            'properties': sep.join([filepath, 'storage', 'properties', 'properties.txt']),
            'defaults': sep.join([filepath, 'storage', 'properties', 'defaults.txt']),
            'sets': [sep.join([filepath, 'storage', 'sets'])],
            'maps': [sep.join([filepath, 'storage', 'maps'])],
            'rdfs': [sep.join([filepath, 'storage', 'rdfs'])],
            'denormals': sep.join([filepath, 'storage', 'lookups', 'denormal.txt']),
            'normals': sep.join([filepath, 'storage', 'lookups', 'normal.txt']),
            'genders': sep.join([filepath, 'storage', 'lookups', 'gender.txt']),
            'persons': sep.join([filepath, 'storage', 'lookups', 'person.txt']),
            'person2s': sep.join([filepath, 'storage', 'lookups', 'person2.txt']),
            'regexes': sep.join([filepath, 'storage', 'regex', 'regex-templates.txt']),
            'preprocessors': sep.join([filepath, 'storage', 'processing', 'preprocessors.conf']),
            'postprocessors': sep.join([filepath, 'storage', 'processing', 'postprocessors.conf'])
        }

        self.logging = sep.join(
            [filepath, 'config', self.platform, 'logging.yaml'])
        self.config = sep.join(
            [filepath, 'config', self.platform, 'config.yaml'])
