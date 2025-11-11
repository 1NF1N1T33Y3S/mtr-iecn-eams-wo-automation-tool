import re

import pandas as pd
from typing import Self, List

from constants.constants import eams_wo_id_pattern
from constants.file_paths import iecc_centralized_log_file_path
from model.work_order import WorkOrder


class DataHelper:
    def __init__(self):
        self.df = None
        self.file_path: str = ""
        self.sheet_name: str = ""

    def set_file_path(self, file_path: str) -> Self:
        self.file_path = file_path
        return self

    def set_sheet_name(self, sheet_name: str) -> Self:
        self.sheet_name = sheet_name
        return self

    def read_excel(self) -> pd.DataFrame:
        self.df = pd.read_excel(
            self.file_path,
            sheet_name="2025",
            dtype={"IECC Log": str, "EAMS WO Completed": str}
        )
        return self.df


# df_with_completed_wo = self.filter_completed_wo()

# def filter_completed_wo(self) -> pd.DataFrame:
#     return self._filter_no_nan("Finish Work\nTime")

def get_fault_cleared_df(df: pd.DataFrame) -> pd.DataFrame:
    return filter_df(df, "Fault Cleared", "Y")


def get_eams_incomplete_df(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["EAMS WO Completed"] != "DONE"]


def filter_df(df: pd.DataFrame, column_name: str, value: str) -> pd.DataFrame:
    return df[df[column_name] == value]


def filter_nan_df(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    return df[df[column_name].notna()]


def filter_valid_eams_wo(df: pd.DataFrame) -> pd.DataFrame:
    pass


def parse_work_order(df: pd.DataFrame) -> List[WorkOrder]:
    work_orders: List[WorkOrder] = []
    problems = []
    for index, each in df.iterrows():
        uuid = each["IECC Log"]
        wo_id = str(each["Work Order Number"])
        problem_code = each["Problem Code"]
        cause_code = each["Cause Code"]
        remedy_code = each["Remedy Code"]
        component_code_1 = each["Component Code 1"]
        component_code_2 = each["Component Code 2"]
        actual_work_date = each["Site Arrival\nStart Work\nDate"]
        actual_work_time = each["Site Arrival\nStart Work\nTime"]
        finish_work_date = each["Finish Work\nDate"]
        finish_work_time = each["Finish Work\nTime"]
        possible_wo_ids = wo_id.split("\n")
        formatted_date = "Error Date"
        formatted_time = "Error Time"
        formatted_actual_finish_datetime = "Error Datetime"
        formatted_start_date = "Error Date"
        formatted_start_time = "Error Time"
        formatted_actual_start_datetime = "Error Datetime"

        try:
            date = finish_work_date.date()
            formatted_date = date.strftime('%d/%m/%Y')
            formatted_time = finish_work_time.strftime("%H:%M")
            formatted_actual_finish_datetime = f"{formatted_date} {formatted_time}"

            d = actual_work_date.date()
            formatted_start_date = d.strftime('%d/%m/%Y')
            formatted_start_time = actual_work_time.strftime("%H:%M")
            formatted_actual_start_datetime = f"{formatted_start_date} {formatted_start_time}"
        except AttributeError as e:
            problems.append(
                {"uuid": uuid, "error": f"Incorrect Datetime format: {finish_work_date} or {finish_work_time}"})

        for each_id in possible_wo_ids:
            each_id_splits = each_id.split(" ")
            for each_id_split in each_id_splits:
                clean_id = each_id_split.rstrip().lstrip()
                match = re.match(eams_wo_id_pattern, clean_id)
                if match:
                    work_order = WorkOrder(
                        id=uuid,
                        wo_id=clean_id,
                        start_work_date=formatted_start_date,
                        start_work_time=formatted_start_time,
                        finish_work_date=formatted_date,
                        finish_work_time=formatted_time,
                        problem_code=problem_code,
                        cause_code=cause_code,
                        remedy_code=remedy_code,
                        component_code_1=component_code_1,
                        component_code_2=component_code_2,
                        actual_start_date=formatted_actual_start_datetime,
                        actual_finish_date=formatted_actual_finish_datetime
                    )
                    work_orders.append(work_order)
    for p in problems:
        for wo in work_orders:
            if wo.id == p["uuid"]:
                print("found")
                wo.execution_error_message = p["error"]
    return work_orders


if __name__ == '__main__':
    df = pd.read_excel(iecc_centralized_log_file_path, sheet_name="2025")
