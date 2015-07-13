@ echo "---- Generating SchemaSpy ----------------"
@ SET SQLITE_PROPS=%SCRIBETOOLS%/SchemaSpy/sqlite.properties
schemaspy -t %SQLITE_PROPS% -db db.sqlite3  -sso -o docs\SchemaSpy
