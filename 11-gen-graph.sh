# python3.8 10-output_dot.py | neato -v -Goverlap=false -Gsplines=true -Tps -o 12-graph.ps && atril 12-graph.ps --preview
python3.8 10-output_dot.py | dot -Tps -o 12-graph.ps && atril 12-graph.ps --preview
