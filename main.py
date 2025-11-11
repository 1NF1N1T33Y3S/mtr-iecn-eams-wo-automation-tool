# 1.
import os
from constants.constants import url, username, email, password
from constants.file_paths import iecc_centralized_log_file_path
from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import CrawlerHelper
from helper.data_helper import DataHelper, parse_work_order, filter_df, get_fault_cleared_df, filter_nan_df, \
    get_eams_incomplete_df
from helper.excel_helper import ExcelHelper

if __name__ == '__main__':
    print('hello world')
    # close_all_excel_instances()
    os.system("taskkill /f /im excel.exe")
    test_value = "5000669050"
    test_value = "5000682265"
    chrome_helper = ChromeHelper()
    crawler_helper = CrawlerHelper()
    (
        crawler_helper
        .set_chrome_helper(chrome_helper)
        .login()
        .go_to_wo_tracking_page()
    )
    data_helper = DataHelper()
    df = (
        data_helper
        .set_file_path(iecc_centralized_log_file_path)
        .set_sheet_name("2025")
        .read_excel()
    )
    max_rows = len(df)

    excel_helper = ExcelHelper()
    (
        excel_helper
        .set_file_path(iecc_centralized_log_file_path)
        .set_sheet_name("2025")
        .set_max_row(max_rows)
        .read_excel()
    )

    print(f"filtering on the data")
    fault_cleared_df = get_fault_cleared_df(df)
    fault_cleared_n_eams_completed_df = get_eams_incomplete_df(fault_cleared_df)
    fault_cleared_n_eams_completed_n_valid_wo_df = filter_nan_df(fault_cleared_n_eams_completed_df, "Work Order Number")

    work_orders = parse_work_order(fault_cleared_n_eams_completed_n_valid_wo_df)

    print("writing the result into xlsx ")
    clean_wo = [order for order in work_orders if order.execution_error_message is None]
    problem_wo = [order for order in work_orders if order.execution_error_message is not None]

    for wo in clean_wo:
        crawler_helper.close_single_wo(wo)
    crawler_helper.chrome_helper.driver.quit()

    for wo in clean_wo:
        print(f"{wo.id=} {wo.wo_id=} {wo.actual_start_date=} {wo.actual_finish_date=}")
        row = excel_helper.get_row_by_column(0, wo.id)
        excel_helper.write("EAMS WO Completed", row, wo.job_status)
        excel_helper.write("EAMS WO Failure Message", row, wo.execution_error_message)

    for wo in problem_wo:
        print(f"{wo.id=} {wo.wo_id=} {wo.actual_start_date=} {wo.actual_finish_date=}")
        row = excel_helper.get_row_by_column(0, wo.id)
        excel_helper.write("EAMS WO Completed", row, "NOT DONE")
        excel_helper.write("EAMS WO Failure Message", row, wo.execution_error_message)

    excel_helper.save()
    # print(f"write completed")
