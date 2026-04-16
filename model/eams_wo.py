import datetime
from dataclasses import dataclass
from typing import Optional


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
    target_start_datetime: datetime.datetime
    target_finish_datetime: datetime.datetime
    actual_start_datetime: Optional[datetime.datetime] = None
    actual_finish_datetime: Optional[datetime.datetime] = None

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
