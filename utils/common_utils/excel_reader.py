from pathlib import Path
from typing import Any

import pandas as pd


class ReadExcel:
    def __init__(self, data_directory: str | Path | None = None) -> None:
        self.data_directory = Path(data_directory or Path(__file__).parents[2] / "test_data")

    def _resolve_workbook_path(self, environment: str) -> Path:
        expected_name = f"{environment}_Test_Data.xlsx"
        expected_path = self.data_directory / expected_name
        if expected_path.exists():
            return expected_path

        for file_path in self.data_directory.glob("*.xlsx"):
            if file_path.name.lower() == expected_name.lower():
                return file_path

        raise FileNotFoundError(
            f"Workbook not found for environment '{environment}'. "
            f"Expected '{expected_name}' under '{self.data_directory}'."
        )

    def excel_reader(self, environment: str) -> dict[str, pd.DataFrame]:
        workbook = self._resolve_workbook_path(environment)
        with pd.ExcelFile(workbook) as excel_file:
            return {
                sheet_name: pd.read_excel(workbook, sheet_name=sheet_name)
                for sheet_name in excel_file.sheet_names
            }

    @staticmethod
    def value(data: dict[str, pd.DataFrame], sheet: str, column: str, row: int = 0) -> Any:
        return data[sheet].iloc[row][column]
