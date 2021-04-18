import tkinter as tk
from tkinter import Tk
import sys
from View.homepage import Homepage

class Application(Tk):

    def __init__(self, event, controller):
        Tk.__init__(self)
        self.event = event
        self.controller = controller
        self.frame = None
        self.protocol("WM_DELETE_WINDOW", self.annihilator)

    def display_frame(self, frame_class):
        if self.frame is not None:
            self.frame.destroy()

        new_frame = frame_class(self, self.event, self.controller)
        self.frame = new_frame
        new_frame.pack()

    def annihilator(self):
        self.destroy()
        sys.exit()