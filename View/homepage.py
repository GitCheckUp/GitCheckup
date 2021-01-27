from tkinter import Frame
from functools import partial
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar
from tkinter.scrolledtext import ScrolledText

class Homepage(Frame):

    def __init__(self, master, event, controller):
        self.master = master
        self.event = event
        self.controller = controller

        Frame.__init__(self, master)
        self.pack()

        self.master.geometry("450x160")
        self.master.title("test")

        self.repo_url = ""
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        self.master.geometry("1000x750+554+92")
        self.master.minsize(600, 450)
        self.master.maxsize(1924, 1061)
        self.master.resizable(1, 1)
        self.master.title("GitCheckup")
        self.master.configure(background="#24292e")
        self.master.configure(highlightbackground="#d9d9d9")
        self.master.configure(highlightcolor="#000000")

        self.Button1 = tk.Button(self.master)
        self.Button1.place(relx=0.8, rely=0.067, height=44, width=157)
        self.Button1.configure(activebackground="#24292e")
        self.Button1.configure(activeforeground="white")
        self.Button1.configure(activeforeground="#ffffff")
        self.Button1.configure(background="#24292e")
        self.Button1.configure(borderwidth="3")
        self.Button1.configure(compound='left')
        self.Button1.configure(cursor="arrow")
        self.Button1.configure(disabledforeground="#ffffff")
        self.Button1.configure(font="-family {Arial} -size 14")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(background="#24292e")
        self.Button1.configure(highlightbackground="#24292e")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(highlightthickness="3")
        self.Button1.configure(justify='left')
        self.Button1.configure(overrelief="flat")
        self.Button1.configure(padx="12")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief="flat")
        self.Button1.configure(state='active')
        self.Button1.configure(text='''Analyze''')
        self.Button1.configure(command=self.analyze_repo)

        repo_url = StringVar()

        self.Entry1 = tk.Entry(self.master)
        self.Entry1.place(relx=0.075, rely=0.083, height=30, relwidth=0.705)
        self.Entry1.configure(background="white")
        self.Entry1.configure(cursor="arrow")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(highlightbackground="#d9d9d9")
        self.Entry1.configure(highlightcolor="black")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(selectbackground="blue")
        self.Entry1.configure(selectforeground="white")
        self.Entry1.configure(textvariable=repo_url)

        self.Label1 = tk.Label(self.master)
        self.Label1.place(relx=0.013, rely=0.017, height=31, width=145)
        self.Label1.configure(activebackground="#24292e")
        self.Label1.configure(activeforeground="white")
        self.Label1.configure(activeforeground="#ffffff")
        self.Label1.configure(background="#24292e")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#24292e")
        self.Label1.configure(font="-family {Arial} -size 12")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")

        '''
        prog_call = sys.argv[0]
        prog_location = os.path.split(prog_call)[0]
        photo_location = os.path.join(prog_location, "./View/fork.png")
        _img0 = tk.PhotoImage(file=photo_location)
        self.Label1.configure(image=_img0)
        '''
        self.Label1.configure(justify='left')
        self.Label1.configure(padx='8')
        self.Label1.configure(text='Repository:')

        self.Frame1 = tk.Frame(self.master)
        self.Frame1.place(relx=0.0, rely=0.167, relheight=0.842, relwidth=1.006)
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#ffffff")
        self.Frame1.configure(highlightcolor="#ffffff")

        self.Scrolledtext1 = ScrolledText(self.Frame1)
        self.Scrolledtext1.place(relx=0.012, rely=0.079, relheight=0.901
                                 , relwidth=0.975)
        self.Scrolledtext1.configure(background="white")
        self.Scrolledtext1.configure(font="TkTextFont")
        self.Scrolledtext1.configure(foreground="black")
        self.Scrolledtext1.configure(highlightbackground="#d9d9d9")
        self.Scrolledtext1.configure(highlightcolor="black")
        self.Scrolledtext1.configure(insertbackground="black")
        self.Scrolledtext1.configure(insertborderwidth="3")
        self.Scrolledtext1.configure(selectbackground="blue")
        self.Scrolledtext1.configure(selectforeground="white")
        self.Scrolledtext1.configure(wrap="word")

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(relx=0.012, rely=0.02, height=22, width=70)
        self.Label2.configure(activebackground="#ffffff")
        self.Label2.configure(activeforeground="#ffffff")
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(disabledforeground="#ffffff")
        self.Label2.configure(font="-family {Arial} -size 10 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Summary:''')

    def analyze_repo(self):
        self.event.func = self.controller.analyze_repo
        self.event.args = (self.Entry1.get(),)
        self.event.set()
