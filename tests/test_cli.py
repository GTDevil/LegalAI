"""CLI campaign runner."""

from pathlib import Path

from app.cli import main
from app.workbook import load_workbook_file


def test_cli_writes_updated_sheet(tmp_path: Path, monkeypatch: object) -> None:
    output = tmp_path / "out.xlsx"
    monkeypatch.setattr(
        "sys.argv",
        ["cli", "--input", "data/sample_leads.csv", "--output", str(output), "--firm-name", "CLI Firm"],
    )
    main()
    assert output.exists()
    leads = load_workbook_file(output)
    priya = next(row for row in leads if row.name == "Priya Sharma")
    assert priya.interested == "Yes"
    assert priya.settlement_amount is not None
