#!/usr/bin/python2.7

import rrdtool
import os
import argparse
import sys

# Command line arguments
parser = argparse.ArgumentParser(description='Process inbound and outbound datatraffic for specified domain')
parser.add_argument('-c','--customer-domain', metavar='Customer-Domain', required=True,
                   help='domain name of customer from CloudStack')
parser.add_argument('-r', '--in-traffic', metavar='Traffic-Rx', type=int,
                   help='number of bytes for In Traffic')
parser.add_argument('-s', '--out-traffic', metavar='Traffic-Tx', type=int,
                   help='number of bytes for Out Traffic')
parser.add_argument('-o', '--oper-status', metavar='Oper-Status', type=int, choices=[0,1], default=1,
                   help='ifOperStatus, whether the interface has successfully formed a link')
parser.add_argument('-d', '--rrd-directory', metavar='RRD-Directory', default = "rrd-datastore",
				           help='path (directory) to store rrd file')
parser.add_argument('-v', '--verbose', action="store_true",
        				   help='increase output verbosity')

args = parser.parse_args()

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.rrd_directory)
rrd_file = os.path.join(directory, args.customer_domain + ".rrd")

# Creating Directory, if not exist
if not os.path.exists(directory):
    os.makedirs(directory)
    if args.verbose: print "Directory created!"
else:
    if args.verbose: print "Directory already exists."

if args.verbose: print "RRD file path: %s" %(rrd_file)

# Creating database (rrd), if not exist else update(v)
if not os.path.exists(rrd_file):
    if args.verbose: print "Creating rrd file now...",
    rrdtool.create(str(rrd_file),
      '--step', '300',
      '--no-overwrite',
      'DS:ifInOctets:COUNTER:900:0:18446744073709551615',
      'DS:ifOutOctets:COUNTER:900:0:18446744073709551615',
      'DS:ifOperStatus:GAUGE:900:0:100',
      'RRA:MAX:0.5:1:288',
      'RRA:MIN:0.5:1:288',
      'RRA:AVERAGE:0.5:1:288',
      'RRA:AVERAGE:0.5:6:336',
      'RRA:AVERAGE:0.5:24:360',
      'RRA:AVERAGE:0.5:288:365')
    if args.verbose: print "created!"
else:
    # Command: rrdtool update(v) network_usage_db.rrd --template in-trafic:out-trafic N:10:20
    if args.verbose:
        print "RRD already exists."
        return_val = rrdtool.updatev(str(rrd_file), 'N:%s:%s:%s' %(args.in_traffic, args.out_traffic, args.oper_status))
        print return_val
    else:
        return_val = rrdtool.update(str(rrd_file), 'N:%s:%s:%s' %(args.in_traffic, args.out_traffic, args.oper_status))
