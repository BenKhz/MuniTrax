"""All XML parsing happens here."""

import xml.etree.ElementTree as ET


class XmlParser:
    """XML Parser."""

    @classmethod
    def parse_xml(cls, xml_file):    # working generator function.
        '''
        Creates a generator.
            Parses single XML file and finds selected elements.

        Yields: A list on each specific route with indices as follows:

            [<route number>,<direction>,<Stop location>,<nested list of departs>]
        '''
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for i in root.findall("./predictions"):
            try:
                for j in i.findall('./direction'):
                    predict_list = j.findall('./prediction')
                    min_list = []
                    min_count = 0
                    for elems in predict_list:
                        if min_count < 2: # Stops appending at 2 entries
                            min_list.append(elems.get('minutes'))
                            min_count += 1
                        elif len(min_list) < 2:
                            min_list.append('Min')
                        else:
                            min_list.append('Min')
                            break
                    row_data = []
                    route = i.get('routeTag')
                    stop = i.get('stopTitle')
                    direct = j.get('title')
                    if "Presidio" in stop and "Presidio" in direct:
                        if "Park" in direct:
                            row_data.append(route)
                            row_data.append(direct)
                            row_data.append(stop)
                            row_data.append(min_list)
                            yield row_data
                        else:
                            continue
                    else:
                        row_data.append(route)
                        row_data.append(direct)
                        row_data.append(stop)
                        row_data.append(min_list)
                        yield row_data
            except IndexError:
                print("No 'direction' tag in " + i.get('routeTitle'))
