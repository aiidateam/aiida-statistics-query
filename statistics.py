#!/usr/bin/env python
# pylint: disable=import-outside-toplevel
from __future__ import absolute_import
from __future__ import print_function
import json
from datetime import datetime
from collections import Counter
from aiida import __version__ as AIIDA_VERSION
from distutils.version import StrictVersion

OUTFILE = 'statistics.json'


def get_statistics():
    if StrictVersion(AIIDA_VERSION) >= StrictVersion('1.0.0'):
        results = query_aiida_1()
    else:
        pass

    data = [tuple(item) for item in results]
    # Need to convert to tuple to make them hashable
    count = list(dict(Counter(data)).items())

    return {'nodes_count': count}


def query_aiida_1():
    """Statistics query for AiiDA 1.0 and above."""
    from aiida import load_profile
    from aiida.orm import QueryBuilder, Node

    load_profile()

    qb = QueryBuilder()

    qb.append(Node, project=['node_type', 'process_type'])
    return qb.all()


print(("{} Starting query".format(datetime.now())))

with open(OUTFILE, 'w') as handle:
    json.dump(get_statistics(), handle, indent=2)

print(("{} Statistics written to '{}'".format(datetime.now(), OUTFILE)))
