from typing import Optional

from pydantic.dataclasses import dataclass

from enums.eams_status import EAMSStatus
from enums.iecc_console import IECCConsole


@dataclass
class EAMSRecord:
    eams_wo: int
    iecc_log_id: int
    iecc_console: IECCConsole
    status: EAMSStatus
    remarks: Optional[str]

    def to_dict(self) -> dict:
        d = self.__dict__
        d["iecc_console"] = d["iecc_console"].value
        d["status"] = d["status"].value
        return d
