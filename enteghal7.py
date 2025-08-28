import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import xlwings as xw

# محدوده‌های انتقال داده
TRANSFER_RANGES = {
    "DBTakhsis": ["A:P"],
    "DBKholaseTakhsis": ["A:D"],
    "DBProjectItems": ["A:K", "R:R"],
    "ProjectDet": ["B1:B2", "B3", "B4:B5"],
    "BarnameZamanbandi": ["A:I"],
    "PishraftVagheii": ["A:C"],
    "ListF": ["A:V"],
    "DBHazineha": ["A:L"],
    "GFBs": ["A:G"],
    "ZarayebFosool": ["A:F"],
    "FBs": ["A:F"],
    "DBTafkikItem": ["A:J"],
    "DBSoorat": ["A:F", "I:J", "L:L", "P:P"]
}

def get_max_row_for_columns(sheet, cols):
    max_row = 1
    for col in cols:
        col_data = sheet.range(f"{col}1:{col}1048576").value
        if not isinstance( col_data, list):
            continue
        col_max = next((i for i, v in reversed(list(enumerate(col_data, 1))) if v not in (None, "")), 0)
        max_row = max(max_row, col_max)
    return max_row

def generate_dynamic_ranges(file_path, transfer_ranges, password=None):
    app = xw.App(visible=False)
    wb = app.books.open(file_path)
    dynamic_ranges = {}

    for sheet_name, ranges in transfer_ranges.items():
        if sheet_name=="ProjectDet":continue
        match sheet_name:
            case "DBTakhsis":
                start_row="2"
            case "DBKholaseTakhsis":
                start_row="2"
            case "DBProjectItems":
                start_row="2"
            case "BarnameZamanbandi":
                start_row="2"
            case "PishraftVagheii":
                start_row="4"
            case "ListF":
                start_row="2"
            case "DBHazineha":
                start_row="2"
            case "GFBs":
                start_row="2"
            case "ZarayebFosool":
                start_row="2"
            case "FBs":
                start_row="2"
            case "DBTafkikItem":
                start_row="2"
            case "DBSoorat":
                start_row="2"
            case _:
                start_row="2"
        
        if isinstance(ranges, str):
            ranges = [ranges]
        try:
            sht = wb.sheets[sheet_name]

            was_protected = sht.api.ProtectContents
            if was_protected and password:
                sht.api.Unprotect(Password=password)

            calculated_ranges = []
            for rng in ranges:
                cols = []
                for part in rng.split(","):
                    for section in part.split(":"):
                        if section:
                            cols.append(section.strip())
                max_row = get_max_row_for_columns(sht, cols)
                calculated_ranges.append(
                    ":".join([rng.split(":")[0] + start_row, rng.split(":")[-1] + str(max_row)])
                )
            dynamic_ranges[sheet_name] = calculated_ranges

            if was_protected and password:
                sht.api.Protect(Password=password)

        except Exception as e:
            print(f"⚠ خطا در پردازش شیت {sheet_name}: {e}")
            dynamic_ranges[sheet_name] = ranges
            try:
                if was_protected and password:
                    sht.api.Protect(Password=password)
            except:
                pass

    wb.close()
    app.quit()
    return dynamic_ranges


def read_excel_file(file, sheet_name, rng, password=None):
    try:
        app = xw.App(visible=False)
        wb = app.books.open(file)
        ws = wb.sheets[sheet_name]
        if ws.api.ProtectContents and password:
            ws.api.Unprotect(Password=password)
        data = ws.range(rng).value
        wb.close()
        app.quit()
        return data
    except Exception as e:
        print(f"خطا در خواندن محدوده {rng} شیت {sheet_name} از فایل {file}: {e}")
        return None

def transfer_data(old_file, new_file, password=None):
    try:
        dynamic_ranges = generate_dynamic_ranges(old_file, TRANSFER_RANGES, password)
        print("📌 محدوده‌های نهایی:")
        print(dynamic_ranges)
        app = xw.App(visible=False)
        wb_new = app.books.open(new_file)

        for sheet, ranges in dynamic_ranges.items():
            print(f"📌 در حال پردازش شیت: {sheet}")

            if sheet in [s.name for s in wb_new.sheets]:
                ws_new = wb_new.sheets[sheet]

                was_protected = ws_new.api.ProtectContents
                if was_protected and password:
                    ws_new.api.Unprotect(Password=password)

                for rng in ranges:
                    print(f"🔹 پردازش محدوده: {rng}")
                    old_data = read_excel_file(old_file, sheet, rng, password)

                    if old_data:
                        current_data = ws_new.range(rng).value
                        if not isinstance(old_data[0], list):
                            old_data = [old_data]
                        if not isinstance(current_data[0], list):
                            current_data = [current_data]

                        rows = len(old_data)
                        cols = len(old_data[0]) if rows > 0 else 0

                        changed_cells = 0

                        for i in range(rows):
                            for j in range(cols):
                                old_val = old_data[i][j] if i < len(old_data) and j < len(old_data[i]) else None
                                cur_val = current_data[i][j] if i < len(current_data) and j < len(current_data[i]) else None

                                if old_val != cur_val:
                                    ws_new.range((i+1, j+1)).value = old_val
                                    changed_cells += 1

                        print(f"✅ {changed_cells} سلول به‌روزرسانی شدند.")
                    else:
                        print(f"⚠ داده‌ای در محدوده {rng} از شیت {sheet} وجود ندارد.")
                
                if was_protected and password:
                    ws_new.api.Protect(Password=password)

        wb_new.save()
        wb_new.close()
        app.quit()
        print("✅ انتقال اطلاعات انجام شد.")

    except Exception as e:
        messagebox.showerror("خطا", str(e))

def select_old_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xlsm;*.xlsb")])
    old_file_entry.delete(0, tk.END)
    old_file_entry.insert(0, file_path)

def select_new_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xlsm;*.xlsb")])
    new_file_entry.delete(0, tk.END)
    new_file_entry.insert(0, file_path)

def start_transfer():
    old_file = old_file_entry.get()
    new_file = new_file_entry.get()
    password = password_entry.get()
    if old_file and new_file:
        transfer_data(old_file, new_file, password)
    else:
        messagebox.showwarning("خطا", "لطفاً فایل‌های قدیمی و جدید را انتخاب کنید")

# رابط گرافیکی
tk_root = tk.Tk()
tk_root.title("انتقال اطلاعات اکسل")

tk.Label(tk_root, text="فایل قدیمی:").grid(row=0, column=0)
old_file_entry = tk.Entry(tk_root, width=50)
old_file_entry.grid(row=0, column=1)
tk.Button(tk_root, text="انتخاب", command=select_old_file).grid(row=0, column=2)

tk.Label(tk_root, text="فایل جدید:").grid(row=1, column=0)
new_file_entry = tk.Entry(tk_root, width=50)
new_file_entry.grid(row=1, column=1)
tk.Button(tk_root, text="انتخاب", command=select_new_file).grid(row=1, column=2)

tk.Label(tk_root, text="رمز شیت‌ها:").grid(row=2, column=0)
password_entry = tk.Entry(tk_root, width=50, show="*")
password_entry.grid(row=2, column=1)





tk.Button(tk_root, text="انتقال داده‌ها", command=start_transfer).grid(row=3, column=1)





tk_root.mainloop()
