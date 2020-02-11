#! usr/bin/python

import time, sys, logging
from logging.handlers import RotatingFileHandler

import PySimpleGUI as sg
import tkinter as tk

import helper  # Stop ID variables and API url in this module

logo = """
 __ __ _  _ __  _ _   _____ ___  __ __   ____   ____  ___   _
|  V  | || |  \| | | |_   _| _ \/  \\\ \_/ /\ \_/ /__\| _ \ / \\
| \_/ | \/ | | ' | |   | | | v / /\ |> , <  > , < \/ | v / \_/
|_| |_|\__/|_|\__|_|   |_| |_|_\_||_/_/ \_\/_/ \_\__/|_|_\ (_)

github.com/BenKhz/MuniTrax

If you are seeing this, it means the iterator <count> has ended the main
while loop, and the XML_app.py scripts needs to be run again.

For testing the while loop counter is set for 2 iterations.

For deployment, increase while loop count or otherwise create a better loop.

"""
# --- Setting global variables --- #

monitor = tk.Tk()  # instance of tk to get monitor resolution.
height = 900  # Initial GUI window designed for 1600X900 resolution.
width = 1600
h_ratio = (monitor.winfo_screenheight() / height)  # make ratio for autoresize.
w_ratio = (monitor.winfo_screenwidth() / width)
table_headers = ["Route", "Direction", "Stop", "Departures"]
greeting_text = "Welcome to the Jewish Community Center of San Francisco"

# --- Initial table population needed before GUI instancing --- #

table_data = helper.populate_table()

# --- Setting up PySimpleGUI variables Below --- #

table_form = [[sg.Image(filename=r'./JCCSF.png',  # talbe setup for GUI..
                        size=(208,173)),
                sg.Text(greeting_text,
                            font="Helvitica " + str(int(28*w_ratio)) + " bold",
                            justification='center')],
                        #    align='center')],
                [sg.Table(values=table_data,
                            headings=table_headers,
                            max_col_width=999,
                            font="Helvitica " + str(int(22*w_ratio)) + " bold",
                            auto_size_columns=False,
                            col_widths=[int(9*w_ratio),int(55*w_ratio),int(50*w_ratio),int(36*w_ratio)],
                            justification='center',
                            num_rows=min(14),
                            hide_vertical_scroll=True,
                            row_height=int(70*h_ratio),
                            key='table')
                            ]]

# --- Logging setup --- #
root = logging.getLogger()
root.setLevel(logging.INFO)
# --- Establishing log formatting --- #
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# --- Setting up rotating file handler for INFO level logs --- #
fileHandler = logging.handlers.RotatingFileHandler('muni.log', maxBytes=6400, backupCount=5)
fileHandler.setLevel(logging.warning)
fileHandler.setFormatter(formatter)
# --- setting up StreamHandler to send only Warn or above to stderr only --- #
stdErrorHandler = logging.StreamHandler(sys.stderr)
stdErrorHandler.setLevel(logging.warning)
# --- adding both new handlers to the root logger --- #
root.addHandler(stdErrorHandler)
root.addHandler(fileHandler)


display = sg.Window('Transit Times',  # GUI window containing table setup.
                    table_form,
                    size=(int(width*w_ratio) ,int(height*h_ratio)),
                    no_titlebar=True,
                    location=(0,0),
                    keep_on_top=True,
                    )
logging.info("Screen Dimensions set to: " + str(width * w_ratio) + "x" + str(height*h_ratio))
# count = 0

while True:  # Main Loop. Change to while count < x for testing.
    # count += 1
    event, values = display.Read(timeout=5000)
    time.sleep(5)
    display.FindElement('table').Update(values=helper.populate_table())
logging.warning("Main While Loop exited and script finished without error.")
