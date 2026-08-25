"""Tkinter desktop app: Excel-like calling sheet plus AI campaign controls."""

from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from app.call_agent import CampaignController
from app.paths import default_workbook_path, sample_leads_path
from app.settings import AppSettings, load_settings, save_settings
from app.workbook import (
    COLUMNS,
    HEADERS,
    Lead,
    empty_leads,
    lead_from_mapping,
    load_workbook_file,
    save_workbook_file,
)

COLORS = {
    "bg": "#eef2f7",
    "card": "#ffffff",
    "primary": "#12355b",
    "accent": "#1d4ed8",
    "text": "#111827",
    "muted": "#6b7280",
    "grid": "#d1d5db",
}


STATUS_COLORS = {
    "Not called": "#f3f4f6",
    "Calling": "#fef3c7",
    "No answer": "#e5e7eb",
    "No loan": "#e5e7eb",
    "Not interested": "#fee2e2",
    "Interested": "#dcfce7",
    "Completed": "#bbf7d0",
    "Call failed": "#fecaca",
    "Live call placed": "#dbeafe",
}


class Spreadsheet(ttk.Frame):
    def __init__(self, parent: tk.Widget, leads: list[Lead]) -> None:
        super().__init__(parent)
        self.leads = leads
        self.tree = ttk.Treeview(self, columns=COLUMNS, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        widths = {
            "name": 140,
            "phone": 130,
            "call_status": 130,
            "interested": 90,
            "total_loan_amount": 140,
            "remaining_amount": 160,
            "settlement_amount": 180,
            "legal_fee": 110,
            "fee_percent": 70,
            "cibil_or_experience": 170,
            "notes": 280,
        }
        for column, header in zip(COLUMNS, HEADERS, strict=True):
            self.tree.heading(column, text=header)
            self.tree.column(column, width=widths.get(column, 120), minwidth=80, stretch=True)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self._begin_edit)
        self._editor: tk.Entry | None = None
        self.reload()

    def reload(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for index, lead in enumerate(self.leads):
            values = [lead.display_values()[column] for column in COLUMNS]
            item = self.tree.insert("", tk.END, iid=str(index), values=values)
            self._paint(item, lead.call_status)

    def _paint(self, item: str, status: str) -> None:
        tag = status.replace(" ", "_")
        self.tree.tag_configure(tag, background=STATUS_COLORS.get(status, "#ffffff"))
        self.tree.item(item, tags=(tag,))

    def refresh_row(self, index: int, lead: Lead) -> None:
        self.leads[index] = lead
        item = str(index)
        if self.tree.exists(item):
            self.tree.item(item, values=[lead.display_values()[column] for column in COLUMNS])
            self._paint(item, lead.call_status)
            self.tree.see(item)
            self.tree.selection_set(item)

    def selected_index(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            return None
        return int(selection[0])

    def _begin_edit(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        if self._editor is not None:
            self._editor.destroy()
            self._editor = None
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)
        if not row_id or not col_id:
            return
        col_index = int(col_id.replace("#", "")) - 1
        bbox = self.tree.bbox(row_id, col_id)
        if not bbox:
            return
        x, y, width, height = bbox
        value = self.tree.set(row_id, COLUMNS[col_index])
        editor = tk.Entry(self.tree, font=("Segoe UI", 10))
        editor.place(x=x, y=y, width=width, height=height)
        editor.insert(0, value)
        editor.select_range(0, tk.END)
        editor.focus_set()
        self._editor = editor

        def commit(_event: object | None = None) -> None:
            if self._editor is None:
                return
            new_value = editor.get()
            editor.destroy()
            self._editor = None
            self._apply_cell(int(row_id), col_index, new_value)

        editor.bind("<Return>", commit)
        editor.bind("<FocusOut>", commit)
        editor.bind("<Escape>", lambda _e: (editor.destroy(), setattr(self, "_editor", None)))

    def _apply_cell(self, row_index: int, col_index: int, value: str) -> None:
        column = COLUMNS[col_index]
        current = self.leads[row_index].display_values()
        current[column] = value
        self.leads[row_index] = lead_from_mapping(current)
        self.refresh_row(row_index, self.leads[row_index])


class LegalAIDesktopApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LegalAI — Loan Settlement Calling Agent")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(1100, 680)
        self.settings: AppSettings = load_settings()
        self.controller = CampaignController()
        self.workbook_path = default_workbook_path()

        leads = self._load_starting_leads()
        self._build(leads)
        self._center()

    def _load_starting_leads(self) -> list[Lead]:
        if self.workbook_path.exists():
            try:
                return load_workbook_file(self.workbook_path)
            except Exception:
                pass
        sample = sample_leads_path()
        if sample.exists():
            return load_workbook_file(sample)
        return empty_leads()

    def _center(self) -> None:
        self.root.update_idletasks()
        width = max(self.root.winfo_width(), 1200)
        height = max(self.root.winfo_height(), 720)
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build(self, leads: list[Lead]) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["primary"], font=("Segoe UI", 18, "bold"))
        style.configure("Sub.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=("Segoe UI", 10))

        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill=tk.BOTH, expand=True)

        ttk.Label(outer, text="LegalAI calling desk", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            outer,
            text="Excel-like sheet of people to call. Start process and the AI agent calls each number, then fills settlement details.",
            style="Sub.TLabel",
        ).pack(anchor=tk.W, pady=(0, 8))

        toolbar = ttk.Frame(outer)
        toolbar.pack(fill=tk.X, pady=(0, 8))
        buttons = [
            ("Start process", self._start),
            ("Stop", self._stop),
            ("Add person", self._add_person),
            ("Remove person", self._remove_person),
            ("Open Excel / CSV", self._open_file),
            ("Save sheet", self._save_file),
            ("Settings", self._settings),
            ("How to use", self._help),
        ]
        for text, command in buttons:
            tk.Button(
                toolbar,
                text=text,
                command=command,
                bg=COLORS["accent"] if text == "Start process" else "#ffffff",
                fg="white" if text == "Start process" else COLORS["text"],
                font=("Segoe UI", 10, "bold" if text == "Start process" else "normal"),
                relief=tk.FLAT,
                padx=10,
                pady=6,
                cursor="hand2",
            ).pack(side=tk.LEFT, padx=3)

        self.mode_label = ttk.Label(toolbar, text="", style="Sub.TLabel")
        self.mode_label.pack(side=tk.RIGHT)
        self._refresh_mode_label()

        self.sheet = Spreadsheet(outer, leads)
        self.sheet.pack(fill=tk.BOTH, expand=True)

        ttk.Label(outer, text="Call transcript (what the AI agent said)", style="Sub.TLabel").pack(anchor=tk.W, pady=(8, 2))
        self.log = tk.Text(outer, height=10, wrap=tk.WORD, font=("Segoe UI", 10), bg="#ffffff")
        self.log.pack(fill=tk.BOTH, expand=False)
        self.log.insert(tk.END, "Open the application, add names and numbers (or keep the sample list), then click Start process.\n")
        self.log.configure(state=tk.DISABLED)

        self.status = ttk.Label(outer, text="Ready.", style="Sub.TLabel")
        self.status.pack(anchor=tk.W, pady=(6, 0))

    def _refresh_mode_label(self) -> None:
        mode = "Demo AI calls (no real phone)" if self.settings.call_mode != "twilio" else "Live Twilio calls"
        self.mode_label.configure(text=f"{self.settings.firm_name}  ·  {mode}")

    def _append_log(self, lines: list[str]) -> None:
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, "\n" + "\n".join(lines) + "\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def _start(self) -> None:
        if self.controller.running():
            messagebox.showinfo("Already running", "The AI agent is already making calls. Click Stop if you want to halt.")
            return
        callable_rows = [lead for lead in self.sheet.leads if lead.phone.strip()]
        if not callable_rows:
            messagebox.showwarning("No numbers", "Add at least one person with a phone number first.")
            return
        mode_note = (
            "This will place REAL phone calls using your Twilio account."
            if self.settings.call_mode == "twilio"
            else "This will run DEMO AI calls (no real phone network). The sheet will still update automatically."
        )
        if not messagebox.askyesno("Start process", mode_note + "\n\nCall every person who is not already completed?"):
            return
        self.status.configure(text="Calling…")
        thread = threading.Thread(target=self._run_campaign, daemon=True)
        thread.start()

    def _run_campaign(self) -> None:
        def on_progress(index: int, lead: Lead, transcript: list[str]) -> None:
            self.root.after(0, lambda: self._on_progress(index, lead, transcript))

        self.controller.run(self.sheet.leads, self.settings, on_progress=on_progress)
        self.root.after(0, self._campaign_finished)

    def _on_progress(self, index: int, lead: Lead, transcript: list[str]) -> None:
        self.sheet.refresh_row(index, lead)
        self._append_log([f"—— {lead.name or lead.phone} ——"] + transcript)
        self.status.configure(text=f"Updated row {index + 1}: {lead.call_status}")
        try:
            save_workbook_file(self.workbook_path, self.sheet.leads)
        except Exception:
            pass

    def _campaign_finished(self) -> None:
        self.status.configure(text="Process finished. The sheet has been saved.")
        self._append_log(["System: Campaign finished."])

    def _stop(self) -> None:
        self.controller.request_stop()
        self.status.configure(text="Stopping after the current call…")

    def _add_person(self) -> None:
        name = simpledialog.askstring("Add person", "Name:", parent=self.root)
        if name is None:
            return
        phone = simpledialog.askstring("Add person", "Phone number:", parent=self.root)
        if phone is None:
            return
        self.sheet.leads.append(Lead(name=name.strip(), phone=phone.strip()))
        self.sheet.reload()

    def _remove_person(self) -> None:
        index = self.sheet.selected_index()
        if index is None:
            messagebox.showinfo("Remove person", "Click a row first, then click Remove person.")
            return
        del self.sheet.leads[index]
        self.sheet.reload()

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Open leads",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            leads = load_workbook_file(Path(path))
        except Exception as exc:
            messagebox.showerror("Could not open file", str(exc))
            return
        if not leads:
            leads = empty_leads()
        self.sheet.leads = leads
        self.sheet.reload()
        self.status.configure(text=f"Opened {path}")

    def _save_file(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save sheet",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")],
            initialfile="leads.xlsx",
        )
        if not path:
            return
        try:
            save_workbook_file(Path(path), self.sheet.leads)
            save_workbook_file(self.workbook_path, self.sheet.leads)
        except Exception as exc:
            messagebox.showerror("Could not save", str(exc))
            return
        self.status.configure(text=f"Saved {path}")

    def _settings(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.transient(self.root)
        frm = ttk.Frame(win, padding=16)
        frm.pack(fill=tk.BOTH, expand=True)
        fields: dict[str, tk.Entry] = {}
        specs = [
            ("firm_name", "Firm name", self.settings.firm_name),
            ("call_mode", "Call mode (demo or twilio)", self.settings.call_mode),
            ("seconds_between_calls", "Seconds between calls", str(self.settings.seconds_between_calls)),
            ("twilio_account_sid", "Twilio Account SID", self.settings.twilio_account_sid),
            ("twilio_auth_token", "Twilio Auth Token", self.settings.twilio_auth_token),
            ("twilio_from_number", "Twilio From number", self.settings.twilio_from_number),
        ]
        for key, label, value in specs:
            ttk.Label(frm, text=label).pack(anchor=tk.W, pady=(8, 0))
            entry = ttk.Entry(frm, width=48)
            entry.insert(0, value)
            entry.pack(fill=tk.X)
            fields[key] = entry

        def save() -> None:
            self.settings.firm_name = fields["firm_name"].get().strip() or self.settings.firm_name
            mode = fields["call_mode"].get().strip().lower()
            self.settings.call_mode = "twilio" if mode == "twilio" else "demo"
            try:
                self.settings.seconds_between_calls = float(fields["seconds_between_calls"].get() or 1)
            except ValueError:
                self.settings.seconds_between_calls = 1.0
            self.settings.twilio_account_sid = fields["twilio_account_sid"].get().strip()
            self.settings.twilio_auth_token = fields["twilio_auth_token"].get().strip()
            self.settings.twilio_from_number = fields["twilio_from_number"].get().strip()
            save_settings(self.settings)
            self._refresh_mode_label()
            win.destroy()

        tk.Button(frm, text="Save", command=save, bg=COLORS["accent"], fg="white", relief=tk.FLAT, padx=12, pady=6).pack(
            pady=16
        )

    def _help(self) -> None:
        messagebox.showinfo(
            "How to use",
            "1. Names and phone numbers appear in the sheet (sample data is loaded the first time).\n"
            "2. Double-click any cell to edit it, like Excel.\n"
            "3. Click Start process. In Demo mode the AI agent calls each person in software and fills:\n"
            "   interested, total loan, remaining amount, settlement offered, legal fee, CIBIL/experience.\n"
            "4. Click Save sheet to create an Excel file you can email or copy to another PC.\n"
            "5. Real phone calls need a Twilio account. Open Settings, set call mode to twilio, and paste your keys.\n\n"
            "Demo phone endings: 0 = no answer, 1–2 = not interested, 3 = no loan, 4–9 = interested (sheet fills).",
        )


def run_desktop_app() -> None:
    root = tk.Tk()
    LegalAIDesktopApp(root)
    root.mainloop()
