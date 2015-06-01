#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "northcoast.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcode_re = re.compile(r'^[A-Z0-9]+ ?[A-Z0-9]+$')


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", 'Crescent', 'Dale', 'Glen', 'Green', 'Gardens',
            'Walk', 'Way', 'Park', 'Parade', 'Manor', 'Meadow', 'Lodge', 'Heights', 'Grove',
            'Close', 'Quay']


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def audit_postcode(bad_postcodes, postcode):
    m = postcode_re.search(postcode)
    if not m:
        bad_postcodes.add(postcode)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    bad_postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                v = tag.attrib['v']
                if is_street_name(tag) and ' ' in v:
                    audit_street_type(street_types, v)
                if is_postcode(tag):
                    audit_postcode(bad_postcodes, v)

    return street_types, bad_postcodes


def test():
    st_types, bad_postcodes = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    pprint.pprint(bad_postcodes)


if __name__ == '__main__':
    test()
