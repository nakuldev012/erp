import mysql.connector
import json

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "MyStrongPassword1234$",
    "database": "kieterp",
}

# Connect to the database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Get a list of all tables in the database
    cursor.execute("SHOW TABLES")
    tables = [table['Tables_in_kieterp'] for table in cursor.fetchall()]

    # Create a dictionary to store data from all tables
    all_data = {}

    # Extract data from each table and store it in the dictionary
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()
        all_data[table] = data

    # Write the aggregated data to a single JSON file
    with open("kieterp_data.json", "w") as json_file:
        json.dump(all_data, json_file, default=str)

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
