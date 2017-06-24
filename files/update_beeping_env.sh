#!/bin/bash
CONFIG_JSON=$(files/yaml2json.py < files/beeping.yaml)
cp files/beeping_exporter.env.tpl beeping_exporter.env
echo "BEEPING_CHECKS=$CONFIG_JSON" >> beeping_exporter.env

