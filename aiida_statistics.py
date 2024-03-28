# pylint: disable=import-outside-toplevel
"""
Script to collect anonymous statistics on the nodes stored in an AiiDA profile.

This counts the number of nodes in your profile, split by (process) type.

Usage: Execute `verdi run aiida_statistics.py` in your AiiDA python environment for statistics on the default AiiDA
profile.
    Execute `verdi -p PROFILE_NAME run aiida_statistics.py` for statistics on any other AiiDA profile.

Note: This script is designed to support AiiDA versions >= 0.10 and runs both under python 2 and 3.
"""

from __future__ import absolute_import, print_function

import json
from collections import Counter
from datetime import datetime

from aiida import __version__ as AIIDA_VERSION
from packaging.version import parse

OUTFILE = "statistics.json"


def get_statistics():
    if parse(AIIDA_VERSION) >= parse("1.0.0b1"):
        results = query_aiida()
    else:
        results = query_aiida_0x()

    data = [tuple(item) for item in results]
    # Need to convert to tuple to make them hashable
    count = list(dict(Counter(data)).items())

    return {"nodes_count": count, "aiida_version": AIIDA_VERSION}


def query_aiida_0x():
    """Statistics query for AiiDA 0.x (tested on AiiDA 0.10 and 0.12.4)."""
    from aiida.orm.node import Node
    from aiida.orm.querybuilder import QueryBuilder

    qb = QueryBuilder()

    qb.append(Node, project=["type"])
    return qb.all()


def query_aiida():
    """Statistics query for AiiDA 1.0 and above (tested on AiiDA 1.0b6, 1.1, and 2.5)."""
    from aiida.orm import Node, QueryBuilder

    qb = QueryBuilder()

    qb.append(
        Node,
        project=[
            "node_type",
            "process_type",
            "attributes.version.core",
            "attributes.version.plugin",
        ],
    )
    return qb.all()


print(("{} Starting query".format(datetime.now())))

with open(OUTFILE, "w") as handle:
    json.dump(get_statistics(), handle, indent=2)

print(("{} Statistics written to '{}'".format(datetime.now(), OUTFILE)))
