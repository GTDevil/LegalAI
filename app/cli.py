"""Command-line campaign runner for testing without the desktop window."""

from __future__ import annotations

import argparse
from pathlib import Path

from app.call_agent import CampaignController
from app.settings import AppSettings
from app.workbook import load_workbook_file, save_workbook_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LegalAI demo calling campaign on a sheet")
    parser.add_argument("--input", required=True, help="CSV or XLSX with Name and Phone columns")
    parser.add_argument("--output", required=True, help="Where to write the updated sheet")
    parser.add_argument("--firm-name", default="LegalAI Associates")
    args = parser.parse_args()

    leads = load_workbook_file(Path(args.input))
    settings = AppSettings(firm_name=args.firm_name, call_mode="demo", seconds_between_calls=0)
    report = CampaignController().run(leads, settings)
    save_workbook_file(Path(args.output), leads)
    print(f"Attempted={report.attempted} completed={report.completed} skipped={report.skipped}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
