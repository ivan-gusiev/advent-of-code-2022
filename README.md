# Advent of Code 2022

Python implementation.

### Setup

```
pip install -r requirements-dev.txt # setup dev requirements
```
Note: requirements.txt is empty, because this is not intended to be an actual package.

Upgrade packages:
```
sed -i '' 's/[~=]=/>=/' requirements-dev.txt
pip install -U -r requirements-dev.txt
pip freeze | sed 's/==/~=/' > requirements-dev.txt
```

### Run

```bash
python -m aoc2022.day1 # runs day 1, parts 1 and 2
python -m aoc2022.day5 --paint # runs day 5, plus renders a visualization
```

### New day

```bash
./day.sh day7 # initializes day 7 (see ./.templates)
```