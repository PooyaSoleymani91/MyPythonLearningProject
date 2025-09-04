import pandas as pd
import tkinter as tk
from dbexcle import init_db, add_fehrestbaha, add_items, list_items, list_fehrestbaha, show_item , delete_all_itemsdb
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
    try:
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

    except:
        print("error in copy to DB ")

def start_copy():
    init_db()
    fileEntry=file_entry.get()
    fbname=newfb_entry.get()
    print(f"fehrest baha name: {fbname}")
    if fbname=="":
        messagebox.showerror(title="خطا",message="لطفا نام فهرست بها را وارد کنید")
    else:
        app = xw.App(visible=False)
        wb = app.books.open(fileEntry)
        sht=wb.sheets["copysheet"]
        maxrang=rangeChk(sht)
        print(f"rangeChk successful{maxrang}")
        copy_to_DB(fileEntry,maxrang,"copysheet",fbname)
        refreshOptionMenu()
        wb.close()
        app.quit()


def showitem_btn():
    msg=""
    itemc=item_entry.get()
    crntfb=selected_option.get()
    if crntfb=="انتخاب کنید" or crntfb=="هیچ فهرست بهایی موجود نیست":
        messagebox.showerror(title="خطا",message="لطفا فهرست بها را انتخاب کنید")
    else:
        itemToShow=show_item(crntfb,itemc)
        for itemsfound in itemToShow: #cuz itemToShow is a list[dict[any , any]]
            for key in itemsfound.keys():
                msg=msg + f"{key} = {itemsfound[key]} \n" #\n for next line in strings
            msg=msg+"----------------------------\n"
        print(show_item(crntfb,itemc))
        messagebox.showinfo(title="مشخصات آیتم", message=msg)


def delete_all_items():
    crntfb=selected_option.get()
    if crntfb=="انتخاب کنید" or crntfb=="هیچ فهرست بهایی موجود نیست":
        messagebox.showerror(title="خطا",message="لطفا فهرست بها را انتخاب کنید")
    else:
        delete_all_itemsdb(crntfb)
        messagebox.showinfo(title="Delete all items", message="DONE")
        refreshOptionMenu()

def refreshOptionMenu(): #For updation OptionMenu items
    init_db()
    options = list_fehrestbaha()
    finalOption = [opt["name"] for opt in options] if options else []
    if not finalOption:
        finalOption = ["هیچ فهرست بهایی موجود نیست"]

    # پاک کردن آیتم‌های قبلی
    menu = dropdownfb["menu"] #access to internal menu for OptionMenu
    menu.delete(0, "end") #delete items from "0" to "end"

    # اضافه کردن آیتم‌های جدید
    for option in finalOption:
        menu.add_command( #Create each items in menu
            label=option, #name of the item in menu
            command=lambda value=option: selected_option.set(value) #when user clicked on item: (StringVar)s change to name of that item
        )
        #value esme fildiye ke mikhaym avaz konim
        # lambda value=option: ... برای محافظت از مقدار متغیر در حلقه هست بدون این همه آیتم ها آخرین مقدار رو میگیرن


#------------------------------------------------------------------------------------------------        
#UI Design:

tk_root = tk.Tk()
tk_root.title("منوی اصلی")
mainMenu=tk.Menu(tk_root)
tk_root.config(menu=mainMenu) 
init_db()
if list_fehrestbaha()==[]:
    options=[]
else:
    options = list_fehrestbaha()
finalOption=list()
for optionOne in options:
    finalOption.append(optionOne["name"])
if finalOption==[]:
    finalOption=["هیچ فهرست بهایی موجود نیست"]
print(f"final Option is: {finalOption}")
selected_option = tk.StringVar(tk_root)
selected_option.set("انتخاب کنید")
tk.Label(tk_root, text="عنوان فهرست بها:").grid(row=0, column=0)
newfb_entry = tk.Entry(tk_root, width=50)
newfb_entry.grid(row=0, column=1)
tk.Button(tk_root, text="اضافه کردن", command=None).grid(row=0, column=2)
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
tk.Button(tk_root,text="حذف آیتم ها",command=delete_all_items).grid(row=5,column=1)
tk_root.mainloop()
#---------------------------------------------------------------------


