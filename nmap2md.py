#!/usr/bin/env python3

from collections import OrderedDict
import re
import sys
import xml.etree.ElementTree as ET
from optparse import OptionParser

__version__ = "1.3.2"

definition = dict(
    port={
        'xpath': '.',
        'children': dict(
            number={
                'attribute': 'portid'
            },
            protocol={
                'attribute': 'protocol'
            }
        ),
    },
    state={
        'attribute': 'state',
        'xpath': 'state'
    },
    service={
        'xpath': 'service',
        'children': dict(
            name={
                'attribute': 'name'
            },
            product={
                'attribute': 'product'
            },
            version={
                'attribute': 'version'
            }
        )
    }
)


class Element:
    name = None
    xpath = ""
    parent = None
    children = []
    attribute = None
    text = False
    level = 0

    def __init__(self, key):
        self.name = key

    def xpathfull(self, xpath=None):
        """Return a full xPath for the element"""

        if xpath is None:
            xpath = []

        xpath.append(self.xpath)

        if self.parent:
            return self.parent.xpathfull(xpath)

        return "".join(reversed(xpath))

    def data(self, xml_element, default=""):
        """Get data from the element depending on the "type" of element,
        either it's attribute data or the text value from the XML element
        """

        if self.text:
            if xml_element.text:
                return xml_element.text
            else:
                return default

        if self.attribute:
            return xml_element.get(self.attribute, default)

        return default

    def find(self, key):
        if key == self.name:
            return self

        splitted_names = key.split(".")

        for k in splitted_names:
            if self.name == k:
                if self.children:
                    for child in self.children:
                        elem = child.find(".".join(splitted_names[1:]))

                        if elem:
                            return elem

        return None

    @staticmethod
    def build(definition_object, parent=None):
        elements = []

        for _, key in enumerate(definition_object):
            elem = Element(key)

            if 'xpath' in definition_object[key]:
                elem.xpath = definition_object[key]['xpath']

            if 'text' in definition_object[key]:
                elem.text = definition_object[key]['text']

            if parent:
                elem.level = parent.level + 1
                elem.parent = parent

            if 'attribute' in definition_object[key]:
                elem.attribute = definition_object[key]['attribute']

            # Recursively build children elements
            if 'children' in definition_object[key]:
                elem.children = Element.build(definition_object[key]['children'], elem)

            elements.append(elem)

        return elements

if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options] file.xml", version="%prog " + __version__)

    parser.add_option("-c", "--columns", default="Port,State,Service,Version", help="define a columns for the table")
    parser.add_option(
        "--hs",
        default=4,
        type="int",
        help="address is used as a header, this option defines header number h1 -> h6"
    )
    parser.add_option(
        "--rc",
        "--row-cells",
        default="[port.number]/[port.protocol],[state],[service.name],[service.product] [service.version]",
        help="define rows which will report certain data. Those rows: [port.number], [port.protocol], [state], "
            "[service.name], [service.product], [service.version] "
    )
    parser.add_option(
        "--print-empty",
        dest="print_empty",
        action="store_true",
        help="should addresses with no opened ports to be printed"
    )
    parser.set_defaults(print_empty=False)

    (options, args) = parser.parse_args()

    columns = options.columns.split(",")
    row_cells = options.rc.split(",")

    definitions = Element.build(definition)
    result = OrderedDict()
    md = ""

    if len(columns) != len(row_cells):
        print("[Err] Columns and row cells amount should be equal")
        sys.exit()

    # Wrong header number, setting to default option
    if options.hs < 0 or options.hs > 6:
        options.hs = 4

    try:
        tree = ET.parse(args[0])
        tree = tree.getroot()
    except IndexError:
        try:
            stdinXml = sys.stdin.read()
            stdinXml = stdinXml[stdinXml.index("<?xml"):]
            tree = ET.fromstring(stdinXml)
        except:
            print("[Err] No filename supplied as an argument")
            print()
            parser.print_help()
            sys.exit()
    except IOError:
        print("[Err] Non-readable or non-existent file supplied as an argument")
        print()
        sys.exit()
    except ET.ParseError:
        print("[Err] Something went wrong when parsing the XML file - perhaps it's corrupted/invalid?")
        print()
        sys.exit()

    for host in tree.findall("host"):
        address = host.find("address").attrib["addr"]
        port_info = []
        ports = host.find("ports")

        if ports:
            for port in ports.findall("port"):
                if port.find("state").get("state") != "open":
                    continue
                cells = []

                for rc in row_cells:
                    current_cell = rc
                    for bc in re.findall("(\[[a-z\.*]+\])", rc):
                        for definition in definitions:
                            elem = definition.find(bc[1:-1])

                            if elem:
                                xml_element = port.find(elem.xpathfull())
                                if xml_element is not None:
                                    data = elem.data(xml_element)
                                    current_cell = current_cell.replace(bc, data)
                                    break

                                break

                    cells.append(current_cell)

                port_info.append(cells)

        port_info.sort(key=lambda port_num: list(map(int, re.findall(r'\d+', port_num[0])))[0])
        result[address] = port_info

    result = OrderedDict(sorted(result.items(), key=lambda address: address[0]))
    # Start converting data to Markdown
    for address in result:
        if not options.print_empty and len(result[address]) == 0:
            continue

        if options.hs != 0:
            md += "%s %s\n\n" % ('#' * options.hs, address)
        md += "| %s |" % " | ".join(columns)
        md += "\n"

        # Adding +2 for 1 space on left and right sides
        md += "|%s|" % "|".join(map(lambda s: '-' * (len(s) + 2), columns))
        md += "\n"

        for port_info in result[address]:
            md += "| %s |" % " | ".join(port_info)
            md += "\n"

        md += "\n\n"

    print()
    print()
    print(md)
