#!/usr/bin/env python

from collections import OrderedDict, defaultdict
import json
import ipaddress
import csv
import gzip

verbose = True


def prefix_in_country(p):
    p = unicode(p)
    overlaps = False
    overlap_country = ''
    num_slash_24 = 0
    try:
        net_p = ipaddress.ip_network(p)
        num_slash_24 = int(net_p.num_addresses/256)
        for country in net_data:
            for prefix in net_data[country]:
                overlaps = prefix.overlaps(net_p)
                overlap_country = country
                if overlaps:
                    break
    except ValueError:
        print "ERR: prefix %s caused exception" % p

    return dict(overlap=overlaps, count24=num_slash_24, country=overlap_country)


def as_in_country(asn):
    found = False
    for country in as_data:
        found = found or asn in as_data[country]

    return found


with open('../data/AS-from-rir.json', 'rb') as as_file:
    as_data = json.load(as_file)

net_data = defaultdict(list)
with open('../data/networks-from-rir.json', 'rb') as net_file:
    net_raw_data = json.load(net_file)

    for country in net_raw_data:
        # Prepare ipaddress objects to speed up things later
        for net in net_raw_data[country]:
            net_data[country].append(ipaddress.ip_network(net))

# The key is going to be a string representing an AS-PATH, and the values a
# list of prefixes sharing that common AS-PATH
aspath_set = defaultdict(list)
prefix_list = {}
line_cnt = 0
with gzip.open('../data/prefix-aspath.txt.gz', 'rb') as aspath_file:
    aspath_list = csv.reader(aspath_file, delimiter='|')

    for aspath in aspath_list:
        # Special case to filter out some prefixes we don't want to see.
        if aspath[0] == "0.0.0.0/0":
            print "ERROR: Skipping default route"
            continue
        if line_cnt % 100000 == 0:
            print "{} paths processed".format(line_cnt)
        # XXX Just for testing
        if line_cnt > 1000000:
            break
        # Test if the origin AS is from the country we are interested on
        origin = aspath[1].split(' ')[-1]
        if as_in_country(origin):
            netmask = int(aspath[0].split('/')[-1])
            if netmask <= 24:
                aspath_set[aspath[1]].append(aspath[0])
            else:
                print "ERROR: Skipping prefix {} with mask smaller to 24".format(aspath[0])
        else:   # If not, test if the prefix corresponds to the country
            status = prefix_list.get(aspath[0], None)
            if status is None:  # The entry doesnt exist
                prefix_list[aspath[0]] = prefix_in_country(aspath[0])
            elif status['overlap']:  # Entry exists and it's a prefix we want
                aspath_set[aspath[1]].append(aspath[0])
        line_cnt += 1

sel_aspath = []
for aspath, prefix_list in aspath_set.iteritems():
    sel_aspath.append({'path': list(OrderedDict.fromkeys(aspath.split(' '))),
                      'prefixes': prefix_list})

with open('../data/country-aspath-selection.json', 'wb') as aspath_file:
    json.dump(dict(aspath=sel_aspath), aspath_file)

