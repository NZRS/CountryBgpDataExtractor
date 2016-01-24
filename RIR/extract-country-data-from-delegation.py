#!/usr/bin/env python

import csv
from collections import defaultdict
import argparse
import glob
import json

parser = argparse.ArgumentParser("Parses the delegation files from the RIR to extract ASes and prefixes belonging to a country")
parser.add_argument('--country', required=True, action='append',
                    help="Country to extract data for")
args = parser.parse_args()

print("Selected countries %s" % args.country)

# Each file has a line that looks like this
# apnic|JP|asn|173|1|20020801|allocated

as_country = set([cc.upper() for cc in args.country])
as_list = defaultdict(list)
prefix_list = defaultdict(list)
for rir_file in glob.glob("delegated-*-latest"):
    with open(rir_file, 'rb') as csvfile:
        csvin = csv.reader(csvfile, delimiter='|')

        for row in csvin:
            if row[-1] == 'allocated':
                if row[2] == 'asn' and row[1] in as_country:
                    as_list[row[1]].append(row[3])
                if row[2] == 'ipv4' and row[1] in as_country:
                    prefix = row[3]
                    mask = 32 - (int(row[4]) - 1).bit_length()
                    prefix = "{0}/{1}".format(row[3], mask)
                    prefix_list[row[1]].append(prefix)


with open('../data/AS-from-rir.json', 'wb') as as_file:
    json.dump(as_list, as_file)

with open('../data/networks-from-rir.json', 'wb') as net_file:
    json.dump(prefix_list, net_file)

