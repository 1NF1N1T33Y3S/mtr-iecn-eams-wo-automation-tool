import re
import pandas as pd
from typing import List

from constants.constants import eams_wo_id_pattern
from constants.email_configs import RECIPIENTS
from constants.file_paths import iecc_centralized_log_file_path
from constants.html_table_template import html_table_style, html_table_header, html_table_footer
from helper.data_helper import DataHelper
from helper.email_manager import email_handler
from helper.logging_helper import logger
from model.reminder_row import ReminderRow


def get_eams_wo_number(value: str) -> str:
    is_found = re.search(eams_wo_id_pattern, value)
    if is_found:
        return is_found.group()
    return "invalid"


def create_reminder_rows(df: pd.Series) -> List[ReminderRow]:
    l = []
    for i, row in df.iterrows():
        l.append(ReminderRow(
            row['IECC Log'],
            row['fault-report-date'],
            row["Equipment"],
            row['NR'],
            row['Reported Failure'],
            row['eams-wo'],
            row['overdue']
        ))
    return l


def create_email_rows(reminders: List[ReminderRow]) -> str:
    html = ''
    for e in reminders:
        r = f'''<tr><td>{e.id}</td>
                <td>{e.fault_report_date}</td>
                <td>{e.equipment}</td>
                <td>{e.fault_category}</td>
                <td>{e.fault_description}</td>
                <td>{e.eams_wo}</td>
                <td>{e.overdue_days}</td></tr>'''
        html += r
    return html


def create_email_table(reminders: List[ReminderRow]) -> str:
    email_rows = create_email_rows(reminders)
    return html_table_style + html_table_header + email_rows + html_table_footer


def main():
    data_helper = DataHelper()
    df = (
        data_helper
        .set_file_path(iecc_centralized_log_file_path)
        .set_sheet_name("2025")
        .read_excel()
    )
    logger.info(f"Filtering Datasets")
    df_length = len(df)
    logger.info("removing all empty rows in the excel")
    df = df.dropna(how="all")
    filtered_df_length = len(df)
    logger.info(f"removed {df_length - filtered_df_length} empty rows in the excel")
    df = df.dropna(subset=['Work Order Number'])
    valid_wo_df_length = len(df)
    logger.info(f"removed {filtered_df_length - valid_wo_df_length} null work order number rows in the excel")

    logger.info(f"Transforming Datasets")
    df["fault-cleared"] = df["Fault Cleared"].str.rstrip().str.lstrip().str.lower().astype(str)
    df['fault-report-date'] = pd.to_datetime(df['Fault Report\nDate'])
    df['overdue'] = (pd.Timestamp.today() - df['fault-report-date']).dt.days.astype(int)
    df['wo'] = df["Work Order Number"].str.lstrip().str.rstrip().str.lower().astype(str)
    df["eams-wo"] = df["wo"].apply(get_eams_wo_number).astype(str)

    logger.info("Readying Data")
    valid_df = df[df["fault-cleared"] != "y"]
    valid_df = valid_df[valid_df["overdue"] > 6]
    valid_df = valid_df[valid_df["eams-wo"] != "invalid"]

    logger.info("Filling nan Data with N/A")
    valid_df["NR"] = valid_df["NR"].fillna("N/A")
    valid_df["Reported Failure"] = valid_df["Reported Failure"].fillna("N/A")
    valid_df["Equipment"] = valid_df["Equipment"].fillna("N/A")

    logger.info("Generating HTML string")
    reminder_rows = create_reminder_rows(valid_df[:10])
    html = create_email_table(reminder_rows)

    logger.info("Sending Email")
    email_handler.send_email(
        RECIPIENTS,
        "[Testing Email for CMCR Near Overdue WO Reminder]",
        f'''
            Dear Colleagues,
                Please check the table below:
                {html}
        ''',
    )
    logger.info("done")


if __name__ == "__main__":
    main()
