set positional-arguments := true

default:
    @just --list

# initializes Python environment
pip-init:
    pip install -r requirements-dev.txt

# upgrades dependencies
pip-upgrade:
    sed -i '' 's/[~=]=/>=/' requirements-dev.txt
    pip install -U -r requirements-dev.txt
    pip freeze | sed 's/==/~=/' > requirements-dev.txt

# runs a selected day EXAMPLE just run day 5 --paint
run day x *args='':
    python -m aoc2022.day{{ x }} $@

# runs all days
run-all *args='':
    sh ./run-all.sh $@

# sets up boilerplate for new day EXAMPLE just new day 7
new day x:
    sh ./day.sh day{{ x }}

# format code (Python and the justfile)
fmt:
    black .
    @just --fmt --unstable
