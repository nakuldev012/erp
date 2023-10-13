import mysql.connector
import json

import mysql.connector
import json

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "harry",
    "password": "MyStrongPassword1234$",
    "database": "abc",
}

# Connect to the database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Read the JSON data from the file
    with open("erp_backend/mastertableconfig_masterconfig.json", "r") as json_file:
        data = json.load(json_file)

    # Assuming you want to insert the data into a table named "your_table"
    target_table = "mastertableconfig_masterconfig"

    # Iterate through the JSON data and insert it into the MySQL table
    for row in data:
        columns = ", ".join(row.keys())
        values = ", ".join(["%s"] * len(row))
        insert_query = f"INSERT INTO {target_table} ({columns}) VALUES ({values})"
        cursor.execute(insert_query, tuple(row.values()))

    # Commit the changes to the database
    conn.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
