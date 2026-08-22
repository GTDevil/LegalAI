"""Tkinter desktop UI for the LegalAI Loan Settlement Agent."""

import tkinter as tk
from tkinter import messagebox, ttk

from app.settlement import LoanCase, recommend_settlement

COLORS = {
    "bg": "#f4f6f9",
    "card": "#ffffff",
    "primary": "#1e3a5f",
    "accent": "#2563eb",
    "accent_hover": "#1d4ed8",
    "text": "#1f2937",
    "muted": "#6b7280",
    "border": "#e5e7eb",
    "success": "#059669",
}


class SettlementDesktopApp:
    """Desktop application for loan settlement recommendations."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LegalAI — Loan Settlement Agent")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(520, 640)

        self._configure_style()
        self._build_layout()
        self._center_window()

    def _configure_style(self) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Card.TFrame", background=COLORS["card"])
        style.configure(
            "Title.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["primary"],
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Field.TLabel",
            background=COLORS["card"],
            foreground=COLORS["text"],
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "ResultTitle.TLabel",
            background=COLORS["card"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        style.configure(
            "ResultValue.TLabel",
            background=COLORS["card"],
            foreground=COLORS["text"],
            font=("Segoe UI", 11),
        )
        style.configure(
            "ResultHighlight.TLabel",
            background=COLORS["card"],
            foreground=COLORS["success"],
            font=("Segoe UI", 22, "bold"),
        )

    def _center_window(self) -> None:
        self.root.update_idletasks()
        width = max(self.root.winfo_width(), 560)
        height = max(self.root.winfo_height(), 680)
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_layout(self) -> None:
        outer = ttk.Frame(self.root, padding=20)
        outer.pack(fill=tk.BOTH, expand=True)

        ttk.Label(outer, text="LegalAI", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            outer,
            text="Loan settlement offer calculator for collections teams",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 16))

        form_card = ttk.Frame(outer, style="Card.TFrame", padding=16)
        form_card.pack(fill=tk.X, pady=(0, 12))

        self.fields: dict[str, ttk.Entry] = {}
        field_defs = [
            ("principal", "Original principal ($)", "50000"),
            ("outstanding_balance", "Outstanding balance ($)", "40000"),
            ("days_past_due", "Days past due", "90"),
            ("borrower_income", "Borrower annual income ($)", "55000"),
            ("prior_settlements", "Prior settlements (count)", "0"),
        ]

        for key, label, default in field_defs:
            row = ttk.Frame(form_card, style="Card.TFrame")
            row.pack(fill=tk.X, pady=6)
            ttk.Label(row, text=label, style="Field.TLabel").pack(anchor=tk.W)
            entry = ttk.Entry(row, font=("Segoe UI", 11))
            entry.insert(0, default)
            entry.pack(fill=tk.X, pady=(4, 0), ipady=4)
            self.fields[key] = entry

        btn_row = ttk.Frame(outer, style="Card.TFrame")
        btn_row.pack(fill=tk.X, pady=(0, 12))
        self.calc_btn = tk.Button(
            btn_row,
            text="Calculate Settlement Offer",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["accent"],
            fg="white",
            activebackground=COLORS["accent_hover"],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=10,
            command=self._calculate,
        )
        self.calc_btn.pack(fill=tk.X)

        results_card = ttk.Frame(outer, style="Card.TFrame", padding=16)
        results_card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            results_card,
            text="RECOMMENDED OFFER",
            style="ResultTitle.TLabel",
        ).pack(anchor=tk.W)

        self.amount_label = ttk.Label(
            results_card,
            text="—",
            style="ResultHighlight.TLabel",
        )
        self.amount_label.pack(anchor=tk.W, pady=(4, 12))

        self.discount_label = ttk.Label(results_card, text="", style="ResultValue.TLabel")
        self.discount_label.pack(anchor=tk.W, pady=2)
        self.terms_label = ttk.Label(results_card, text="", style="ResultValue.TLabel")
        self.terms_label.pack(anchor=tk.W, pady=2)

        ttk.Label(
            results_card,
            text="Rationale",
            style="ResultTitle.TLabel",
        ).pack(anchor=tk.W, pady=(12, 4))

        self.rationale_text = tk.Text(
            results_card,
            height=5,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#f9fafb",
            fg=COLORS["text"],
            relief=tk.FLAT,
            padx=8,
            pady=8,
        )
        self.rationale_text.pack(fill=tk.BOTH, expand=True)
        self.rationale_text.configure(state=tk.DISABLED)

    def _parse_float(self, key: str, label: str) -> float:
        raw = self.fields[key].get().strip().replace(",", "")
        try:
            value = float(raw)
        except ValueError:
            raise ValueError(f"{label} must be a valid number.") from None
        if value < 0:
            raise ValueError(f"{label} cannot be negative.")
        return value

    def _parse_int(self, key: str, label: str) -> int:
        raw = self.fields[key].get().strip()
        try:
            value = int(raw)
        except ValueError:
            raise ValueError(f"{label} must be a whole number.") from None
        if value < 0:
            raise ValueError(f"{label} cannot be negative.")
        return value

    def _calculate(self) -> None:
        try:
            principal = self._parse_float("principal", "Original principal")
            outstanding = self._parse_float("outstanding_balance", "Outstanding balance")
            days_past_due = self._parse_int("days_past_due", "Days past due")
            income = self._parse_float("borrower_income", "Borrower income")
            prior = self._parse_int("prior_settlements", "Prior settlements")

            if principal <= 0 or outstanding <= 0:
                raise ValueError("Principal and outstanding balance must be greater than zero.")

            case = LoanCase(
                principal=principal,
                outstanding_balance=outstanding,
                days_past_due=days_past_due,
                borrower_income=income,
                prior_settlements=prior,
            )
            offer = recommend_settlement(case)
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        self.amount_label.configure(text=f"${offer.recommended_amount:,.2f}")
        self.discount_label.configure(
            text=f"Discount: {offer.discount_percent:.1f}% off outstanding balance"
        )
        self.terms_label.configure(
            text=f"Payment terms: {offer.payment_terms_months} months"
        )

        self.rationale_text.configure(state=tk.NORMAL)
        self.rationale_text.delete("1.0", tk.END)
        self.rationale_text.insert(tk.END, offer.rationale)
        self.rationale_text.configure(state=tk.DISABLED)


def run_desktop_app() -> None:
    root = tk.Tk()
    SettlementDesktopApp(root)
    root.mainloop()
