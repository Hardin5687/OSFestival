import sqlite3

db_path = "festival.db"
output_file = "festival_export.sql"

conn = sqlite3.connect(db_path)
with open(output_file, "w", encoding="utf-8") as f:
    for line in conn.iterdump():      # dumps entire database as SQL text
        f.write(f"{line}\n")

conn.close()
print("Export complete → festival_export.sql created.")
    