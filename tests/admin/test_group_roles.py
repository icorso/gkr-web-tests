# coding=utf-8

import allure
import pytest

from constants.urls import Urls
from data.users import ADMIN
from pages.admin.group_roles import GroupRolesPage
from steps.user_steps import GkrUserSteps


@pytest.mark.usefixtures('config')
@allure.feature('Administration')
@allure.story('Group Roles')
class TestGroupRoles:

    def test_group_roles_count(self, config):

        user = GkrUserSteps(config)
        group_roles_page = GroupRolesPage(config)
        user.login(ADMIN.login, ADMIN.password)
        user.waits_for_ajax()

        user.opens(Urls.ADMIN_GROUP_ROLES.url)
        user.should_see_element(group_roles_page)
        user.chooses_from_select(group_roles_page.GROUP_LIST, 'SUPPORT')
        user.waits_for_ajax()
        support_count = len(group_roles_page.ROLE_LIST.elements)
        user.should_see_element_contains_text(group_roles_page.ROLE_LIST_COUNT, 'Роли:(' + str(support_count) + ')')
