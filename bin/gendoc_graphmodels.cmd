echo "---- Generating GraphModels --------------"
mkdir docs\GraphModels
python manage.py  graph_models --pygraphviz -a -g -o docs\GraphModels\my_project_visualized.jpg
python manage.py  graph_models --pygraphviz -a -g -o docs\GraphModels\my_project_visualized.svg
