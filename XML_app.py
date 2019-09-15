"""Main module for MuniTraxx."""
#! usr/bin/python

import time
import tkinter as tk

import requests
import PySimpleGUI as sg

from .munitrax import XmlParser

logo = r"""
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

monitor = tk.Tk()  # instance of tk to get monitor resolution.
height = 900  # Initial GUI window designed for 1600X900 resolution.
width = 1600
h_ratio = (monitor.winfo_screenheight() / height)  # make ratio for autoresize.
w_ratio = (monitor.winfo_screenwidth() / width)
stopList = ["13893", "13892", "16089", "16088"]  # List of Stop IDs.
testurl = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&stopId="
table_headers = ["Route", "Direction", "Stop", "Departures"]
greeting_text = "Welcome to the Jewish Community Center of San Francisco"


def getRoute(url):  # Working API retrieval
    '''Get requests a URL to local temp file named TempXML.xml'''

    with open("TempXML.xml", 'w') as inFile:

        r = requests.get(url)
        inFile.write(r.text)
        inFile.close()


def populate_table():
    '''
    Iterate getRoute() and parse_xml() to create complete table.
    This formats the table in a consummable manner for PYSimpleGUI.

    Returns: Two-Dimensional List // table_data
    '''

    table_data = []
    for s in stopList:  # Working loop with Generator.
        getRoute(testurl + s)
        for x in XmlParser.parse_xml("TempXML.xml"):
            table_data.append(x)
    table_data.sort()
    return table_data  # working combined getRoute(),parse_xml(),with iterate.


table_data = populate_table()   # initial table population.

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
                            num_rows=min(len(table_data), 14),
                            hide_vertical_scroll=True,
                            row_height=int(70*h_ratio),
                            key='table')
                            ]]


display = sg.Window('Transit Times',  # GUI window containing table setup.
                    table_form,
                    size=(int(width*w_ratio) ,int(height*h_ratio)),
                    no_titlebar=True,
                    location=(0,0),
                    keep_on_top=True,
                    )
print("Screen Dimensions set to: " + str(width * w_ratio) + "x" + str(height*h_ratio))
# count = 0
while True:  # Main Loop. Change to while count < x for testing.
    table_data = populate_table()
#    count += 1
    event, values = display.Read(timeout=10000)
    display.FindElement('table').Update(values=table_data,
                                num_rows=min(len(table_data), 14)
                                )
# display.Close()
with open('python.log', 'w') as logfile:
    logfile.write(logo)
    logfile.write("While loop exited at : " + time.asctime())
    logfile.close()
