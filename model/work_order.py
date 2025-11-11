from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkOrder:
    id: str
    wo_id: str
    start_work_date: str
    start_work_time: str
    finish_work_date: str
    finish_work_time: str
    problem_code: str
    cause_code: str
    remedy_code: str
    component_code_1: str
    component_code_2: str
    job_status: Optional[str] = None
    execution_error_message: Optional[str] = None
    actual_start_date: Optional[str] = None
    actual_finish_date: Optional[str] = None
