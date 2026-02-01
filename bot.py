import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random

DATA_FILE = "equities.json"

def fetch_mock_api(symbol):
    return {
        "price" : 100
    }

def mock_chatgpt_response(message):

    return f"Mock response to: {message}"

class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Trading Bot")
        self.equities = self.load_equities()
        self.system_running = False

        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=10)

        #Form to add a new equity to our trading bot 
        tk.Label(self.form_frame, text="Symbol:").grid(row=0, column=0)
        self.symbol_entry = tk.Entry(self.form_frame)
        self.symbol_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Levels:").grid(row=0, column=2)
        self.levels_entry = tk.Entry(self.form_frame)
        self.levels_entry.grid(row=1, column=3)

        tk.Label(self.form_frame, text="Drawdown%:").grid(row=0, column=4)
        self.drawdown_entry = tk.Entry(self.form_frame)
        self.drawdown_entry.grid(row=1, column=5)

        self.add_button = tk.button(self.form_frame, text="Add Equity", command=self.add_equity)
        self.add_button.grid(row=0, column=6)

        #Table to track the traded equities
        self.tree = ttk.Treeview(root, columns=("symbol",  "Position", "Entry Price", "Levels", "Status"), show='headings')
        for col in ["Symbol", "Position", "Entry Price", "Levels", "Status"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col)
        self.tree.pack(pady=10)

        #Button to control the bot
        self.toggle_system_button = tk.Button(root, text="Toggle selected System", command=self.tooggle_system)
        self.toggle_system_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove selected Equity", command=self.remove_selected_equity)
        self.remove_button.pack(pady=5)

        #AI component
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(pady=10)

        self.chat_input = tk.Entry(self.chat_frame, width=50)
        self.chat_input.grid(row=0, column=0, padx=5)

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_buttongrid(row=0, column=1)

        self.chat_output = tk.Text(root, height=5, width=60, state=tk.DISABLED)
        self.chat_output.pack()

        #Load saved data
        self.refresh_table()

        self.running = True
        self.auto_update_thread = threading.Thread(target=self.auto_update, daemo=True)
        self.auto_update_thread.start()
    
    def add_equity(self):
        symbol = self.symbol_entry.get().upper()
        levels = self.levels_entry.get()
        drawdwon = self.drawdown_entry.get()

        if not symbol or not levels.isdigit() or not drawdown.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Invalid Input")
            return


        levels = int(levels)
        drawdown = float(drawdown) /100
        entry_price = fetch_mock_api(symbol)['price']

        level_prices = {i+1: round(entry_price * (1-drawdown*(i+1), 2)) for i in range (levels)}

        self.equities[symbol] = {
            "position":0,
            "entry_price":entry_price,
            "levels":level_prices,
            "status":"Off"
        }
        self.save_equities()
        self.refresh_table()