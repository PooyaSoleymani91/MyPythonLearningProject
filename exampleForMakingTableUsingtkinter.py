import tkinter as tk
import tksheet

root = tk.Tk()
root.geometry("600x300")

sheet = tksheet.Sheet(root)
sheet.pack(fill="both", expand=True)

# مقدار اولیه
data = [
    ["1", "بتن C25", "متر مکعب", 1200000],
    ["2", "آرماتور 16", "کیلوگرم", 25000]
]

sheet.set_sheet_data(data)

# قفل کردن ستون اول (id)
sheet.headers(["ID", "Item", "Vahed", "Price"])
sheet.enable_bindings((
    "single_select", "row_select", "column_select",
    "arrowkeys", "right_click_popup_menu",
    "rc_insert_row", "rc_delete_row",
    "edit_cell"
))

# ستون اول (ID) رو فقط-خواندنی کنیم
sheet.column_width(column=0, width=80, redraw=True)
sheet.hide_columns([0])  # یا می‌تونی کامل مخفی کنی

root.mainloop()
