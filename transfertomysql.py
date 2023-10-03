# import json
# import mysql.connector

# # Read the JSON file
# with open('data.json', 'r') as json_file:
#     data = json.load(json_file)

# # Establish a connection to your MySQL database
# db_connection = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='rooterp',
#     database='erp3'
# )

# # Create a cursor to interact with the database
# cursor = db_connection.cursor()
# import ipdb;
# ipdb.set_trace()

# # Iterate through each table and insert data
# for table_name, table_data in data.items():
#     for item in table_data:
#          # Modify the column names to match the structure of your JSON data
#         columns = ', '.join(item.keys())
#         placeholders = ', '.join(['%s'] * len(item))
#         values = tuple(item.values())

#         query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#         cursor.execute(query, values)

# # Commit the changes to the database
# db_connection.commit()

# # Close the cursor and database connection
# cursor.close()
# db_connection.close()




import json
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

# Open and read the JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Define your MySQL database connection parameters
db_config = {
    'host': 'localhost',
    'database': 'kieterp',
    'user': 'root',
    'password': 'rooterp',
}


# Create a connection pool to manage database connections
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Loop through the 'user_account' data and insert it into the MySQL table
for user_account in data['user_account']:
    cursor.execute("INSERT INTO user_account (id, password, last_login, is_superuser, email, first_name, last_name, phone_number, is_verified, is_active,is_admin, user_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", user_account)

# Loop through the 'user_account_groups' data and insert it into the MySQL table
for user_group in data['user_account_groups']:
    cursor.execute("INSERT INTO user_account_groups (id, account_id, group_id) VALUES (%s, %s, %s)", user_group)

# Loop through the 'user_account_user_permissions' data and insert it into the MySQL table
for user_perm in data['user_account_user_permissions']:
    cursor.execute("INSERT INTO user_account_user_permissions (user_id, permission_id) VALUES (%s, %s)", user_perm)

# Loop through the 'django_admin_log' data and insert it into the MySQL table
# for admin_log in data['django_admin_log']:
#     cursor.execute("INSERT INTO django_admin_log (id, object_id, object_repr, content_type_id, change_message, user_id, action_flag, action_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", admin_log)

# Loop through the 'oauth2_provider_refreshtoken' data and insert it into the MySQL table
for refresh_token in data['oauth2_provider_refreshtoken']:
    cursor.execute("INSERT INTO oauth2_provider_refreshtoken (id, token, access_token_id, user_id, application_id, created, updated, revoked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", refresh_token)

# Loop through the 'oauth2_provider_accesstoken' data and insert it into the MySQL table
for access_token in data['oauth2_provider_accesstoken']:
    cursor.execute("INSERT INTO oauth2_provider_accesstoken (id, token, expires, scope, application_id, user_id, created, updated, refresh_token_id, jti) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", access_token)

# Loop through the 'oauth2_provider_application' data and insert it into the MySQL table
for application in data['oauth2_provider_application']:
    cursor.execute("INSERT INTO oauth2_provider_application (id, client_id, user_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, created, updated, uuid, owner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", application)

# Loop through the 'employee_employee' data and insert it into the MySQL table
for employee in data['employee_employee']:
    cursor.execute("INSERT INTO employee_employee (id, name, hire_date, department_id) VALUES (%s, %s, %s, %s)", employee)

# Loop through the 'mastertableconfig_organization' data and insert it into the MySQL table
for organization in data['mastertableconfig_organization']:
    cursor.execute("INSERT INTO mastertableconfig_organization (id, name) VALUES (%s, %s)", organization)

# Commit the changes and close the database connection
conn.commit()
conn.close()