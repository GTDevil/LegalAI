"""Start LegalAI. Opens the calling desk in the web browser (works on any PC).

Use --window for the old Tkinter desktop window.
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from pathlib import Path


def calling_desk_html() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        return base / "web" / "index.html"
    return Path(__file__).resolve().parent / "web" / "index.html"


def open_browser_desk() -> None:
    page = calling_desk_html()
    if not page.exists():
        raise FileNotFoundError(f"Calling desk page not found: {page}")
    webbrowser.open(page.resolve().as_uri())
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "LegalAI",
            "The calling desk opened in your browser.\n\n"
            "Click Start process on that page to test the AI agent.\n"
            "You can close this message.",
        )
        root.destroy()
    except Exception:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="LegalAI calling desk")
    parser.add_argument(
        "--window",
        action="store_true",
        help="Open the Tkinter desktop window instead of the browser page",
    )
    args = parser.parse_args()
    if args.window:
        from app.desktop_ui import run_desktop_app

        run_desktop_app()
        return
    open_browser_desk()


if __name__ == "__main__":
    main()
