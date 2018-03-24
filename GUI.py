import os
import Network
import HearthRNN
import BoardState
from tkinter import *
from tkinter import messagebox
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np

titleFont = ("Arial", 20, "bold")

class GUI(object):

    def __init__(self):
        self.running = True
        self.root = Tk()
        self.root.title = "Hearth-AI"
        # self.root.resizable(0, 0)
        self.initMainMenu()
        self.initPanels()
        self.initOptions()
        self.initStatusBar()
        self.initNetwokrPlotDisplay()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def Draw(self):
        self.root.update_idletasks()
        self.root.update()

    def initMainMenu(self):
        # create a menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        # self.filemenu.add_command(label="New", command=self.callback)
        # self.filemenu.add_command(label="Open...", command=self.callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)

        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="Guide", command=self.on_help)

    def initPanels(self):
        # create Options frame
        self.panel1 = PanedWindow(orient=VERTICAL)
        self.panel1.pack()

    def initOptions(self):

        OptionsPanel = Frame(self.panel1)
        OptionsPanel.grid(row=0, column=0)

        # TITLE
        Label(OptionsPanel, text="Options", font=titleFont).grid(row=0, column=0, columnspan=2)

        # RUN NAME
        Label(OptionsPanel, text="Run Name").grid(row=1, column=0)
        self.runName = Entry(OptionsPanel)
        self.runName.grid(row=1, column=1, sticky=W+E+N+S)

        # DATA LOADING MODE
        Label(OptionsPanel, text="Data Loading Mode").grid(row=2, column=0)
        self.dataLoadingMode = StringVar(OptionsPanel)
        self.dataLoadingMode.set("0-Load From Stored Data")  # default value
        OptionMenu(OptionsPanel, self.dataLoadingMode, "0-Load From Stored Data", "1-Load From Windows APP",
                   "2-Load From Mac APP").grid(row=2, column=1, columnspan=1, sticky=W+E+N+S)

        # EPOCHS TO RUN
        Label(OptionsPanel, text="Epochs To Run").grid(row=3, column=0)
        self.epochsToRun = Spinbox(OptionsPanel, from_=0, to=1000)
        self.epochsToRun.grid(row=3, column=1, columnspan=1, sticky=W+E+N+S)

        # RUNNING
        self._trainButton = Button(OptionsPanel, text="Train", command=self._train)
        self._trainButton.grid(row=4, column=0, columnspan=2, sticky=W+E+N+S)
        self._testButton = Button(OptionsPanel, text="Test", command=self._test)
        self._testButton.grid(row=5, column=0, columnspan=2, sticky=W+E+N+S)
        self._predictButton = Button(OptionsPanel, text="Predict", command=self._predict)
        self._predictButton.grid(row=6, column=0, columnspan=2, sticky=W+E+N+S)


    def initStatusBar(self):
        status = self.StatusBar(self.root)
        status.pack(side=BOTTOM, fill=X)

    # def initPredition(self):
    #     # create Prediction section
    #

    def initNetwokrPlotDisplay(self):
        # create boardState Display
        padding = Frame(self.panel1)
        padding.grid(row=0, column=1)

        frame = Frame(self.panel1)
        frame.grid(row=0, column=2)

        f = Figure(figsize=(5, 4), dpi=100)
        self.plt = f.add_subplot(111)
        self.plt.title = "Loss Function"

        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas._tkcanvas.grid(row=0, column=0)

    def Plot(self, network):
        self.plt.cla()
        self.plt.plot(network.loss_list)

        # for batch_series_idx in range(5):
        #     one_hot_output_series = np.array(network.predictions_series)[:, batch_series_idx, :]
        #     single_output_series = np.array([(1 if out[0] < 0.5 else 0) for out in one_hot_output_series])
        #
        #     # self.plt.(2, 3, batch_series_idx + 2)
        #     self.plt.cla()
        #     # self.plt.axis([0, network.truncated_backprop_length, 0, 2])
        #     left_offset = range(network.truncated_backprop_length)
        #     self.plt.bar(left_offset, network.batchX[batch_series_idx, :], width=1, color="blue")
        #     self.plt.bar(left_offset, network.batchY[batch_series_idx, :] * 0.5, width=1, color="red")
        #     self.plt.bar(left_offset, single_output_series * 0.3, width=1, color="green")

        # self.plt.draw()

    """ CALLBACKS """

    def callback(self):
        print("called empty callback!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.running = False

    def _train(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def _test(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def _predict(self):
        """Button action event"""
        mode = self._modeSelect
        print(mode)

    def on_help(self):
        print("You asked for Help")

    """GUI SPECIFIC FRAMES"""

    class StatusBar(Frame):

        def __init__(self, master):
            Frame.__init__(self, master)
            self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
            self.label.pack(fill=X)

        def set(self, format, *args):
            self.label.config(text=format % args)
            self.label.update_idletasks()

        def clear(self):
            self.label.config(text="")
            self.label.update_idletasks()
