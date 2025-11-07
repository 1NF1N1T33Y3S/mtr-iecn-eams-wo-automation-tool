import time
from typing import Self

from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from constants.constants import default_download_path, chrome_driver_path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class ChromeHelper:
    def __init__(
            self):
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless=new")
        prefs = {
            "download.default_directory": default_download_path,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        service = Service(
            executable_path=chrome_driver_path
        )
        self.driver = Chrome(
            service=service,
            options=chrome_options
        )

    def close(
            self) -> Self:
        self.driver.close()
        return self

    def go_to_page(
            self,
            page_url: str
    ) -> Self:
        self.driver.get(page_url)
        return self

    def set_full_screen(
            self) -> Self:
        self.driver.maximize_window()
        return self

    def clear_text(
            self,
            x_path: str,
            timeout: int) -> Self:
        element = (
            WebDriverWait(
                self.driver,
                timeout)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     x_path)
                )
            )
        )
        backspaces = Keys.BACKSPACE * 20
        element.send_keys(backspaces)
        return self

    def input_text(
            self,
            x_path: str,
            text: str,
            timeout: int
    ) -> Self:
        (
            WebDriverWait(
                self.driver,
                timeout)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     x_path)
                )
            ).send_keys(text)
        )
        return self

    def select_dropdown_element(
            self,
            id: str,
            day: str
    ) -> Self:
        dropdown_element = self.driver.find_element(
            By.ID,
            id
        )
        select = Select(dropdown_element)
        select.select_by_visible_text(day)
        return self

    def click_button(
            self,
            x_path: str,
            timeout: int) -> Self:
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, x_path))
            )
            button.click()
        except Exception as e:
            print(f"encounter exception {e=}, continue to next step")
        return self

    def select_date_from_calender(
            self,
            x_path: str,
            timeout: int,
            date: str) -> Self:
        table_element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, x_path))
        )
        arrays = []
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                cell_class_name = cell.get_attribute("class")
                if cell_class_name != "rf-cal-week" and cell.accessible_name == date:
                    cell.click()
                    return self
                arrays.append(cell)
        return self

    def sleep(
            self,
            duration: int) -> Self:
        time.sleep(duration)
        return self

    def switch_iframe(
            self,
            frame_id: str
    ) -> Self:
        time.sleep(3)
        self.driver.switch_to.frame(frame_id)
        return self

    def refresh(
            self) -> Self:
        self.driver.refresh()
        return self
