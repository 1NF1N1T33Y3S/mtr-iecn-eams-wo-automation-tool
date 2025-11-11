from typing import Self
from selenium.webdriver import Keys

from constants.constants import url, email, username, password
from constants.xpaths import main_page_email_input_xpath, main_page_login_button_xpath, sso_lan_id_input_xpath, \
    sso_lan_pw_input_xpath, sso_login_button_xpath, eams_menu_button_xpath, eams_menu_search_xpath, \
    eams_workorder_tracking_button_xpath, eams_wo_search_xpath, eams_wo_list_xpath, actual_start_xpath, \
    actual_finish_xpath, save_button_xpath, failure_reporting_xpath, select_failure_codes_button_xpath, \
    failure_table_xpath, change_status_menu_xpath, drop_down_xpath, completed_xpath, confirm_ok_button_xpath, \
    back_to_list_view_xpath, confirm_cancel_button_xpath, status_xpath
from helper.chrome_helper import ChromeHelper
from model.work_order import WorkOrder


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

    def go_to_wo_tracking_page(self) -> Self:
        (
            self.chrome_helper
            .click_button(eams_menu_button_xpath, self.timeout_in_sec)
            .input_text(eams_menu_search_xpath, "work", self.timeout_in_sec)
            .click_button(eams_workorder_tracking_button_xpath, self.timeout_in_sec)
            .sleep(self.timeout_in_sec)
        )
        return self

    def close_single_wo(self, wo: WorkOrder) -> Self:
        print(
            f"closing {wo.id} {wo.wo_id} {wo.finish_work_date} {wo.finish_work_time} {wo.problem_code} {wo.cause_code} {wo.remedy_code}")
        try:
            (self.chrome_helper
             .input_text(eams_wo_search_xpath, wo.wo_id, 3)
             .input_text(eams_wo_search_xpath, Keys.ENTER, 3)
             .sleep(3)
             .click_button(eams_wo_list_xpath, 3)
             .sleep(3))
            value = self.chrome_helper.read_value(status_xpath, 3)
            if value in ["COMP", "CANCEL"]:
                raise Exception
            print(f"{value=}")
            (
                self.chrome_helper
                .click_button(change_status_menu_xpath, 3)
                .sleep(3)
                .click_button(confirm_cancel_button_xpath, 3)  # change back to OK
                .click_button(back_to_list_view_xpath, 3)
                .sleep(3)
            )
            wo.job_status = "DONE"
        except Exception as e:
            error_message = f"error in closing workorder {str(e)}"
            wo.job_status = "NOT DONE"
            wo.execution_error_message = error_message
            self.go_to_wo_tracking_page()
            # self.chrome_helper.driver.quit()
            # chrome_helper = ChromeHelper()
            # (self
            #  .set_chrome_helper(chrome_helper)
            #  .login()
            #  .go_to_wo_tracking_page()
            #  )
        return self
