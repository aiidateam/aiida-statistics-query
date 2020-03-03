# Compute statistics of AiiDA databases

This repository contains a [script](https://raw.githubusercontent.com/ltalirz/aiida-statistics-query/master/statistics.py) that computes statistics on AiiDA databases for reporting purposes.

The script is designed to work with AiiDA >= 0.10 (tested on aiida-core 0.10, 0.12.4, 1.0.0b6 and 1.1.0), both under python 2 and 3.

Typical run times are 10-20s per 1 million nodes in your AiiDA database.

## Usage

```bash
./statistics.py
```

## Development

Set up pre-commit hooks for python2/3 compatibility, code formatting & linting.
```bash
pip install -e .[pre-commit]
```
