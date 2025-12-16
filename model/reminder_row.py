import datetime

from pydantic.dataclasses import dataclass
from typing import List


@dataclass
class ReminderRow:
    id: int
    fault_report_date: datetime.date
    equipment: str
    fault_category: str
    fault_description: str
    eams_wo: int
    overdue_days: int
