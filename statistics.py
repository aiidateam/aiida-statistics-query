#!/usr/bin/env runaiida
# pylint: disable=import-outside-toplevel
"""
Script to get anonymous statistics on the nodes stored in an AiiDA profile.

This returns the (process) types of nodes in the DB and their count.

*NOTE*: Simply execute ./statistics.py in your virtual environment to get the results for your 
default AiiDA profile; otherwise, run `verdi -p PROFILE_NAME run statistics.py`. 
"""
from __future__ import absolute_import
from __future__ import print_function
import json
from datetime import datetime
from collections import Counter
from aiida import __version__ as AIIDA_VERSION
from distutils.version import StrictVersion

OUTFILE = 'statistics.json'


def get_statistics():
    if StrictVersion(AIIDA_VERSION) >= StrictVersion('1.0.0b1'):
        results = query_aiida_1()
    else:
        results = query_aiida_0x()

    data = [tuple(item) for item in results]
    # Need to convert to tuple to make them hashable
    count = list(dict(Counter(data)).items())

    return {'nodes_count': count, 'aiida_version': AIIDA_VERSION}


def query_aiida_0x():
    """Statistics query for AiiDA 0.x (tested on AiiDA 0.10 and 0.12.4)."""
    from aiida.orm.querybuilder import QueryBuilder
    from aiida.orm.node import Node

    qb = QueryBuilder()

    qb.append(Node, project=['type'])
    return qb.all()


def query_aiida_1():
    """Statistics query for AiiDA 1.0 and above (tested on AiiDA 1.0b6 and 1.1)."""
    from aiida.orm import QueryBuilder, Node

    qb = QueryBuilder()

    qb.append(Node, project=['node_type', 'process_type'])
    return qb.all()


print(("{} Starting query".format(datetime.now())))

with open(OUTFILE, 'w') as handle:
    json.dump(get_statistics(), handle, indent=2)

print(("{} Statistics written to '{}'".format(datetime.now(), OUTFILE)))
