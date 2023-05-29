from tkinter import *
from sqlite3 import *
from tkinter import ttk
import tkinter as tk


conn=connect('college.db')
root=Tk()
root.configure(bg='gray15')
root.focus_set()

frame=Frame(root,padx=5,pady=5)

mylabel=Label(root,text="COLLEGE MANAGEMENT SYSTEM",bg='black',fg='gray76',bd=4,font=("Times", "20", "bold"),relief=RAISED)
mylabel.pack(pady=10)

lb1=Label(root,text='Please select an option:',bg='black',fg='gray76',bd=4,font=("Monteserrat", "14"),relief=RAISED)
lb1.pack(pady=10)
c=conn.cursor()

DataList=[]

def submit():
    global e
    click=clicked.get()
    for i in e:
        DataList.append(i.get()) #Stores data entered by the user in the textbox

    if click=="Student":
        column_names=dropdown["Student"] #names of columns
        c.execute("INSERT INTO student ({}) VALUES ('{}','{}','{}',{},'{}',{},{},{})".format(",".join(column_names),*DataList))
        c.execute("SELECT * FROM student")
        print(c.fetchall())

    elif click=="Subject":
        column_names=dropdown["Subject"]
        c.execute("INSERT INTO subject ({}) VALUES ('{}','{}',{},'{}',{})".format(",".join(column_names),*DataList))
        c.execute("SELECT * FROM subject")
        print(c.fetchall())

    elif click=="Teacher":
        column_names=dropdown["Teacher"]
        c.execute("INSERT INTO teacher ({}) VALUES ('{}','{}')".format(",".join(column_names),*DataList))
        c.execute("SELECT * FROM teacher")
        print(c.fetchall())

    elif click=="Employee":
        column_names=dropdown["Employee"]
        c.execute("INSERT INTO employee ({}) VALUES ('{}','{}','{}','{}','{}')".format(",".join(column_names),*DataList))
        c.execute("SELECT * FROM employee")
        print(c.fetchall())

    elif click=="Transport":
        column_names=dropdown["Transport"]
        c.execute("INSERT INTO transport ({}) VALUES ({},'{}')".format(",".join(column_names),*DataList))
        c.execute("SELECT * FROM transport")
        print(c.fetchall())

    for i in range(len(e)):
        e[i].delete(0,END)
    del(DataList[:]) #To clear data entered by the user to take input for next entry
    conn.commit()

def delete():
    global e

    click=clicked.get()
    DelVal=e[0].get()

    if click=="Student":
        c.execute("DELETE FROM student WHERE srn='{}'".format(DelVal))
        c.execute("SELECT * FROM student")
        print(c.fetchall())

    elif click=="Subject":
        c.execute("DELETE FROM subject WHERE code='{}'".format(DelVal))
        c.execute("SELECT * FROM subject")
        print(c.fetchall())

    elif click=="Teacher":
        c.execute("DELETE FROM teacher WHERE teacher_id='{}'".format(DelVal))
        c.execute("SELECT * FROM teacher")
        print(c.fetchall())

    elif click=="Employee":
        c.execute("DELETE FROM employee WHERE employee_id='{}'".format(DelVal))
        c.execute("SELECT * FROM employee")
        print(c.fetchall())

    elif click=="Transport":
        c.execute("DELETE FROM transport WHERE Route={}".format(DelVal))
        c.execute("SELECT * FROM transport")
        print(c.fetchall())

    for i in range(len(e)):
        e[i].delete(0,END)
    del(DataList[:]) #To clear data entered by the user to take input for next entry

def update():

    dropdown={"Student":["srn","student_name","student_email","phone_number","branch", "semester", "year_of_joining", "route_number"],

"Subject":["code","subject_name","subject_year","subject_branch","subject_semester"],

"Transport":["Route","Drivers"],

"Teacher":["teacher_id","subject_code"],

"Employee":["employee_id","employee_name","employee_address","employee_email","designation"]}

clicked=StringVar()
clicked.set("Student") #default dropdown option

e=[]
l=[]

def initButton():
    global del_btn
    global submit_btn
    global set_btn
    global update_btn

    del_btn=Button(root,text='DELETE',bg='black',fg='gray76',bd=4,font=("Monteserrat", "11","bold"),relief=RAISED,command=delete)
    del_btn.pack(pady=4,padx=40,side=LEFT)

    submit_btn=Button(root,text='SUBMIT',bg='black',fg='gray76',bd=4,font=("Monteserrat", "11","bold"),relief=RAISED,command=submit)
    submit_btn.pack(pady=4,padx=40,side=LEFT)

    set_btn=Button(root,text='SET',bg='black',fg='gray76',bd=4,font=("Monteserrat", "11","bold"),relief=RAISED,command=setentry)
    set_btn.pack(pady=4,padx=40,side=LEFT)

    update_btn=Button(root,text='UPDATE',bg='black',fg='gray76',bd=4,font=("Monteserrat", "11","bold"),relief=RAISED,command=update)
    update_btn.pack(pady=4,padx=40,side=LEFT)


def initEntry(d,c,e,l):
    for i in d[c.get()]:
        l.append(Label(root,text=i,bg='black',fg='gray76',bd=4,font=("Monteserrat", "12"),relief=RAISED))
        e.append(Entry(root,width=50))

    for k in range(len(e)):
        l[k].pack(pady=4)
        e[k].pack(pady=4)

def initTree(d,clicked,c):
    global treev
    global vscrlbar
    global hscrlbar


    sqlquery='SELECT * FROM {}'.format(clicked.get())
    print(sqlquery,c)
    c.execute(sqlquery)
    table_data=c.fetchall()


    treev=ttk.Treeview(frame,selectmode='browse')

    vscrlbar=ttk.Scrollbar(frame,orient='vertical',command=treev.yview)
    vscrlbar.pack(side='right',fill='x')

    hscrlbar=ttk.Scrollbar(frame,orient='horizontal',command=treev.xview)
    hscrlbar.pack(side='bottom',fill='x')

    treev.configure(xscrollcommand=vscrlbar.set)
    treev.configure(yscrollcommand=hscrlbar.set)

    names = d[clicked.get()]
    columns = tuple(map(str,range(1,len(names)+1)))

    treev["columns"] = columns
    treev['show'] = 'headings'
    for (column, name) in zip(columns, names):
        treev.column(column, width = 150, anchor = 'c')
        treev.heading(column, text = name)

    for row,n in zip(table_data,range(len(table_data))):
        treev.insert('','end',text=str(n),values=tuple(row))
    treev.pack()

def setentry():
    treev.bind('<ButtonRelease-1>',setentry1())

def setentry1():
    global e
    global treev

    curitem=treev.focus()
    x=treev.item(curitem)['values']
    print(range(len(e)),x,len(x))
    for i in range(len(e)):
        e[i].delete(0,END)
        e[i].insert(0,x[i])





def func(*args):
    global l
    global e
    global del_btn
    global submit_btn
    global set_btn
    global update_btn
    global treev
    global vscrlbar
    global hscrlbar
    global curitem
    global x
    for i in range(len(e)):
        l[i].pack_forget()
        e[i].pack_forget()
    l=[]
    e=[]

    del_btn.pack_forget()
    submit_btn.pack_forget()
    set_btn.pack_forget()
    update_btn.pack_forget()
    treev.pack_forget()
    vscrlbar.pack_forget()
    hscrlbar.pack_forget()
    ew=initEntry(dropdown,clicked,e,l)
    initButton()
    initTree(dropdown,clicked,c)


drop=OptionMenu(root,clicked,"Student","Subject","Transport","Teacher","Employee",command=func)
drop.config(bg='black',fg='gray76',bd=4,font=("Monteserrat", "12","bold"),relief=RAISED)
drop.pack(pady=4)
initEntry(dropdown,clicked,e,l)
initButton()
frame.pack(padx=5,pady=5,side=BOTTOM)
initTree(dropdown,clicked,c)


root.mainloop()
