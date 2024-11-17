import pyodbc
import logging

# Configure logging to write errors to a file
logging.basicConfig(
    filename="db_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Replace these with your own database connection details
server = 'JAVERIASLAPTOP\\SQLSERVER1'
database = 'CineFlix'
use_windows_authentication = False
username = 'sa'
password = 'f4d238ea'

# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # # Establish a connection to the database
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # # INSERT: 
    # new_customer = (
    #     'Premium',  # CustomerRole
    #     'Anna Brown',  # CustomerName
    #     'Female',  # CustomerGender
    #     '1995-06-10',  # CustomerDateOfBirth
    #     '99 Elm St',  # CustomerAddress
    #     'Greenfield',  # CustomerCity
    #     'USA'  # CustomerCountry
    # )

    # insert_customer_query = """
    #     INSERT INTO Customer (CustomerRole, CustomerName, CustomerGender, CustomerDateOfBirth, 
    #                         CustomerAddress, CustomerCity, CustomerCountry)
    #     OUTPUT INSERTED.CustomerID  -- This returns the auto-generated CustomerID
    #     VALUES (?, ?, ?, ?, ?, ?, ?)
    # """

    # cursor.execute(insert_customer_query, new_customer)
    # new_customer_id = cursor.fetchone()[0]  # Get the CustomerID of the new customer
    # connection.commit()  # Commit the transaction
    # print(f"New customer added successfully with CustomerID {new_customer_id}.")

    # # Step 2: Add an account for the new customer using the generated CustomerID
    # new_account = ('annabrown@example.com', 'SecurePass2024!', new_customer_id, None)
    # insert_account_query = """
    #     INSERT INTO Account ([Email], [Password], [CustomerID], [EmployeeID])
    #     VALUES (?, ?, ?, ?)
    # """

    # cursor.execute(insert_account_query, new_account)
    # connection.commit()
    # print("New account added successfully.")


    # # UPDATE:
    # # Now update the account details using the fetched CustomerID
    # new_email = 'annabrown_updated@example.com'
    # new_password = 'UpdatedPass2024!'

    # update_account_query = """
    #     UPDATE Account
    #     SET Email = ?, Password = ?
    #     WHERE CustomerID = (select CustomerID from Customer where CustomerName = 'Anna Brown')
    # """
    # cursor.execute(update_account_query, new_email, new_password)
    # connection.commit()  # Commit the transaction
    # print("Account Information Updated")
    
    # # DELETE
    # email = 'annabrown_updated@example.com'
    # delete_account_query = """
    #     DELETE from Account 
    #     WHERE Email = ?
    # """

    # cursor.execute(delete_account_query, email)
    # connection.commit()
    # print("Account deleted successfully")

except Exception as e:
    error_message = f"An error occurred: {e}"
    print(error_message)
    logging.error(error_message)

finally:
    # Ensure resources are released properly
    try:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    except Exception as cleanup_error:
        cleanup_message = f"Error during cleanup: {cleanup_error}"
        print(cleanup_message)
        logging.error(cleanup_message)






