# 1. login to microsoft page
main_page_email_input_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]"
main_page_login_button_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"

# 2. redirect to SSO login page
sso_lan_id_input_xpath = r"/html/body/div[9]/div/div/div[2]/div[2]/div[3]/div/form/div/div[1]/div/input"
sso_lan_pw_input_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input"
sso_login_button_xpath = r"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[5]/div/div/div/div/input"

# 3. workorder icon
eams_menu_button_xpath = r"/html/body/div[1]/header/button"
eams_menu_search_xpath = r"/html/body/div[1]/div[1]/div/div[1]/input"
eams_workorder_tracking_button_xpath = r"/html/body/div[1]/div[1]/div/div[2]/ul/li[2]/a"

# 4. track_order_list
eams_wo_search_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input"
eams_wo_list_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[3]/span"
eams_wo_result_table_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table"

# 4b. Work Order page
actual_start_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/table/tbody/tr[1]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[3]/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[2]/td/input"
actual_finish_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/table/tbody/tr[1]/td/div/table/tbody/tr[2]/td/table/tbody/tr/td[3]/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[4]/td/input"
status_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr[3]/td/input"
status_output_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[10]"

# 5. failure reporting
failure_reporting_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[1]/td/div/div[1]/div[3]/ul/li[6]/a"
select_failure_codes_button_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[10]/button"
failure_table_xpath = r"/html/body/form/div[2]/table[3]/tbody/tr/td[3]/table/tbody/tr[2]/th/table/tbody/tr/td/table[2]/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table"

# 6 change status button
change_status_menu_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[1]/div/table/tbody/tr/td/div/div[3]/div[2]/div[3]/div[2]/div/ul/li[4]/a"
drop_down_xpath = r"/html/body/form/div[2]/table[3]/tbody/tr/td[3]/table/tbody/tr[2]/th/table/tbody/tr/td/table[2]/tbody/tr/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[4]/td/input"
completed_xpath = r"/html/body/form/div[2]/table[1]/tbody/tr/td/div/div[1]/div/ul/li[3]/a"
confirm_ok_button_xpath = r"/html/body/form/div[2]/table[3]/tbody/tr/td[3]/table/tbody/tr[2]/th/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/button[2]"
confirm_cancel_button_xpath = r"/html/body/form/div[2]/table[3]/tbody/tr/td[3]/table/tbody/tr[2]/th/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/button[1]"
back_to_list_view_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[1]/div/table/tbody/tr/td/div/div[1]/div[1]/ul/li/a"

# universal save button
save_button_xpath = r"/html/body/form/div[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/div/table/tbody/tr/td/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td[4]/table/tbody/tr/td[2]/ul/li[2]/a"
