from typing import Self

from constants.constants import url, email, username, password
from constants.xpaths import main_page_email_input_xpath, main_page_login_button_xpath, sso_lan_id_input_xpath, \
    sso_lan_pw_input_xpath, sso_login_button_xpath, eams_menu_button_xpath, eams_menu_search_xpath, \
    eams_workorder_tracking_button_xpath
from helper.chrome_helper import ChromeHelper


class CrawlerHelper:
    def __init__(self):
        self.chrome_helper = None
        self.timeout_in_sec = 3

    def set_chrome_helper(self, chrome_helper: ChromeHelper) -> Self:
        self.chrome_helper = chrome_helper
        return self

    def login(self) -> Self:
        (
            self.chrome_helper
            .go_to_page(url)
            .sleep(self.timeout_in_sec)
            .input_text(main_page_email_input_xpath, email, self.timeout_in_sec)
            .click_button(main_page_login_button_xpath, self.timeout_in_sec)
            .sleep(self.timeout_in_sec)
            .input_text(sso_lan_id_input_xpath, username, self.timeout_in_sec)
            .input_text(sso_lan_pw_input_xpath, password, self.timeout_in_sec)
            .click_button(sso_login_button_xpath, self.timeout_in_sec)
            .sleep(self.timeout_in_sec)
            .switch_iframe("manage-shell_Iframe")
        )
        return self

    def go_to_workorder_tracking_page(self) -> Self:
        (
            self.chrome_helper
            .click_button(eams_menu_button_xpath, self.timeout_in_sec)
            .input_text(eams_menu_search_xpath, "work", self.timeout_in_sec)
            .click_button(eams_workorder_tracking_button_xpath, self.timeout_in_sec)
            .sleep(self.timeout_in_sec)
        )
        return self
