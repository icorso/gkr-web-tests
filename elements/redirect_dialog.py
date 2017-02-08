# coding=utf-8
from elements import BaseElement, By


class RedirectDialog(BaseElement):

    @property
    def title(self):
        return self.element.find_element(By.XPATH, ".//h6")

    @property
    def content(self):
        return self.element.find_element(By.XPATH, ".//div[@class='modal-body_type1']")

    @property
    def close(self):
        return self.element.find_element(By.XPATH, ".//a")
