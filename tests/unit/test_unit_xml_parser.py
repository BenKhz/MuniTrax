"""Testing for xml_parser."""
import os
import pprint

from munitrax import XmlParser


HERE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestUnitXmlParser:
    """Test XML Parser."""

    def test_unit_xml_parser_init(self):
        """Make sure the method returns data and has the expected items."""
        xml_file = os.path.join(HERE_DIR, "../assets/test.xml")
        result = [x for x in XmlParser.parse_xml(xml_file)]
        pprint.pprint(result)
        control = [['2',
                    'Inbound to Mission + Main',
                    'California St & Presidio Ave',
                    ['16', '36', 'Min']],
                   ['1',
                    'Inbound to Drumm + Clay',
                    'California St & Presidio Ave',
                    ['10', '20', 'Min']]]
        assert result == control
