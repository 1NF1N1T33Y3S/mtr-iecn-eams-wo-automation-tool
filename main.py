# 1.
from selenium.webdriver import Keys

from constants.constants import url, username, email, password
from constants.xpaths import main_page_login_button_xpath, sso_lan_id_input_xpath, \
    sso_lan_pw_input_xpath, sso_login_button_xpath, main_page_email_input_xpath, eams_workorder_tracking_button_xpath, \
    eams_menu_button_xpath, eams_menu_search_xpath, eams_wo_search_xpath, eams_wo_list_xpath
from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import CrawlerHelper

if __name__ == '__main__':
    print('hello world')
    test_value = "5000669050"
    chrome_helper = ChromeHelper()
    crawler_helper = CrawlerHelper()
    (
        crawler_helper
        .set_chrome_helper(chrome_helper)
        .login()
        .go_to_workorder_tracking_page()
    )
    crawler_helper.chrome_helper.input_text(eams_wo_search_xpath, test_value, 3)
    crawler_helper.chrome_helper.input_text(eams_wo_search_xpath, Keys.ENTER, 3)
    crawler_helper.chrome_helper.click_button(eams_wo_list_xpath, 3)
    crawler_helper.chrome_helper.sleep(10)

    print("done")
