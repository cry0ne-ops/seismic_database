import pandas as pd
import sqlite3

df = pd.read_excel("cleaned_full_seismic_dataset.xlsx")

conn = sqlite3.connect("seismic_database.db")

df.to_sql("barangay_halls", conn, if_exists="replace", index=False)

conn.close()

print("Database created!")
