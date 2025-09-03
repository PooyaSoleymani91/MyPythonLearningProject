import pandas
import tkinter as tk
from dbexcle import init_db, add_fehrestbaha, add_items, list_items, list_fehrestbaha, show_item
from tkinter import filedialog, messagebox
import xlwings as xw





def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xlsm;*.xlsb")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def rangeChk(sheet):
    try:
        return sheet.used_range.last_cell.row
    except:
        print("error in range chk")





def copy_to_DB(fileentry,copy_max_row,sheet_name,fehrestbaha):
    # try:
        fileentry=file_entry.get()
        print(f"fileentry: finished")
        app = xw.App(visible=False)
        print(f"app: finished")
        wb = app.books.open(fileentry)
        print(f"wb: finished")
        sht=wb.sheets[sheet_name]
        print(f"sht: finished")
        fbid=add_fehrestbaha(fehrestbaha)
        print(f"fbid: finished {fbid}")
        for i in range(1,copy_max_row):
            itemcode=sht.range(f"A{i}").value
            itemdesc=sht.range(f"B{i}").value
            itemunit=sht.range(f"C{i}").value
            itemprice=sht.range(f"D{i}").value
            print(f"{itemcode},{fbid},{itemdesc},{itemunit},{itemprice}")
            add_items(itemcode,fbid,itemdesc,itemunit,itemprice)
            print("Successful")

    # except:
        print("error in copy to DB ")

def start_copy():
    init_db()
    fileEntry=file_entry.get()
    fbname=newfb_entry.get()
    app = xw.App(visible=False)
    wb = app.books.open(fileEntry)
    sht=wb.sheets["copysheet"]
    maxrang=rangeChk(sht)
    print(f"rangeChk successful{maxrang}")
    copy_to_DB(fileEntry,maxrang,"copysheet",fbname)


def showitem_btn():
    itemc=item_entry.get()
    crntfb=selected_option.get()
    Allfbs=list_fehrestbaha()
    for fb in Allfbs:
        if fb["name"]==crntfb:
            crntfbid=fb["id"]
    if crntfb=="انتخاب کنید":
        messagebox.showerror(title="خطا",message="لطفا فهرست بها را انتخاب کنید")
    else:
        print(show_item(crntfbid,itemc))
        messagebox.showinfo(title="مشخصات آیتم", message=show_item(crntfbid,itemc))

selectedOPTtxt=""
def selectedOptCmnd():
    print(dropdownfb.grab_release)



#UI Design:

tk_root = tk.Tk()
tk_root.title("منوی اصلی")
# finalOption=["test1","test2"]
init_db()
if list_fehrestbaha()==[]:
    options=[]
else:
    options = list_fehrestbaha()
finalOption=list()
for optionOne in options:
    finalOption.append(optionOne["name"])
print(f"final Option is: {finalOption}")
selected_option = tk.StringVar(tk_root)
selected_option.set("انتخاب کنید")
tk.Label(tk_root, text="عنوان فهرست بها:").grid(row=0, column=0)
newfb_entry = tk.Entry(tk_root, width=50)
newfb_entry.grid(row=0, column=1)
tk.Button(tk_root, text="11اضافه کردن", command=None).grid(row=0, column=2)
tk.Label(tk_root, text="ورودی فایل اکسل:").grid(row=1, column=0)
file_entry = tk.Entry(tk_root, width=50)
file_entry.grid(row=1, column=1)
tk.Button(tk_root, text="باز کردن", command=select_file,).grid(row=1, column=2)
tk.Button(tk_root, text="افزودن آیتم ها", command=start_copy).grid(row=2, column=2)

tk.Label(tk_root, text="انتخاب فهرست بها:").grid(row=2, column=0)
dropdownfb = tk.OptionMenu(tk_root,selected_option,*finalOption)
dropdownfb.grid(row=2, column=1)

tk.Label(tk_root, text="انتخاب آیتم:").grid(row=3, column=0)
item_entry = tk.Entry(tk_root, width=50)
item_entry.grid(row=3, column=1)
 
tk.Button(tk_root, text="مشاهده آیتم", command=showitem_btn).grid(row=4, column=1)

tk_root.mainloop()
#---------------------------------------------------------------------


