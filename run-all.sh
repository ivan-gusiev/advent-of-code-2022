for script_file in ./aoc2022/day*.py
do
    python -m $(echo $script_file | sed 's/.py//g' | sed 's|^./||g' | sed 's|/|.|g') "$@"
done