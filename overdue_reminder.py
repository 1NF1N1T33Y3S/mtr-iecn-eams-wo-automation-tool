import re
import pandas as pd
from typing import List

from constants.constants import eams_wo_id_pattern
from constants.email_configs import RECIPIENTS
from constants.file_paths import iecc_centralized_log_file_path
from constants.html_table_template import html_table_style, html_table_header, html_table_footer
from constants.mongo_db_configs import MONGO_DB_URL, MONGO_DB_NAME, MONGO_DB_COLLECTION
from controller.db_controller import GenericController
from enums.eams_status import EAMSStatus
from enums.iecc_console import IECCConsole
from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import crawler_helper
from helper.data_helper import DataHelper
from helper.email_manager import email_handler
from helper.logging_helper import logger
from model.eams_record import EAMSRecord
from model.reminder_row import ReminderRow
from repository.mongodb_manager import MongoCRUD
from utils.utils import map_to_eams_status, map_eams_status


def get_eams_wo_number(value: str) -> str:
    is_found = re.search(eams_wo_id_pattern, value)
    if is_found:
        return is_found.group()
    return "invalid"


def create_reminder_rows(r: List[EAMSRecord], df: pd.DataFrame) -> List[ReminderRow]:
    l = []
    for each in r:
        data = df[df["IECC Log"] == str(each.iecc_log_id)]
        l.append(ReminderRow(
            data['IECC Log'].values[0],
            data['Fault Report\nDate'].values[0],
            data["Equipment"].values[0],
            data['NR'].values[0],
            data['Reported Failure'].values[0],
            data['eams-wo'].values[0],
            data['overdue'].values[0]
        ))
    return l


def create_eams_records(df: pd.Series) -> List[EAMSRecord]:
    l = []
    for i, row in df.iterrows():
        iecc_log_id = row["IECC Log"]
        l.append(EAMSRecord(
            row['eams-wo'],
            iecc_log_id,
            IECCConsole.DUAT,
            EAMSStatus.OPENED,
            ""
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
    is_debug = False
    mongo_db_manager = MongoCRUD(
        MONGO_DB_URL,
        MONGO_DB_NAME,
        MONGO_DB_COLLECTION
    )
    db_controller = GenericController(mongo_db_manager)

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

    logger.info("Creating EAMS Records")
    eams_records = create_eams_records(valid_df)

    newly_created_eams_records: List[EAMSRecord] = []
    existing_eams_records: List[EAMSRecord] = []
    eams_records_to_email: List[EAMSRecord] = []

    logger.info("Looping over EAMS Records")
    for r in eams_records:
        r_in_db = db_controller.get(r.eams_wo)
        logger.info(f"{r_in_db=}")
        if r_in_db is None:
            logger.info("creating new EAMS record in db and appending it to array")
            db_controller.create(r)
            newly_created_eams_records.append(r)
        else:
            logger.info("updating local record status")
            status = r_in_db.status
            r.status = status
            existing_eams_records.append(r)

    logger.info("Checking the Newly Created EAMS Records with EAMS")
    # loop through the new eams records
    # check with EAMS system status
    (crawler_helper
     .set_chrome_helper(
        ChromeHelper()
        .set_debug(is_debug))
     .login()
     .go_to_wo_tracking_page())
    for r in newly_created_eams_records:
        raw_table_content = (
            crawler_helper
            .search_wo(r.eams_wo))
        status = map_eams_status(raw_table_content)
        logger.info(f"status mapped to {status=}")
        r.status = status
    crawler_helper.close()

    logger.info("Updating the status of the EAMS Records to DB after Checking with EAMS")
    for r in newly_created_eams_records:
        db_controller.update(r.eams_wo, {"status": r.status.value})

    logger.info("Filtering the local records with status == open")
    new_eams_records_with_open_status = [x for x in newly_created_eams_records if x.status == EAMSStatus.OPENED]
    existing_eams_records_with_open_status = [x for x in existing_eams_records if x.status == EAMSStatus.OPENED]
    eams_records_to_email = new_eams_records_with_open_status + existing_eams_records_with_open_status

    logger.info("Generating HTML string")
    reminder_rows = create_reminder_rows(eams_records_to_email, valid_df)
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
