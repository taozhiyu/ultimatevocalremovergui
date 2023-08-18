import json
import os


class Translator:
    DEFAULT_LANGUAGE = "en"
    AVAILABLE_LANGUAGES = {
        "en": "English",
        "zh_CN": "简体中文",
    }

    def __init__(self, lang):
        self.language = lang
        self.translations = self.load_translations()

    def load_translations(self):
        translations = {}
        for lang in self.AVAILABLE_LANGUAGES:
            filename = f"{lang}.json"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as file:
                    translations[lang] = json.load(file)
        return translations

    def translate(self, key, *args, force=False):
        keys = key.split(".")
        current_translation = self.translations.get(self.language if not force else "en", {})
        for k in keys:
            if k not in current_translation:
                if isinstance(current_translation, list) and k.isdigit() and 0 <= int(k) < len(current_translation):
                    current_translation = current_translation[int(k)]
                    continue
                if force:
                    return key
                return self.translate(key, *args, force=True)
            current_translation = current_translation.get(k, {})
        if isinstance(current_translation, str) and args:
            try:
                current_translation = current_translation.format(*list(args))
            except IndexError:
                """
                    When the number of arguments is less than the number of placeholders in the string,
                    return the original string.
                """
                pass
        return current_translation

    def set_language(self, lang):
        if lang not in self.AVAILABLE_LANGUAGES:
            if lang not in self.AVAILABLE_LANGUAGES.values():
                lang = self.DEFAULT_LANGUAGE
            else:
                lang = list(self.AVAILABLE_LANGUAGES.keys())[list(self.AVAILABLE_LANGUAGES.values()).index(lang)]
        self.language = lang

    def get_language_list(self):
        return self.AVAILABLE_LANGUAGES.values()

    def get_language(self):
        return self.language
