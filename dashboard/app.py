"""NAVARIS desktop dashboard. Sensitive workbooks are stored encrypted in SecureVault."""
from __future__ import annotations

import tempfile
import tkinter.messagebox as messagebox
from pathlib import Path

import customtkinter as ctk

from src.core.branch_manager import get_decision
from src.specializations.consulting.excel_factory import create_consulting_sheet


class NavarisDashboard(ctk.CTk):
    def __init__(self, vault):
        super().__init__()
        self.vault = vault
        self.title("NAVARIS Business Intelligence OS")
        self.geometry("900x650")
        self.minsize(760, 560)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="#0A1931")
        ctk.CTkLabel(self, text="NAVARIS", font=ctk.CTkFont(size=30, weight="bold"),
                     text_color="#D4AF37").grid(row=0, column=0, padx=28, pady=(28, 4), sticky="w")
        ctk.CTkLabel(self, text="Business Intelligence & Operations", text_color="#FFFBF0").grid(
            row=1, column=0, padx=30, pady=(0, 22), sticky="w")

        panel = ctk.CTkFrame(self, fg_color="#10284D", corner_radius=14)
        panel.grid(row=2, column=0, padx=28, pady=10, sticky="ew")
        panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(panel, text="Service").grid(row=0, column=0, padx=18, pady=18, sticky="w")
        self.service = ctk.CTkOptionMenu(
            panel, values=["consulting", "auditor", "training"],
            fg_color="#D4AF37", button_color="#B8952F", text_color="#0A1931")
        self.service.set("consulting")
        self.service.grid(row=0, column=1, padx=18, pady=18, sticky="ew")

        ctk.CTkLabel(panel, text="Company name").grid(row=1, column=0, padx=18, pady=18, sticky="w")
        self.company = ctk.CTkEntry(panel, placeholder_text="Enter company name")
        self.company.grid(row=1, column=1, padx=18, pady=18, sticky="ew")

        self.generate_button = ctk.CTkButton(
            panel, text="Generate Excel Sheet", command=self.generate,
            fg_color="#D4AF37", hover_color="#B8952F", text_color="#0A1931",
            font=ctk.CTkFont(weight="bold"))
        self.generate_button.grid(row=2, column=0, columnspan=2, padx=18, pady=(12, 22), sticky="ew")

        status = ctk.CTkFrame(self, fg_color="#10284D", corner_radius=14)
        status.grid(row=3, column=0, padx=28, pady=12, sticky="ew")
        status.grid_columnconfigure((0, 1, 2), weight=1)
        self.decision_value = ctk.CTkLabel(status, text="🟡", font=ctk.CTkFont(size=42))
        self.decision_value.grid(row=0, column=0, padx=15, pady=(20, 4))
        ctk.CTkLabel(status, text="Decision", text_color="#D4AF37").grid(row=1, column=0, padx=15, pady=(0, 18))
        self.bep_value = ctk.CTkLabel(status, text="BEP: Not calculated", font=ctk.CTkFont(size=16))
        self.bep_value.grid(row=0, column=1, rowspan=2, padx=15, pady=20)
        self.cf_value = ctk.CTkLabel(status, text="CF: Not calculated", font=ctk.CTkFont(size=16))
        self.cf_value.grid(row=0, column=2, rowspan=2, padx=15, pady=20)

        self.result = ctk.CTkLabel(self, text="Generated workbooks are encrypted inside SecureVault.",
                                   text_color="#FFFBF0", wraplength=800, justify="left")
        self.result.grid(row=4, column=0, padx=30, pady=18, sticky="w")
        self.footer = ctk.CTkLabel(self, text="Local-first • SQLCipher • AES-256-GCM",
                                   text_color="#D4AF37")
        self.footer.grid(row=5, column=0, padx=30, pady=(4, 20), sticky="w")

    def generate(self):
        company = self.company.get().strip()
        if not company:
            messagebox.showwarning("NAVARIS", "Enter a company name first.")
            return
        mapping = {"consulting": "consulting_proposal", "auditor": "audit", "training": "training_plan"}
        self.generate_button.configure(state="disabled", text="Generating...")
        try:
            with tempfile.TemporaryDirectory(prefix="navaris-sheet-") as temp_dir:
                xlsx_path = create_consulting_sheet(company, mapping[self.service.get()], output_dir=temp_dir)
                vault_id = self.vault.encrypt_file(xlsx_path, delete_source=True)
            self.decision_value.configure(text=get_decision("amber"))
            self.bep_value.configure(text="BEP: Awaiting validated inputs")
            self.cf_value.configure(text="CF: Awaiting validated inputs")
            self.result.configure(
                text=f"Encrypted workbook stored in Vault. Reference: {vault_id}\n"
                     "Plain XLSX temporary file removed. BEP/CF are not estimated without verified company inputs.")
            messagebox.showinfo("NAVARIS", "Excel workbook encrypted and saved inside SecureVault.")
        except Exception as exc:
            messagebox.showerror("NAVARIS Generation Error", str(exc))
        finally:
            self.generate_button.configure(state="normal", text="Generate Excel Sheet")


def run_app(vault):
    app = NavarisDashboard(vault)
    app.mainloop()
