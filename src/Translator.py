import os
import yaml

from util.String_Util import StringUtil


class Translator:
    def __init__(self):
        self.language = "vi"
        self.load_path = "src/locales/"
        self.translations = self.load_translations()

    def load_translations(self):
        locale_path = os.path.join(self.load_path, f"{self.language}.yml")
        absolute_path = os.path.abspath(locale_path)
        if os.path.exists(absolute_path):
            with open(absolute_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        else:
            print(f"Translation file {absolute_path} does not exist.")
            return {}

    def _(self, text):
        return self.get_translation(text)

    def menu_t(self, text):
        return StringUtil.first_letter_uppercase(self.get_translation(f"menu.{text}"))

    def object_t(self, text):
        return StringUtil.first_letter_uppercase(self.get_translation(f"object.{text}"))

    def action_t(self, text):
        return StringUtil.first_letter_uppercase(self.get_translation(f"action.{text}"))

    def button_t(self, text):
        return StringUtil.first_letter_uppercase(self.get_translation(f"button.{text}"))

    def message_t(self, text):
        return self.get_translation(f"message.{text}")

    def message(self, text: str):
        arr = text.split(".")
        obj = StringUtil.first_letter_uppercase(
            self.get_translation(f"object.{arr[1]}")
        )
        mes = self.message_t(arr[0])
        return obj + " " + mes

    def get_translation(self, text):
        keys = text.split(".")
        translation = self.translations
        for key in keys:
            translation = translation.get(key)
            if translation is None:
                return f"Missing translation for {self.language}.{text}"
        return translation
