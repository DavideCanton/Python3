@echo off
set P_FILE=D:\sample.txt
set P_DIR=./res
python3 create_index.py "%P_FILE%" "%P_DIR%"
python3 process_cities.py "%P_FILE%" "%P_DIR%"
