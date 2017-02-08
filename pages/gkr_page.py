# coding=utf-8
from pages import BasePage
from pages.common_blocks import MainMenu, TopMenu, Dialogs


class GkrPage(BasePage):

    @property
    def top_menu(self):
        return TopMenu(self.config)

    @property
    def main_menu(self):
        return MainMenu(self.config)

    @property
    def dialogs(self):
        return Dialogs(self.config)
