from typing import Self, Optional, List

from selenium.common import TimeoutException
from selenium.webdriver import Keys

from constants.constants import url, email, username, password
from constants.xpaths import main_page_email_input_xpath, main_page_login_button_xpath, sso_lan_id_input_xpath, \
    sso_lan_pw_input_xpath, sso_login_button_xpath, eams_menu_button_xpath, eams_menu_search_xpath, \
    eams_workorder_tracking_button_xpath, eams_wo_search_xpath, eams_wo_list_xpath, actual_start_xpath, \
    actual_finish_xpath, save_button_xpath, failure_reporting_xpath, select_failure_codes_button_xpath, \
    failure_table_xpath, change_status_menu_xpath, drop_down_xpath, completed_xpath, confirm_ok_button_xpath, \
    back_to_list_view_xpath, confirm_cancel_button_xpath, status_xpath, status_output_xpath, eams_wo_result_table_xpath
from enums.eams_status import EAMSStatus
from helper.chrome_helper import ChromeHelper
from helper.logging_helper import logger
from model.work_order import WorkOrder


class CrawlerHelper:
    def __init__(self):
        self.chrome_helper = None
        self.timeout_in_sec = 3

    def set_chrome_helper(self, chrome_helper: ChromeHelper) -> Self:
        self.chrome_helper = chrome_helper
        return self

    def close(self):
        self.chrome_helper.close()

    def login(self) -> Self:
        (
            self.chrome_helper
            .go_to_page(url)
            .sleep(self.timeout_in_sec)
            .input_text(main_page_email_input_xpath, email, self.timeout_in_sec)
            .click_button(main_page_login_button_xpath, self.timeout_in_sec)
            # .sleep(self.timeout_in_sec)
            # .input_text(sso_lan_id_input_xpath, username, self.timeout_in_sec)
            .sleep(self.timeout_in_sec)
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

    def search_wo(self, wo: str) -> List[str]:
        logger.info(f"checking with wo {wo=}")
        timeout_in_sec = 3
        try:
            (self.chrome_helper
             .input_text(
                eams_wo_search_xpath,
                wo,
                timeout_in_sec)
             .input_text(eams_wo_search_xpath,
                         Keys.ENTER,
                         timeout_in_sec)
             .sleep(timeout_in_sec))
            values = self.chrome_helper.select_table_element(
                eams_wo_result_table_xpath,
                3)
        except TimeoutException:
            logger.error(f"{wo=} not found in EAMS")
            return []
        logger.info(f"{values=}")
        return values

    def close_single_wo(self, wo: WorkOrder) -> Self:
        logger.info(f"closing WO {wo.wo_id=}")
        logger.info(f"{wo.__dict__}")
        try:
            (self.chrome_helper
             .input_text(eams_wo_search_xpath, wo.wo_id, 3)
             .input_text(eams_wo_search_xpath, Keys.ENTER, 3)
             .sleep(3)
             .click_button(eams_wo_list_xpath, 3)
             .sleep(3))
            value = self.chrome_helper.read_value(status_xpath, 3)
            logger.info(f"{value=}")
            if value in ["COMP", "CANCEL"]:
                error_message = f"{value=} is either already Completed or Cancelled"
                logger.info(error_message)
                raise Exception(error_message)
            (
                self.chrome_helper
                .click_button(change_status_menu_xpath, 3)
                .sleep(3)
                .click_button(confirm_cancel_button_xpath, 3)  # change back to OK
                .click_button(back_to_list_view_xpath, 3)
                .sleep(3)
            )
            logger.info(f"{wo.wo_id} close successfully")
            wo.job_status = "DONE"
        except Exception as e:
            logger.error(f"{wo.wo_id} close failed")
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


crawler_helper = CrawlerHelper()
