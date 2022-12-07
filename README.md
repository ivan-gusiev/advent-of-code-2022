# Advent of Code 2022

Python implementation.

### Just

The easiest way to do develop and run this code is using the `justfile`.
For this, you need `just` installed (e.g. `brew install just`).
If you do, type `just` in the repo directory to see the available commands.

```bash
❯ just
Available recipes:
    default
    new day x          # sets up boilerplate for new day EXAMPLE just new day 7
    pip-init           # initializes Python environment
    pip-upgrade        # upgrades dependencies
    run day x *args='' # runs a selected day EXAMPLE just run day 5 --paint
    run-all *args=''   # runs all days
```

If you don't want to use `just`, see the contents below.

### Setup

```bash
pip install -r requirements-dev.txt # setup dev requirements
```
Note: requirements.txt is empty, because this is not intended to be an actual package.

Upgrade packages:
```bash
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