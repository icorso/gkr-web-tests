# coding=utf-8

from steps.http_steps import GkrHttpSteps


class TestAuth:

    def test_renew(self, config):
        http_user = GkrHttpSteps(config)
        http_user.renew_queue()
