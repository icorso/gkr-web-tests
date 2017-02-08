# coding=utf-8
from elements import BaseElement, By


class HistoryServices(BaseElement):

    class HistoryItem:
        header = None
        info = None
        time = None
        delete = None

    @property
    def elements(self):
        return self.element.find_elements(By.XPATH, ".//li[@class='history-services-list__unit text_type']")

    def get_history_by_id(self, header):
        for i in self.elements:
            header_ = i.find_element(By.XPATH, './/a')
            if header_.text == header:
                history_item = self.HistoryItem
                history_item.header = header_.text
                history_item.info = i.find_element(By.XPATH, ".//p[1]").text
                history_item.time = i.find_element(By.XPATH, ".//p[2]/b").text
                return history_item
