import datetime
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class EAMSWorkOrder:
    work_order_id: int
    description: str
    work_group: str
    work_type: str
    asset: str
    asset_classification: str
    location: str
    status: str
    job_plan: str
    target_start_datetime: Union[datetime.datetime, str]
    target_finish_datetime: Union[datetime.datetime, str]
    programmatic_status: Optional[str] = None
    line: Optional[str] = None
    failure_class: Optional[str] = None
    problem: Optional[str] = None
    cause: Optional[str] = None
    remedy: Optional[str] = None
    actual_start_datetime: Optional[Union[datetime.datetime, str]] = None
    actual_finish_datetime: Optional[Union[datetime.datetime, str]] = None

    def determine_line(self):
        line_mapping = {
            "AEL": "AELnTCL",
            "TCL": "AELnTCL",
            "DRL": "DRL"
        }
        line = self.asset.split("-")[0]
        return line_mapping.get(line, line)

    def to_list_data(self):
        return [
            self.work_order_id,
            self.description,
            self.work_group,
            self.work_type,
            self.asset,
            self.asset_classification,
            self.location,
            self.status,
            self.job_plan,
            self.target_start_datetime,
            self.target_finish_datetime,
            self.actual_start_datetime,
            self.actual_finish_datetime,
            self.determine_line()
        ]
