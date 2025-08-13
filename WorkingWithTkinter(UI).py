import tkinter as tk
from pathlib import Path

tk_root = tk.Tk()
tk_root.title("title")

tk.Label(tk_root, text="lable1:").grid(row=0, column=0)
old_file_entry = tk.Entry(tk_root, width=50)
old_file_entry.grid(row=0, column=1)
tk.Button(tk_root, text="Ok", command=None).grid(row=0, column=2)

tk.Label(tk_root, text="label2:").grid(row=1, column=0)
new_file_entry = tk.Entry(tk_root, width=50)
new_file_entry.grid(row=1, column=1)
tk.Button(tk_root, text="Ok2", command=None).grid(row=1, column=2)

tk.Label(tk_root, text="label3:").grid(row=2, column=0)
password_entry = tk.Entry(tk_root, width=50, show="*")
password_entry.grid(row=2, column=1)

tk.Button(tk_root, text="Start", command=None).grid(row=3, column=1)

tk_root.mainloop()