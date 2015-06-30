rem should be executed from the main directory
mkdir docs

echo "---- Generating GraphModels --------------"
mkdir docs\GraphModels
python manage.py  graph_models --pygraphviz -a -g -o docs\GraphModels\my_project_visualized.jpg
python manage.py  graph_models --pygraphviz -a -g -o docs\GraphModels\my_project_visualized.svg

echo "---- Generating SchemaSpy ----------------"
java -jar c:\S\SchemaSpy\schemaSpy_5.0.0.jar -t c:\S\SchemaSpy\sqlite3.properties -db db.sqlite3 -sso -o docs\SchemaSpy