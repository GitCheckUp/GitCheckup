
import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from View import usergui_support as git_check_support
import os.path
from Controller.controller import Controller


"""
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    p1 = tk.PhotoImage(file='./View/icon.png')
    root.iconphoto(False, p1)
    git_check_support.set_Tk_var()
    top = Toplevel1 (root)
    git_check_support.init(root, top)
    root.mainloop()
"""

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    #rt = root
    root = rt
    w = tk.Toplevel(root)
    p1 = tk.PhotoImage(file='./View/icon.png')
    #root.iconphoto(False, p1)
    git_check_support.set_Tk_var()
    top = Toplevel1 (w)
    git_check_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1(object):
    def analyze_button(self):
        self.repo_url = self.Entry1.get()
        self.Scrolledtext1.insert("end","self.repo_url")
        #print(self.repo_url)
        print("clicked")
        sys.stdout.flush()
        pass

    def display_errors(self, errorDetections, totalErrorCount):
        print("Analysis complete.")
        self.Scrolledtext1.insert("end", "Analysis complete.")
        print("Found %d errors or poor practices." % totalErrorCount)

        for detection in errorDetections:
            #print("-------------------------------")
            self.Scrolledtext1.insert("end", "Found %d issues of type %s of category %s:")
            #print("Found %d issues of type %s of category %s:\n" % (len(detection.errorList), detection.name, detection.category))

            for error in detection.errorList:
                self.Scrolledtext1.insert("end", "User: %s made an error%s at: %s on commit sha: %s with message: %s")

                #print("User: %s made an error%s at: %s on commit sha: %s with message: %s" % (error.user.name, error.extra_info, error.commit.date, error.commit.sha, error.commit.message))

    def __init__(self, top=None):
        self.repo_url = ""
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("800x600+554+92")
        top.minsize(800, 600)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("GitCheckup")
        top.configure(background="#24292e")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.Button1 = tk.Button(top)
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
        self.Button1.configure(command=self.analyze_button)

        self.Entry1 = tk.Entry(top)
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
        self.Entry1.configure(textvariable=git_check_support.repo_url)

        self.Label1 = tk.Label(top)
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
        photo_location = os.path.join(prog_location,"./View/fork.png")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.Label1.configure(image=_img0)
        self.Label1.configure(justify='left')
        self.Label1.configure(padx="8")
        self.Label1.configure(text='''Repository:''')

        self.Frame1 = tk.Frame(top)
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
        self.Scrolledtext1.configure(wrap="none")

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


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

