class EAMSReportNotFoundError(FileNotFoundError):
    def __init__(self,
                 file_path: str):
        self.message = f"Failed to locate or process the EAMS report in path: {file_path}"
        super().__init__(self.message)
