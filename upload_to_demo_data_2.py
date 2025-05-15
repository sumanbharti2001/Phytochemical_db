import pandas as pd
import pymysql

# --- 1. File path and CSV loading ---
file_path = r"C:\Users\priya\OneDrive\Desktop\phytochem-backend\Demo data new.csv"
df = pd.read_csv(file_path, encoding='latin1')  # Handles special characters

# Normalize column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_')  # Replace slashes with underscores

# Debug: Check the column names
print(df.columns)

# --- 2. Replace NaN with None ---
df = df.applymap(lambda x: None if pd.isna(x) else x)

# --- 3. MySQL connection ---
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='natural_products_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

cursor = connection.cursor()

# --- 4. Create table if not exists ---
create_table_sql = """
CREATE TABLE IF NOT EXISTS demo_data_2 (
    Species_name TEXT,
    Compounds TEXT,
    Amount TEXT,
    Time_of_data_collection TEXT,
    Plant_part TEXT,
    Identification_method TEXT,
    Profile TEXT,
    Profile_base TEXT,
    DOI_number TEXT,
    Time_of_publication TEXT,
    Location TEXT,
    Country TEXT,
    Essential_oil_extraction_method TEXT,
    Development_stage TEXT,
    Season_month TEXT,
    Experimental_condition TEXT,
    Species_variety TEXT,
    Plant_Sample TEXT,
    Journals_name TEXT
)
"""
cursor.execute(create_table_sql)

# --- 5. Insert new rows ---
rows_inserted = 0

for index, row in df.iterrows():
    # Print the current row being inserted (for debugging)
    print(f"Inserting row {index}: {row.to_dict()}")
    
    try:
        cursor.execute("""
            INSERT INTO demo_data_2 (
                Species_name, Compounds, Amount, Time_of_data_collection,
                Plant_part, Identification_method, Profile, Profile_base,
                DOI_number, Time_of_publication, Location, Country,
                Essential_oil_extraction_method, Development_stage, Season_month,
                Experimental_condition, Species_variety, Plant_Sample, Journals_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Species_name'], row['Compounds'], row['Amount'], row['Time_of_data_collection'],
            row['Plant_part'], row['Identification_method'], row['Profile'], row['Profile_base'],
            row['DOI_number'], row['Time_of_publication'], row['Location'], row['Country'],
            row['Essential_oil_extraction_method'], row['Development_stage'], row['Season_month'],
            row['Experimental_condition'], row['Species_variety'], row['Plant_Sample'], row['Journals_name']
        ))
        rows_inserted += 1  # ✅ Count successful inserts
    except Exception as e:
        print(f"❌ Row {index} insert failed: {e}")
        print("Row data:", row.to_dict())

# --- 6. Finalize ---
connection.commit()
cursor.close()
connection.close()

# ✅ Show number of rows inserted
print(f"✅ {rows_inserted} rows were added to demo_data_2")
