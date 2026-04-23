import uuid
import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime

from helper.logging_helper import logger
from model.eams_wo import EAMSWorkOrder


def _parse_datetime(dt_val: Any) -> str:
    if isinstance(dt_val, datetime):
        return f"{dt_val.strftime("%Y-%m-%d")} {dt_val.strftime("%H:%M:%S")}"
    return ""


def _clean_string(val: Any) -> str:
    """Safely converts a DataFrame value to a string, handling pandas NaNs."""
    if pd.isna(val) or val is None:
        return ""
    return str(val).strip()


def map_dataframe_to_work_orders(df: pd.DataFrame) -> List[EAMSWorkOrder]:
    if df.empty:
        logger.warning("Provided DataFrame is empty. Returning empty list.")
        return []

    # Clean the DataFrame: Replace float NaN values with Python's native None
    # This ensures Optional[str] fields correctly receive None instead of float(nan)
    clean_df = df.where(pd.notnull(df), None)

    work_orders: List[EAMSWorkOrder] = []

    for row in clean_df.to_dict(orient="records"):
        try:
            target_start_datetime = _parse_datetime(row.get('Target Start'))
            target_finish_datetime = _parse_datetime(row.get('Target Finish'))
            actual_start_datetime = _parse_datetime(row.get('Actual Start'))
            actual_finish_datetime = _parse_datetime(row.get('Actual Finish'))

            wo = EAMSWorkOrder(
                work_order_id=int(_clean_string(row.get('Work Order'))),
                description=_clean_string(row.get('Description')),
                work_group=_clean_string(row.get('Work Group')),
                work_type=_clean_string(row.get('Work Type')),
                asset=_clean_string(row.get('Asset')),
                asset_classification=_clean_string(row.get('Asset Classification')),
                location=_clean_string(row.get('Location')),
                status=_clean_string(row.get('Status')),
                job_plan=_clean_string(row.get('Job Plan')),
                target_start_datetime=target_start_datetime,
                target_finish_datetime=target_finish_datetime,
                actual_start_datetime=actual_start_datetime,
                actual_finish_datetime=actual_finish_datetime,
                line=_clean_string(row.get('Line')),
                failure_class=_clean_string(row.get('Failure Class')),
                problem=_clean_string(row.get('Problem')),
                cause=_clean_string(row.get('Cause')),
                remedy=_clean_string(row.get('Remedy'))
            )
            work_orders.append(wo)

        except Exception as e:
            logger.error(f"Error mapping row to WorkOrder (WO: {row.get('Work Order')}): {e}")
            continue

    logger.info(f"Successfully mapped {len(work_orders)} WorkOrders.")
    return work_orders
