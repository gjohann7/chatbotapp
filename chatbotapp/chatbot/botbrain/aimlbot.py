# -*- coding: utf-8 -*-
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
            'Não entendi, podes me falar de outra forma?', 'O que? kk.', 'Como assim? kk.']
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
            if len(word) > 5:
                if 'ando' in word:
                    word = word.replace('ando', 'ar')
                if 'endo' in word:
                    word = word.replace('endo', 'er')
            if 'indo' in word:
                word = word.replace('indo', 'ir')
            transformed_words.append(word)

        return ' '+' '.join(transformed_words)+' '

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
        message = " "+message+" "
        self.retrieved_message = self.ask_question(message)

        if self.retrieved_message in self.ultimate_default_category:

            transformed_message = self.transform_message(message)
            self.retrieved_message = self.ask_question(transformed_message)

            if self.retrieved_message in self.ultimate_default_category:

                if self.is_first_message:
                    self.set_previous_message(message)

                self.ask_question(self.previous_message)

            else:
                self.set_previous_message(transformed_message)
        else:
            self.set_previous_message(message)

        self.is_first_message = False
        return self.retrieved_message

    def set_settings(self):
        """
        Sets up the chatbot settings.
        """
        filepath = settings.BASE_DIR + "\\chatbotapp\\chatbot" + \
            ("" if not self.chatbot else "\\" + self.chatbot)
        self.files = {
            'aiml': [filepath + '\\storage\\categories'],
            'learnf': [filepath + '\\storage\\learnf'],
            'patterns': filepath + '\\storage\\nodes\\pattern_nodes.conf',
            'templates': filepath + '\\storage\\nodes\\template_nodes.conf',
            'properties': filepath + '\\storage\\properties\\properties.txt',
            'defaults': filepath + '\\storage\\properties\\defaults.txt',
            'sets': [filepath + '\\storage\\sets'],
            'maps': [filepath + '\\storage\\maps'],
            'rdfs': [filepath + '\\storage\\rdfs'],
            'denormals': filepath + '\\storage\\lookups\\denormal.txt',
            'normals': filepath + '\\storage\\lookups\\normal.txt',
            'genders': filepath + '\\storage\\lookups\\gender.txt',
            'persons': filepath + '\\storage\\lookups\\person.txt',
            'person2s': filepath + '\\storage\\lookups\\person2.txt',
            'regexes': filepath + '\\storage\\regex\\regex-templates.txt',
            'preprocessors': filepath + '\\storage\\processing\\preprocessors.conf',
            'postprocessors': filepath + '\\storage\\processing\\postprocessors.conf'
        }

        self.logging = str(filepath + "\\config\\" +
                           self.platform + "\\logging.yaml")
        self.config = str(filepath + "\\config\\" +
                          self.platform + "\\config.yaml")
