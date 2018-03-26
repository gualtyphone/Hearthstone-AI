import os
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


class HS_GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.running = True
        self.title = "Hearth-AI"
        # self.resizable(0, 0)
        self.initMainMenu()
        self.initPanels()
        self.initOptions()
        self.initStatusBar()
        self.initPlot()
        self.initPredictionsDisplay()


    def Draw(self):
        if self.dataLoadingModeButton.get() == "0-Load From Stored Data":
            self.dataLoadingMode = 0
        elif self.dataLoadingModeButton.get() == "1-Load From Windows APP":
            self.dataLoadingMode = 1
        elif self.dataLoadingModeButton.get() == "2-Load From Mac APP":
            self.dataLoadingMode = 2

        self.update_idletasks()
        self.update()

    def initMainMenu(self):
        # create a menu
        self.menu = Menu(self)
        self.config(menu=self.menu)

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
        self.dataLoadingModeButton = StringVar(OptionsPanel)
        self.dataLoadingModeButton.set("0-Load From Stored Data")  # default value
        OptionMenu(OptionsPanel, self.dataLoadingModeButton, "0-Load From Stored Data", "1-Load From Windows APP",
                   "2-Load From Mac APP").grid(row=2, column=1, columnspan=1, sticky=W+E+N+S)

        # EPOCHS TO RUN
        Label(OptionsPanel, text="Epochs To Run").grid(row=3, column=0)
        self.epochsToRun = Spinbox(OptionsPanel, from_=0, to=1000)
        self.epochsToRun.grid(row=3, column=1, columnspan=1, sticky=W+E+N+S)

        # RUNNING
        self._trainButton = Button(OptionsPanel, text="Train", command=self.beginTrain)
        self._trainButton.grid(row=4, column=0, columnspan=2, sticky=W+E+N+S)
        self._testButton = Button(OptionsPanel, text="Test", command=self.beginTest)
        self._testButton.grid(row=5, column=0, columnspan=2, sticky=W+E+N+S)
        self._predictButton = Button(OptionsPanel, text="Predict", command=self.beginPredict)
        self._predictButton.grid(row=6, column=0, columnspan=2, sticky=W+E+N+S)

    def initPlot(self):
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.plot = self.PlotFrame(container)
        self.plot.pack()

    def initPredictionsDisplay(self):
        SelectPanel = Frame(self.panel1)
        SelectPanel.grid(row=0, column=3)

        # TITLE
        Label(SelectPanel, text="Network Predictions", font=titleFont).grid(row=0, column=0, columnspan=2)


    def initStatusBar(self):
        status = self.StatusBar(self)
        status.pack(side=BOTTOM, fill=X)

    """ CALLBACKS """

    def callback(self):
        print("called empty callback!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            self.running = False

    def beginTrain(self):
        self.trainMode = True
        print("Begin Training")

    def beginTest(self):
        self.testMode = True
        print("Begin Testing")

    def beginPredict(self):
        self.predictMode = True
        print("Begin Predicting")

    def stopNetwork(self):
        self.trainMode = False
        self.testMode = False
        self.predictMode = False
        print("Network Stopped")


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

    class PlotFrame(Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            self.initNetwokrPlotDisplay()

        def initNetwokrPlotDisplay(self):
            f = Figure(figsize=(5, 5), dpi=100)
            self.plt = f.add_subplot(111)
            # self.plt.title = "Loss Function"
            self.plt.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

            # a tk.DrawingArea
            # canvas = FigureCanvasTkAgg(f, master=frame)
            # canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
            # canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)

            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
            canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

            toolbar = NavigationToolbar2TkAgg(canvas, self)
            toolbar.update()
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        def Plot(self, network):
            """HI"""
            # self.plt.cla()
            # self.plt.plot(network.loss_list)

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
            # self.plt.draw()
            # self.plt.pause(0.0001)

