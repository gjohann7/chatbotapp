import os
from programy.clients.embed.datafile import EmbeddedDataFileBot
from pathlib import Path


class AimlChatbot(EmbeddedDataFileBot):
    def __init__(self):
        self.set_settings()
        super().__init__(files=self.files, logging_filename=self.logging)
        super().load_configuration(self.config)
        self.ultimate_default_category = [
            'Não entendi, podes me falar de outra forma?', 'O que? kk.', 'Como assim? kk.']
        self.previous_message = ''
        self.is_first_message = True

    def transform_message(self, message):
        message_words = message.split()
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
        self.previous_message = " " + previous_message + " "

    def retrieve_message(self, message=""):
        original = False
        message = message.replace("?", "").strip()

        transformed_message = self.transform_message(message)
        self.retrieved_message = self.ask_question(transformed_message)

        if self.retrieved_message in self.ultimate_default_category:

            if self.is_first_message:
                self.set_previous_message(message)

            self.ask_question(self.previous_message)

        else:
            self.set_previous_message(transformed_message)

        self.is_first_message = False
        return self.retrieved_message

    def render_message_swap(self, message=""):
        self.retrieve_message(message)

        print('Estudante: "' + message + '"\nChatbot: "' +
              str(self.retrieved_message) + '"')

        return {"sent": message, "retrieved": self.retrieved_message}

    def set_settings(self):
        sep = os.sep
        BASE_DIR = str(Path().absolute())
        filepath = sep.join(
            [BASE_DIR, 'botbrain'])
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
            [filepath, 'config', 'windows', 'logging.yaml'])
        self.config = sep.join([filepath, 'config', 'windows', 'config.yaml'])
