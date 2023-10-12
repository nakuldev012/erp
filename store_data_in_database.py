import mysql.connector
import json

# Database connection configuration for the source database (kieterp)
# source_db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "MyStrongPassword1234$",
#     "database": "kieterp",
# }

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
    with open("mastertableconfig_masterconfig.json", "r") as json_file:
        data = json.load(json_file)

    # Assuming you want to insert the data into a table named "your_table"
    target_table = "mastertableconfig_masterconfig"

    # Iterate through the JSON data and insert it into the MySQL table
    for row in data:
        columns = ', '.join(row.keys())
        values = ', '.join(['%s'] * len(row))
        insert_query = f"INSERT INTO {target_table} ({columns}) VALUES ({values})"
        cursor.execute(insert_query, tuple(row.values()))

    # Commit the changes to the database
    conn.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()

# Target database connection configuration
# target_db_config = {
#     "host": "target_host",
#     "user": "target_username",
#     "password": "target_password",
#     "database": "target_database",
# }

# try:
#     # # Connect to the source database (kieterp)
#     # source_conn = mysql.connector.connect(**source_db_config)
#     # source_cursor = source_conn.cursor(dictionary=True)

#     # Read the JSON data from the file
#     with open("mastertableconfig_masterconfig.json", "r") as json_file:
#         data = json.load(json_file)

#     # Connect to the target database
#     target_conn = mysql.connector.connect(**target_db_config)
#     target_cursor = target_conn.cursor()

#     # Iterate through the tables in the JSON data
#     for table, table_data in data.items():
#         for row in table_data:
#             # Insert data into the target database
#             insert_query = f"INSERT INTO {table} ({', '.join(row.keys())}) VALUES ({', '.join(['%s'] * len(row.values()))})"
#             target_cursor.execute(insert_query, list(row.values()))

#     # Commit changes to the target database
#     target_conn.commit()

# except mysql.connector.Error as e:
#     print(f"Error: {e}")
# # finally:
# #     source_cursor.close()
# #     source_conn.close()
#     target_cursor.close()
#     target_conn.close()
