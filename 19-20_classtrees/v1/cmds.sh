python3 process.py cs.json | dot -Tps -o graph.ps && atril graph.ps --preview
convert -density 150 -geometry 100% -flatten graph.ps img.png
