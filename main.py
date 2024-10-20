


from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox,font
from tkinter import ttk
from datetime import datetime
import webbrowser


#======================================================================================
#  ========================== File Code Starts Here  ============================
#=======================================================================================


#=================================== New Code  ======================================
def new():
        text.delete('1.0','end')
#===================================== End =========================================


# ========================= New Window Code  ================================
def new_window():
        root = tk.Tk()
        root.geometry('500x500')


        menubar = Menu(root)

        file = Menu(menubar,tearoff = 0)
        file.add_command(label="New",command=new)
        file.add_command(label="New window",command=new_window)
        file.add_command(label="Open",command=Open)
        file.add_command(label="Save",command=save)
        file.add_command(label="Save as", command=save_as)
        file.add_separator()
        file.add_command(label="Exit",command=exit)
        menubar.add_cascade(label="File",menu=file,font=('verdana',10,'bold'))


        text = ScrolledText(root,width=1000,height=1000)
        text.place(x=0,y=0)



        root.mainloop()

# =========================== End ==============================================        


# ===================== Open File Code ========================================
def Open():
        root.filename = filedialog.askopenfilename(
                initialdir = '/',
                title="Select file",
                filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        file = open(root.filename)
        text.insert('end',file.read())
#================================= End ==========================================


#================================ Save File Code ====================================
def save():
        pass
#================================    End      =======================================

#=================================== save as File code  ==============================
def save_as():
        root.filename = filedialog.asksaveasfile(mode="w",defaultextension='.txt')
        if root.filename is None:
                return
        file_save =  str(text.get(1.0,END))
        root.filename.write(file_save)
        root.filename.close()
# ================================ End ============================================

# ================================ Exit Code =====================================
def exit():
        message = messagebox.askquestion('Notepad',"Do you want to save changes")
        if message == "yes":
                save_as()
        else:
                root.destroy()
#==================================== end =========================================


# ============================= Main Window =============================

root = tk.Tk()
root.geometry('600x300')
root.minsize(400,400)
root.title('notepad')
root.iconbitmap('notepad.ico')
text = ScrolledText(root,height=1000,undo=True)
text.pack(fill=tk.BOTH)

menubar = Menu(root)

file = Menu(menubar,tearoff = 0)
file.add_command(label="New",command=new)
file.add_command(label="New window",command=new_window)
file.add_command(label="Open",command=Open)
file.add_command(label="Save",command=save)
file.add_command(label="Save as", command=save_as)
file.add_separator()
file.add_command(label="Exit",command=exit)
menubar.add_cascade(label="File",menu=file,font=('verdana',10,'bold'))




# ======================== Right Click Menu =========================================

root.config(menu=menubar)
root.mainloop()

# ========================== End =======================================