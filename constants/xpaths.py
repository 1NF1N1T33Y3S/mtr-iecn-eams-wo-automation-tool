# 1. login to microsoft page
main_page_email_input_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]"
main_page_login_button_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"

# 2. redirect to SSO login page
sso_lan_id_input_xpath = r"/html/body/div[9]/div/div/div[2]/div[2]/div[3]/div/form/div/div[1]/div/input"
sso_lan_pw_input_xpath = r"/html/body/div[9]/div/div/div[2]/div[2]/div[3]/div/form/div/div[2]/div/input"
sso_login_button_xpath = r"/html/body/div[9]/div/div/div[2]/div[2]/div[3]/div/form/div/div[3]/span"

# 3. workorder icon
eams_menu_button_xpath = r"/html/body/div[1]/header/button"
eams_menu_search_xpath = r"/html/body/div[1]/div[1]/div/div[1]/input"
eams_workorder_tracking_button_xpath = r"/html/body/div[1]/div[1]/div/div[2]/ul/li[2]/a"

# 4. track_order_list
eams_wo_search_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input"
eams_wo_list_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[3]/span"
