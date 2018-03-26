# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

from BoardState import *

from HearthRNN import RNN

LARGE_FONT = ("Verdana", 12)
titleFont = ("Arial", 20, "bold")

class HS_GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Hearthstone AI")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.dataLoadingMode = 0

        self.trainMode = False
        self.testMode = False
        self.predictMode = False

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        # self.filemenu.add_command(label="New", command=self.callback)
        # self.filemenu.add_command(label="Open...", command=self.callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)

        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="Guide", command=self.on_help)

        self.running = True

        self.frames = {}

        for F in (MainMenu, Options, Predictions, TrainingDisplay):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

        self.initStatusBar()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def Draw(self):
        if self.frames[Options].dataLoadingModeButton.get() == "0-Load From Stored Data":
            self.dataLoadingMode = 0
        elif self.frames[Options].dataLoadingModeButton.get() == "1-Load From Windows APP":
            self.dataLoadingMode = 1
        elif self.frames[Options].dataLoadingModeButton.get() == "2-Load From Mac APP":
            self.dataLoadingMode = 2

        self.update_idletasks()
        self.update()

    def initStatusBar(self):
        self.status = StatusBar(self)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def Plot(self, network):
        """HI"""
        self.frames[Predictions].plt.cla()
        self.frames[Predictions].plt.plot(network.loss_list)

    """ CALLBACKS """

    def callback(self):
        self.debug("%s", "Called empty callback!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            self.running = False

    def beginTrain(self):
        self.trainMode = True
        self.show_frame(TrainingDisplay)
        self.debug("%s", "Begin Training")

    def beginTest(self):
        self.testMode = True
        self.debug("%s", "Begin Testing")

    def beginPredict(self):
        self.predictMode = True
        self.debug("%s", "Begin Predicting")

    def stopNetwork(self):
        self.trainMode = False
        self.testMode = False
        self.predictMode = False
        self.debug("%s", "Network Stopped")

    def on_help(self):
        self.debug("%s", "You asked for Help")

    def debug(self, format, *args):
        self.status.set(format, *args)

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main Menu", font=titleFont)
        label.pack(pady=10, padx=10, fill=tk.X)
        runFrame = tk.Frame(self)
        runFrame.pack(fill=tk.X)
        # RUNNING
        self._trainButton = Button(runFrame, text="Train", command=controller.beginTrain)
        self._trainButton.pack(fill=X)
        self._testButton = Button(runFrame, text="Test", command=controller.beginTest)
        self._testButton.pack(fill=X)
        self._predictButton = Button(runFrame, text="Predict", command=controller.beginPredict)
        self._predictButton.pack(fill=X)

        button2 = ttk.Button(self, text="Training Graph",
                             command=lambda: controller.show_frame(Predictions))
        button2.pack(side=BOTTOM)
        button = ttk.Button(self, text="Network Settings",
                            command=lambda: controller.show_frame(Options))
        button.pack(side=BOTTOM)


class TrainingDisplay(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # TITLE
        tk.Label(self, text="Training Network", font=titleFont).pack(fil=X)

        optionsFrame = Frame(self)
        self.optionsTitlesFrame = tk.Frame(optionsFrame)
        # OPTIONS Titles
        self.networkTitle = Label(self.optionsTitlesFrame, text="Network Options", anchor=SW)
        self.networkTitle.pack(fill=X, side=LEFT)

        self.playerTitle = Label(self.optionsTitlesFrame, text="Player Options", anchor=SE)
        self.playerTitle.pack(fill=X, side=RIGHT)

        self.optionsTitlesFrame.pack(fill=X, expand=True)

        self.optionsFrame = tk.Frame(optionsFrame)
        # OPTIONS DISPLAY
        self.networkOptions = OptionsDisplay(self.optionsFrame)
        self.networkOptions.pack(fill=X, side=LEFT, expand=True)

        self.playerOptions = OptionsDisplay(self.optionsFrame)
        self.playerOptions.pack(fill=X, side=LEFT, expand=True)

        self.optionsFrame.pack(fill=X, expand=True)

        optionsFrame.pack(fill=X, expand=True)

        boardframe = Frame(self)
        tk.Label(boardframe, text="BoardState").pack(fil=X)

        self.boardstateFrame = tk.Frame(boardframe)
        # Boardstate DISPLAY
        self.boardstate = OptionsDisplay(self.boardstateFrame)
        self.boardstate.pack(fill=X, side=LEFT, expand=True)

        self.boardstateFrame.pack(fill=X, expand=True)

        boardframe.pack(fill=X, expand=True)

        # NAVIGATION
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainMenu))
        button1.pack(side=BOTTOM)

class Options(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # TITLE
        tk.Label(self, text="Options Page", font=titleFont).pack(fil=X)

        # RUN NAME
        tk.Label(self, text="Run Name").pack(fil=X)
        self.runName = tk.Entry(self)
        self.runName.pack(fil=X)

        # DATA LOADING MODE
        tk.Label(self, text="Data Loading Mode").pack(fil=X)
        self.dataLoadingModeButton = tk.StringVar(self)
        self.dataLoadingModeButton.set("0-Load From Stored Data")  # default value
        tk.OptionMenu(self, self.dataLoadingModeButton, "0-Load From Stored Data", "1-Load From Windows APP",
                      "2-Load From Mac APP").pack(fil=X)

        # EPOCHS TO RUN
        tk.Label(self, text="Epochs To Run").pack()
        self.epochsToRun = tk.Spinbox(self, from_=0, to=1000)
        self.epochsToRun.pack(fil=X)

        # NAVIGATION
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainMenu))
        button1.pack(side=BOTTOM)

class Predictions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Graph Page", font=titleFont)
        label.pack(pady=10, padx=10)

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.plt = self.f.add_subplot(111)
        # self.plt.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainMenu))
        button1.pack(side=tk.BOTTOM, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)



class StatusBar(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=W)
        self.label.pack(fill=tk.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class OptionsDisplay(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.list = tk.Listbox(self, bd=1, relief=tk.SUNKEN)
        self.list.pack(fill=tk.X, expand=True)

    def setOptions(self, boardstate):
        """TODO: IMPLEMENT"""

class BoardStateDisplay(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.list = tk.Listbox(self, bd=1, relief=tk.SUNKEN)
        self.list.pack(fill=tk.X, expand=True)