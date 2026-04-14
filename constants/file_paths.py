import os

from typing import final

iecc_centralized_log_directory: final = r"C:\Users\leecamkf\OneDrive - MTR Corporation\02-iecc-centralized-logs\DUAT"
iecc_centralized_log_file_name = r"IECC_Fault_Log_DUAT_2025_dev.xlsx"
# iecc_centralized_log_file_name = r"test_file_v3.xlsx"
iecc_centralized_log_file_path = os.path.join(iecc_centralized_log_directory, iecc_centralized_log_file_name)

rru_template_directory = r"C:\Users\leecamkf\PycharmProjects\iecn-eams-workorder-automation-tool\input"
template_file_name = r"cmwo-template.xlsx"
template_file_path = os.path.join(rru_template_directory, template_file_name)

output_directory = r"C:\Users\leecamkf\PycharmProjects\iecn-eams-workorder-automation-tool\output"
