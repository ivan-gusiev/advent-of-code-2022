#!/bin/bash

cp ./.templates/template.py "./aoc2022/$1.py"
cp ./.templates/template.txt "./input/$1.txt"
cp ./.templates/template-test.txt "./input/$1-test.txt"
echo "$1 initialized!"
