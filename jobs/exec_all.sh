#!/bin/sh
P_FILE=D:\sample.txt
P_DIR=D:\cartella_prova_2
if [ -d "$P_DIR" ]
then
    echo "ATTENZIONE LA CARTELLA ESISTE!!!"    
fi
python3 create_index.py "$P_FILE" "$P_DIR"
python3 process_cities.py "$P_FILE" "$P_DIR"
