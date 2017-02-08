# coding=utf-8
from elements import BaseElement, By


class Dialog(BaseElement):

    @property
    def title(self):
        return self.element.find_element(By.XPATH, "//*[@class='ui-dialog-title']")

    @property
    def content(self):
        return self.element.find_element(By.XPATH, "//*[contains(@class,'dialog-content')]")

    @property
    def close(self):
        return self.element.find_element(By.XPATH, ".//button[contains(@class,'close')]/span[1]")

    @property
    def buttons_set(self):
        return self.element.find_elements(By.XPATH, ".//button[not(contains(@class,'close'))]")

    def get_button_by_text(self, text):
        for b in self.buttons_set:
            if b.text.lower() == text.lower():
                return b
