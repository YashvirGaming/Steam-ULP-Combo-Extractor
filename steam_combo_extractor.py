import os, threading, hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import webbrowser

# ✅ Official Steam domains only
STEAM_DOMAINS = [
    "steamcommunity.com",
    "store.steampowered.com",
    "help.steampowered.com",
    "partner.steampowered.com",
    "api.steampowered.com",
    "checkout.steampowered.com",
    "login.steampowered.com",
    "sso.steampowered.com"
]

chunk_size = 500000  # Futureproof chunk handling

def launch_player():
    # ✅ Opens YouTube mini-player in default browser
    webbrowser.open_new("https://www.youtube.com/watch?v=fPO76Jlnz6c")

class SteamExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam [ULP] Combo Extractor | Yashvir Gaming")
        self.root.geometry("610x400")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.combo_file = None

        self.title_label = ctk.CTkLabel(root, text="Steam [ULP] Combo Extractor", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.author_label = ctk.CTkLabel(
            root,
            text="🔥 AUTHOR Telegram: @therealyashvirgaming 🔥",
            font=("Arial", 12)
        )
        self.author_label.pack(pady=5)

        self.browse_btn = ctk.CTkButton(root, text="📂 Browse Combo File", command=self.browse_file)
        self.browse_btn.pack(pady=10)

        self.filter_label = ctk.CTkLabel(root, text="🔍 Filtering for official Steam domains only", font=("Arial", 11))
        self.filter_label.pack(pady=5)

        self.progress = ctk.CTkProgressBar(root, width=400, height=20, progress_color="green")
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.status_label = ctk.CTkLabel(root, text="Waiting...", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.start_btn = ctk.CTkButton(root, text="🚀 Start Extraction", command=self.start_extraction)
        self.start_btn.pack(pady=10)

        self.file_label = ctk.CTkLabel(root, text="No file selected", font=("Arial", 10))
        self.file_label.pack(pady=5)

        self.credits_btn = ctk.CTkButton(root, text="📜 Credits", command=self.show_credits)
        self.credits_btn.pack(pady=10)

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            self.combo_file = file
            self.file_label.configure(text=f"Selected: {os.path.basename(file)}")

    def extractor_worker(self):
        try:
            base_name = os.path.splitext(os.path.basename(self.combo_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_STEAMONLY_{timestamp}.txt"

            seen = set()
            total_lines = 0
            kept = 0

            with open(self.combo_file, "r", encoding="utf-8", errors="ignore") as infile, \
                 open(output_file, "w", encoding="utf-8") as outfile:

                for line in infile:
                    total_lines += 1
                    raw = line.strip()

                    # ✅ must contain Steam domain
                    if not any(domain in raw for domain in STEAM_DOMAINS):
                        continue

                    # Split by colon
                    parts = raw.split(":")

                    # ✅ Require at least 2 fields (user + pass)
                    if len(parts) < 2:
                        continue

                    # Always take last two tokens = username:password
                    user = parts[-2].strip()
                    pwd = parts[-1].strip()

                    # Skip garbage (empty fields)
                    if not user or not pwd:
                        continue

                    # Convert email -> username
                    if "@" in user:
                        user = user.split("@")[0]

                    combo = f"{user}:{pwd}"

                    # Deduplication
                    if combo not in seen:
                        outfile.write(combo + "\n")
                        seen.add(combo)
                        kept += 1

                    # Progress feedback
                    if total_lines % 50000 == 0:
                        self.progress.set(0.5)
                        self.status_label.configure(
                            text=f"⚡ Processed {total_lines:,} lines... {kept:,} saved"
                        )
                        self.root.update_idletasks()

            self.progress.set(1)
            self.status_label.configure(
                text=f"✅ Done! Extracted {kept:,} username:password combos (from {total_lines:,} lines).\nSaved to {output_file}"
            )

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}")

    def start_extraction(self):
        if not self.combo_file:
            messagebox.showerror("Error", "Please select a combo file first!")
            return
        self.status_label.configure(text="⚡ Please wait, extraction in progress...")
        threading.Thread(target=self.extractor_worker, daemon=True).start()

    def show_credits(self):
        credits = ctk.CTkToplevel(self.root)
        credits.title("Credits")
        credits.geometry("450x350")
        credits.resizable(False, False)

        ctk.CTkLabel(
            credits,
            text="💖 Made with love by Yashvir Gaming 💖",
            text_color="cyan",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        yt_button = ctk.CTkButton(
            credits,
            text="🔥 Subscribe on YouTube 🔥",
            fg_color="red",
            hover_color="#cc0000",
            text_color="white",
            font=("Arial", 14, "bold"),
            width=280,
            height=50,
            cursor="hand2",
            command=lambda: webbrowser.open("https://www.youtube.com/@YashvirBlogger?sub_confirmation=1")
        )
        yt_button.pack(pady=12)

        tg_button = ctk.CTkButton(
            credits,
            text="💬 Join Telegram Group 💬",
            fg_color="green",
            hover_color="#006400",
            text_color="white",
            font=("Arial", 14, "bold"),
            width=280,
            height=50,
            cursor="hand2",
            command=lambda: webbrowser.open("https://t.me/OFFICIALYASHVIRGAMING_GROUPCHAT")
        )
        tg_button.pack(pady=12)

        fb_button = ctk.CTkButton(
            credits,
            text="📘 Join Facebook Group 📘",
            fg_color="blue",
            hover_color="#0033cc",
            text_color="white",
            font=("Arial", 14, "bold"),
            width=280,
            height=50,
            cursor="hand2",
            command=lambda: webbrowser.open("https://www.facebook.com/groups/svbconfigsmaker/")
        )
        fb_button.pack(pady=12)

if __name__ == "__main__":
    # 🔥 Launch YouTube mini-player in browser
    threading.Thread(target=launch_player, daemon=True).start()

    root = ctk.CTk()
    app = SteamExtractorGUI(root)
    root.mainloop()
