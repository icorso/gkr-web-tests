from elements import BaseElement, By


class AdminNewsTable(BaseElement):
    id = None
    title = None
    desc = None
    type = None
    date = None
    text = None

    def rows(self):
        return self.element.find_elements(By.XPATH, ".//tr")

    def get_row_by_news_id(self, news_id):
        for row in self.rows():
            if row.find_element(By.XPATH, './td[1]').text == str(news_id):
                self.id = row.find_element(By.XPATH, './td[1]').text
                self.title = row.find_element(By.XPATH, './td[3]/p[1]').text
                self.desc = row.find_element(By.XPATH, './td[3]/p[2]').text
                self.type = row.find_element(By.XPATH, './td[4]/p[1]').text
                self.date = row.find_element(By.XPATH, './td[4]/p[2]').text
                self.text = row.find_element(By.XPATH, '.').text
                self.element = row.find_element(By.XPATH, '.')
                return self
        raise Exception("Не найдена строка с news_id = " + str(news_id))

    def get_row_by_title(self, title):
        for row in self.rows():
            if row.find_element(By.XPATH, './td[3]/p[1]').text == title:
                self.id = row.find_element(By.XPATH, './td[1]').text
                self.title = row.find_element(By.XPATH, './td[3]/p[1]').text
                self.desc = row.find_element(By.XPATH, './td[3]/p[2]').text
                self.type = row.find_element(By.XPATH, './td[4]/p[1]').text
                self.date = row.find_element(By.XPATH, './td[4]/p[2]').text
                self.text = row.find_element(By.XPATH, '.').text
                self.element = row.find_element(By.XPATH, '.')
                return self
        raise Exception("Не найдена строка с title = " + title)
