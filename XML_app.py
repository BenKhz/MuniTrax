#! usr/bin/python

import time
import xml.etree.ElementTree as ET
import requests
import os

import PySimpleGUI as sg
import tkinter as tk

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


def parse_xml():    # working generator function.
    '''
    Creates a generator.
        Parses single XML file and finds selected elements.

    Yields: A list on each specific route with indices as follows:

        [<route number>,<direction>,<Stop location>,<nested list of departs>]
    '''
    try:
        tree = ET.parse('TempXML.xml')
        root = tree.getroot()
        #    table_data = []
        for i in root.findall("./predictions"):
            try:
                for j in i.findall('./direction'):
                    predict_list = j.findall('./prediction')
                    min_list = []
                    min_count = 0
                    for elems in predict_list:
                        if min_count < 2:  # Stops appending at 2 entries
                            min_list.append(elems.get('minutes'))
                            min_count += 1
                        else:
                            break
                    min_list.append('Min')

                    row_data = []
                    route = i.get('routeTag')
                    stop = i.get('stopTitle')
                    direct = j.get('title')
                    # Custom Logic filtering redundancy unique to these stops
                    # Leaving in may or may not effect your application.
                    if "Presidio" in stop and "Presidio" in direct:
                        if "Park" in direct:
                            row_data.append(route)
                            row_data.append(direct)
                            row_data.append(stop)
                            row_data.append(min_list)
                            yield (row_data)
                        else:
                            continue
                    else:
                        row_data.append(route)
                        row_data.append(direct)
                        row_data.append(stop)
                        row_data.append(min_list)
                        yield (row_data)
            except IndexError:
                print("No 'direction' tag in " + i.get('routeTitle'))
    except ET.ParseError:
        print("ET.ParseError occurred at : " + time.asctime())
        time.sleep(30)


def populate_table():
    '''
    Iterate getRoute() and parse_xml() to create complete table.
    This formats the table in a consummable manner for PYSimpleGUI.

    Returns: Two-Dimensional List // table_data
    '''

    table_data = []
    for s in stopList:  # Working loop with Generator.
        getRoute(testurl + s)
        for x in parse_xml():
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
#count = 0
while True:  # Main Loop. Change to while count < x for testing.
#    count += 1
    event, values = display.Read(timeout=5000)
    time.sleep(5)
    display.FindElement('table').Update(values=populate_table())

    with open('python.log', 'w') as logfile:
        logfile.write(logo)
        logfile.write("While loop exited at : " + time.asctime())
        logfile.close()
