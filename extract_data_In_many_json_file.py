import mysql.connector
import json

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "harry",
    "password": "MyStrongPassword1234$",
    "database": "kieterp2",
}

# Connect to the database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Get a list of all tables in the database
    cursor.execute("SHOW TABLES")
    tables = [table['Tables_in_kieterp2'] for table in cursor.fetchall()]

    # Extract data from each table and write to JSON files
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()

        with open(f"{table}.json", "w") as json_file:
            json.dump(data, json_file, default=str)

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
