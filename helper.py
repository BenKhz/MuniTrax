#! usr/bin/python

import requests, logging, time

import xml.etree.ElementTree as ET


stopList = ["13893", "13892", "16089", "16088"]  # List of Stop IDs.
testurl = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&stopId="

def getRoute(url):  # Working API retrieval
    '''Get requests a URL to local temp file named TempXML.xml'''
    logging.info("Attempting API call for stop id:" + url[-5:])
    try:
        with open("TempXML.xml", 'w') as inFile:

            r = requests.get(url)
            inFile.write(r.text)
            inFile.close()
        logging.info("API response received and stored as TEMP_XML.xml")
    except ConnectionError as e:
    #    logging.warning(str(e) + " occured in getRoute()")
        time.sleep(60)
    except:
    #    logging.warning("Bare exception error occurred in getRoute()")
        time.sleep(60)


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
        logging.info("Found root and attempting XML Parsing...")
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
                logging.info("No 'direction' tag in " + i.get('routeTitle'))
        logging.info("Current XML page parsed successfully.")
    except ET.ParseError as e:
    #    logging.warning("ET.ParseError " + str(e) + " occurred. Check bash-crash.log?")
        pass
    except BaseException as baseE:
    #    logging.warning('%(baseE)s occured. Check crash.log?')
        pass

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
