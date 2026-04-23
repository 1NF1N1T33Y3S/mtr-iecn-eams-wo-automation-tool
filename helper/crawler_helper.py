from typing import Self, Optional, List, Dict

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants.constants import url, email, username, password
from constants.xpaths import main_page_email_input_xpath, main_page_login_button_xpath, sso_lan_id_input_xpath, \
    sso_lan_pw_input_xpath, sso_login_button_xpath, eams_menu_button_xpath, eams_menu_search_xpath, \
    eams_workorder_tracking_button_xpath, eams_wo_search_xpath, eams_wo_list_xpath, actual_start_xpath, \
    actual_finish_xpath, save_button_xpath, failure_reporting_xpath, select_failure_codes_button_xpath, \
    failure_table_xpath, change_status_menu_xpath, drop_down_xpath, completed_xpath, confirm_ok_button_xpath, \
    back_to_list_view_xpath, confirm_cancel_button_xpath, status_xpath, status_output_xpath, eams_wo_result_table_xpath, \
    work_group_input_field_xpath, \
    status_input_field_xpath, refresh_report_button_xpath, download_button_xpath, work_type_input_field_xpath, \
    failure_component_input_xpath, failure_class_input_xpath, select_failure_codes_xpath, complete_button_xpath, \
    change_status_ok_button_xpath
from enums.eams_status import EAMSStatus
from helper.chrome_helper import ChromeHelper
from helper.failure_code_parser import FailureCodeParser
from helper.logging_helper import logger
from model.eams_wo import EAMSWorkOrder
from model.work_order import WorkOrder

import re
import logging
from typing import Optional

# Assuming logger is configured elsewhere in your project
logger = logging.getLogger(__name__)


def extract_reference_code(text: str,
                           prefix: str) -> Optional[str]:
    if not text or not prefix:
        logger.debug("Provided text or prefix is empty.")
        return None
    safe_prefix = re.escape(prefix)
    pattern = rf"{safe_prefix}-\d+"
    match = re.search(pattern, text)

    if match:
        extracted_value = match.group(0)
        logger.debug(f"Successfully extracted: '{extracted_value}' using prefix '{prefix}'")
        return extracted_value

    logger.debug(f"No reference found for prefix '{prefix}'.")
    return None


def extract_r_code(text: str) -> Optional[str]:
    if not text:
        return None
    pattern = r"R-[A-Za-z]+-\d+"

    match = re.search(pattern, text)

    if match:
        extracted_value = match.group(0)
        logger.debug(f"Successfully extracted: '{extracted_value}'")
        return extracted_value

    logger.debug("No 'R-' reference found in the text.")
    return None


class CrawlerHelper:
    def __init__(self):
        self.chrome_helper = None
        self.timeout_in_sec = 3

    def set_chrome_helper(self,
                          chrome_helper: ChromeHelper) -> Self:
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
        )
        return self

    def search_and_download_reports(self) -> Self:
        (
            self.chrome_helper
            .input_text(work_group_input_field_xpath, "MIMLLSNR", 3)
            .sleep(1)
            .input_text(work_type_input_field_xpath, "=CM-CR", 3)
            .sleep(1)
            .input_text(status_input_field_xpath, "=APPR,=INPRG", 3)
            .sleep(1)
            .click_button(refresh_report_button_xpath, 3)
            .sleep(3)
            .click_button(download_button_xpath, 3)
            .sleep(self.timeout_in_sec)
        )
        return self

    def search_wo(self,
                  wo: str) -> List[str]:
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

    @staticmethod
    def loop_through_table_and_select_value(table_elements: List[WebElement],
                                            matching_value: str) -> bool:
        if len(table_elements) == 0:
            return False
        for table_element in table_elements:
            if not table_element:
                logger.warning("No table element provided.")
                return False
            rows = table_element.find_elements(By.XPATH, ".//tr")
            for row_index, row in enumerate(rows):
                cells = row.find_elements(By.XPATH, ".//*[self::td or self::th]")
                for cell in cells:
                    cell_value = cell.text.strip()
                    logger.info(f"Row {row_index}: {cell_value}")
                    if matching_value == cell_value:
                        logger.info(f"match is found f{matching_value=} == {cell_value=}")
                        cell.click()
                        return True
        return False

    def select_table_element_by_xpath(self,
                                      element_id: str,
                                      timeout: int,
                                      matching_value: str
                                      ):
        logger.info("checking table element")
        div_element: WebElement = WebDriverWait(self.chrome_helper.driver, timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        tables = div_element.find_elements(By.TAG_NAME, "table")
        if self.loop_through_table_and_select_value(tables, matching_value):
            return

    def close_single_wo(self,
                        wo: EAMSWorkOrder) -> Self:
        logger.info(f"closing WO {wo.work_order_id=}")
        logger.info(f"{wo.__dict__=}")
        try:
            (self.chrome_helper
             .input_text(eams_wo_search_xpath, wo.work_order_id, 3)
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
                .click_button(failure_reporting_xpath, 3)
                .sleep(2)
                .click_button(select_failure_codes_xpath, 3)
                .sleep(2)
            )
            failure_code = extract_reference_code(wo.problem, prefix="P-IMD")
            component_code = extract_reference_code(wo.cause, prefix="C-COMP")
            remedy_code = extract_r_code(wo.remedy)
            self.select_table_element_by_xpath("wolistfailurecodes_bodydiv", 3, failure_code)
            self.chrome_helper.sleep(2)
            self.select_table_element_by_xpath("wolistfailurecodes_bodydiv", 3, component_code)
            self.chrome_helper.sleep(2)
            self.select_table_element_by_xpath("wolistfailurecodes_bodydiv", 3, remedy_code)
            self.chrome_helper.sleep(2)
            self.chrome_helper.click_button(change_status_menu_xpath, 3)
            self.chrome_helper.sleep(1)
            self.chrome_helper.click_button(drop_down_xpath, 3)
            self.chrome_helper.sleep(1)
            self.chrome_helper.click_button(complete_button_xpath, 3)
            self.chrome_helper.sleep(1)
            self.chrome_helper.click_button(change_status_ok_button_xpath, 3)

            logger.info(f"{wo.work_order_id} close successfully")
            wo.programmatic_status = "DONE"
        except Exception as e:
            logger.error(f"{wo.work_order_id} close failed")
            error_message = f"error in closing workorder {str(e)}"
            wo.programmatic_status = "NOT DONE"
            wo.execution_error_message = error_message
        finally:
            self.go_to_wo_tracking_page()
        return self


crawler_helper = CrawlerHelper()
