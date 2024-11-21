import pyodbc
import logging
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys


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

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('MainScreen.ui', self)
    
        # Connect buttons
        self.RegisterButton.clicked.connect(self.open_role_selection_screen)
        self.LoginButton.clicked.connect(self.open_login_screen)

    def open_role_selection_screen(self):
        self.role_selection_screen = RegisterOptions()
        self.role_selection_screen.show()
        self.close()

    def open_login_screen(self):
        self.login_screen = LoginScreen()
        self.login_screen.show()
        self.close()

class RegisterOptions(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterOptions, self).__init__()
        uic.loadUi('Register Options.ui', self)

        # Connect role buttons
        self.AdminRole.clicked.connect(self.open_admin_register_screen)
        self.CMRole.clicked.connect(self.open_manager_register_screen)
        self.PViewerRole.clicked.connect(self.open_premium_register_screen)
        self.ViewerRole.clicked.connect(self.open_normal_register_screen)

        # Connect login instead button
        self.AlreadyLogin.clicked.connect(self.open_login_screen)

    def open_admin_register_screen(self):
        self.register_screen = RegisterScreenAsAdmin()
        self.register_screen.show()
        self.close()

    def open_manager_register_screen(self):
        self.register_screen = RegisterScreenAsCinemaManager()
        self.register_screen.show()
        self.close()

    def open_premium_register_screen(self):
        self.register_screen = RegisterScreenAsPremiumViewer()
        self.register_screen.show()
        self.close()

    def open_normal_register_screen(self):
        self.register_screen = RegisterScreenAsViewer() 
        self.register_screen.show()
        self.close()

    def open_login_screen(self):
        self.login_screen = LoginScreen()
        self.login_screen.show()
        self.close()

class RegisterScreenAsAdmin(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsAdmin, self).__init__()
        uic.loadUi('RegisterAsAdministrator.ui', self)
        
        # Connect register button
        self.RegisterButton_Admin.clicked.connect(self.register_user)

    def register_user(self):
        # Collecting user inputs
        name = self.lineEditname.text()
        email = self.lineEditemail.text()
        password = self.lineEditpassword.text()
        job_title = self.lineEditposition.text()
        department = self.lineEditdepartment.text()
        experience = self.lineEditexperience.text()

        if not (name and email and password and job_title and department and experience):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            # Database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            # Insert into Employee table
            cursor.execute("""
                INSERT INTO Employee ([EmployeeName], [EmployeeDepartment], [EmployeePosition], [EmployeeExperience])
                VALUES (?, ?, ?, ?)
            """, name, department, job_title, experience)
            connection.commit()

            # # Retrieve the generated Employee ID
            # cursor.execute("SELECT SCOPE_IDENTITY()")  # For SQL Server
            # employee_id = cursor.fetchone()[0]

            cursor.execute("SELECT @@IDENTITY")
            employee_id = cursor.fetchone()[0]
            logging.info(f"Employee ID retrieved using @@IDENTITY: {employee_id}")

            if not employee_id:
                raise Exception("Failed to retrieve Employee ID")

            # Insert into Account table
            cursor.execute("""
                INSERT INTO Account ([Email], [Password], [EmployeeID])
                VALUES (?, ?, ?)
            """, email, password, employee_id)
            connection.commit()

            cursor.close()
            connection.close()

            # Success message
            QtWidgets.QMessageBox.information(self, "Success", "Registration successful!")
            self.close()

        except Exception as e:
            logging.error(f"Error registering user: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Registration failed.")


class RegisterScreenAsCinemaManager(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsCinemaManager, self).__init__()
        uic.loadUi('RegisterAsCinemaManager.ui', self)
        
        # Connect register button for manager info
        self.nextButton.clicked.connect(self.register_manager_info)

    def register_manager_info(self):
        # Collecting user inputs for manager info
        name = self.lineEditname.text()
        email = self.lineEditemail.text()
        password = self.lineEditpassword.text()
        job_title = self.lineEditposition.text()
        department = self.lineEditdepartment.text()
        experience = self.lineEditexperience.text()

        if not (name and email and password and job_title and department and experience):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            # Database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()


            # Check if email already exists
            cursor.execute("SELECT Email FROM Account WHERE Email = ?", email)
            if cursor.fetchone():
                raise Exception("Email already exists. Please use a different email.")

            # Insert into Employee table
            cursor.execute("""
                INSERT INTO Employee ([EmployeeName], [EmployeeDepartment], [EmployeePosition], [EmployeeExperience])
                VALUES (?, ?, ?, ?)
            """, name, department, job_title, experience)
            connection.commit()

            # Retrieve the generated Employee ID
            cursor.execute("SELECT @@IDENTITY")  # Retrieve last inserted identity
            employee_id = cursor.fetchone()[0]
            logging.info(f"Employee ID retrieved using @@IDENTITY: {employee_id}")

            if not employee_id:
                raise Exception("Failed to retrieve Employee ID")

            # Insert into Account table
            cursor.execute("""
                INSERT INTO Account ([Email], [Password], [EmployeeID])
                VALUES (?, ?, ?)
            """, email, password, employee_id)
            connection.commit()

            # Close the database connection
            cursor.close()
            connection.close()

            # Success message
            QtWidgets.QMessageBox.information(self, "Success", "Manager registration successful!")
            self.open_cinema_info_screen(employee_id)  # Move to cinema info screen

        except Exception as e:
            logging.error(f"Error registering manager: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Manager registration failed.")

    def open_cinema_info_screen(self, employee_id):
        # Switch to the Cinema Info Screen
        self.cinema_info_screen = CinemaInfoScreen(employee_id)  # Pass employee_id to next screen
        self.cinema_info_screen.show()
        self.close()  # Close the current screen


class CinemaInfoScreen(QtWidgets.QMainWindow):
    def __init__(self, employee_id):
        super(CinemaInfoScreen, self).__init__()
        uic.loadUi('RegisterAsCinemaManager - second screen.ui', self)

        # Store employee_id for associating the manager with the cinema
        self.employee_id = employee_id

        # Connect register button for cinema info
        self.cinemaRegisterButton.clicked.connect(self.register_cinema_info)

    def register_cinema_info(self):
        # Collecting user inputs for cinema info
        cinema_name = self.lineEditcname.text()
        cinema_capacity = self.lineEditcapacity.text()
        cinema_address = self.lineEditcaddress.text()
        cinema_city = self.lineEditccity.text()
        cinema_country = self.lineEditccountry.text()
        cinema_website = self.lineEditcwebsite.text()

        if not (cinema_name and cinema_capacity and cinema_address and cinema_city and cinema_country and cinema_website):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            # Database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Insert into Cinema table (assumes CinemaID is auto-generated)
            cursor.execute("""
                INSERT INTO Cinema ([Cinema_Name], [Capacity], [Address], [City], [Country], [Website_Link])
                VALUES (?, ?, ?, ?, ?, ?)
            """, cinema_name, cinema_capacity, cinema_address, cinema_city, cinema_country, cinema_website)
            connection.commit()

            # Retrieve the generated Cinema ID
            cursor.execute("SELECT @@IDENTITY")  # Retrieve last inserted identity
            cinema_id = cursor.fetchone()[0]
            logging.info(f"Cinema ID retrieved: {cinema_id}")

            if not cinema_id:
                raise Exception("Failed to retrieve Cinema ID")

            # Close the database connection
            cursor.close()
            connection.close()

            # Success message
            QtWidgets.QMessageBox.information(self, "Success", "Cinema registration successful!")
            self.close()

        except Exception as e:
            logging.error(f"Error registering cinema: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Cinema registration failed.")


class RegisterScreenAsViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsViewer, self).__init__()
        uic.loadUi('RegisterAsViewer.ui', self)

        # Connect register button
        self.registerButtonViewer.clicked.connect(self.register_user)

    def register_user(self):
        name = self.lineEditname.text()
        email = self.lineEditemail.text()
        password = self.lineEditpassword.text()
        dob = self.dateEdit.date().toString('yyyy-MM-dd')
        gender = self.lineEditgender.text()
        address = self.lineEditaddress.text()
        city = self.lineEditcity.text()
        country = self.lineEditcountry.text()

        # Role assignment
        role = "Regular" 

        if not (name and email and dob and password and gender and address and city and country):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Customer ([CustomerRole], [CustomerName], [CustomerGender], [CustomerDateOfBirth], [CustomerAddress], [CustomerCity], [CustomerCountry])
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, role, name, gender, dob, address, city, country)

            connection.commit()

            # Retrieve the generated Cinema ID
            cursor.execute("SELECT @@IDENTITY")  # Retrieve last inserted identity
            customer_id = cursor.fetchone()[0]
            logging.info(f"Cinema ID retrieved: {customer_id}")

            if not customer_id:
                raise Exception("Failed to retrieve Customer ID")
            

            # Insert into Account table
            cursor.execute("""
                INSERT INTO Account ([Email], [Password], [CustomerID])
                VALUES (?, ?, ?)
            """, email, password, customer_id)
            connection.commit()

            # Close the database connection
            cursor.close()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Registration successful!")
            
            # Navigate to the home page
            self.go_to_home_page()

        except Exception as e:
            logging.error(f"Error registering user: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Registration failed.")

    def go_to_home_page(self):
        # Load the Home Page UI
        self.home_page = HomePageScreen()
        self.home_page.show()
        # Close the registration screen
        self.close()

class HomePageScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(HomePageScreen, self).__init__()
        uic.loadUi('homePage.ui', self)

        # Assuming you already have a layout with a search bar, we are adding the dynamic table here

        self.setWindowTitle('Movie Search')
        self.setGeometry(200, 200, 800, 600)  # Adjust window size as needed

        # Create a central widget and set it to the main window
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout to manage widgets (Search Bar, Table, etc.)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Create the search bar (QLineEdit)
        self.lineEditsearch = QtWidgets.QLineEdit(self)
        self.lineEditsearch.setPlaceholderText("Search movies by title...")
        self.layout.addWidget(self.lineEditsearch)

        # Connect the search functionality
        self.lineEditsearch.textChanged.connect(self.search_movies)


        # Initially no table, we will add it dynamically after search results are fetched
        self.moviesTable = None  # Placeholder for the table

    def search_movies(self):
        search_query = self.lineEditsearch.text()
        print(f"Search query: '{search_query}'")  # Debugging line
        if search_query.strip() == "":
            return  # Avoid searching with an empty query
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # SQL query with JOIN to get genre from the MovieGenres table
            cursor.execute("""
                SELECT m.MovieID, m.Title, g.GenreName, c.Director, m.Release_date
                FROM Movies m
                INNER JOIN MovieGenres g ON m.GenreID = g.GenreID
                INNER JOIN Crew c on m.MovieID = c.MovieID
                WHERE m.Title LIKE ?
            """, f"%{search_query}%")
            results = cursor.fetchall()

            if not results:
                print("No results found.")  # Debugging line

            # If there is an existing table, remove it from the layout
            if self.moviesTable:
                self.layout.removeWidget(self.moviesTable)
                self.moviesTable.deleteLater()

            # Dynamically create the movies table (QTableWidget) to display search results
            self.moviesTable = QtWidgets.QTableWidget(self)
            self.moviesTable.setColumnCount(5)  # MovieID, Title, Genre, Director, Release Year
            self.moviesTable.setHorizontalHeaderLabels(['Movie ID', 'Title', 'Genre', 'Director', 'Release Year'])
            self.moviesTable.setColumnHidden(0, True)  # Hide MovieID column
            self.moviesTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
            self.layout.addWidget(self.moviesTable)

            # Populate the table with search results
            self.moviesTable.setRowCount(0)  # Clear any existing rows
            for row_number, row_data in enumerate(results):
                self.moviesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.moviesTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
            logging.error(f"Error searching movies: {e}")
        finally:
            cursor.close()
            connection.close()



class MovieDescriptionScreen(QtWidgets.QDialog):
    def __init__(self):
        super(MovieDescriptionScreen, self).__init__()
        uic.loadUi('MovieDescription.ui', self)

    def populate_movie_details_table(self, movie_details):
        """
        Populates the existing table in the UI with movie details.
        :param movie_details: Dictionary containing movie information.
        """
        self.movieDetailsTable.setRowCount(0)  # Clear any existing rows

        # Populate rows with movie details
        for field, value in movie_details.items():
            row_position = self.movieDetailsTable.rowCount()
            self.movieDetailsTable.insertRow(row_position)  # Add a new row
            self.movieDetailsTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(field))  # Field Name
            self.movieDetailsTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(value)))  # Field Value

            # Optionally resize columns for better visibility
            self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
            self.movieDetailsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def show_movie_details(self, item):
        selected_row = item.row()
        movie_id = self.moviesTable.item(selected_row, 0).text()

        # Fetch movie details from the database
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT m.MovieID, m.Title, g.GenreName, c.CrewName AS Director, m.Release_Date, 
                    m.Description, m.Runtime, m.Rating, m.Cast
                FROM Movies m
                LEFT JOIN MovieGenres mg ON m.MovieID = mg.MovieID
                LEFT JOIN Genre g ON mg.GenreID = g.GenreID
                LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director'
                WHERE m.MovieID = ?
            """, movie_id)
            movie_data = cursor.fetchone()
            if not movie_data:
                QtWidgets.QMessageBox.warning(self, "Error", "Movie details not found.")
                return

            # Map the data into a dictionary for ease of use
            movie_details = {
                'Title': movie_data[1],
                'Genre': movie_data[2],
                'Director': movie_data[3],
                'Release Year': movie_data[4],
                'Description': movie_data[5],
                'Runtime': movie_data[6],
                'Rating': movie_data[7],
                'Cast': movie_data[8],
            }

            # Open the Movie Description Screen and populate the table
            description_screen = MovieDescriptionScreen()
            description_screen.populate_movie_details_table(movie_details)
            description_screen.exec_()  # Open as modal dialog
        except Exception as e:
            logging.error(f"Error fetching movie details: {e}")
        finally:
            cursor.close()
            connection.close()



class RegisterScreenAsPremiumViewer(QtWidgets.QMainWindow):
    def __init__(self, role):
        super(RegisterScreenAsPremiumViewer, self).__init__()
        uic.loadUi('RegisterScreenAsPremiumViewer.ui', self)
    #     self.role = role
    #     self.role_label.setText(f"Register as {self.role}")

    #     # Connect register button
    #     self.register_button.clicked.connect(self.register_user)

    # def register_user(self):
    #     username = self.username_input.text()
    #     password = self.password_input.text()
    #     # Add more fields based on the role

    #     try:
    #         connection = pyodbc.connect(connection_string)
    #         cursor = connection.cursor()
    #         cursor.execute("""
    #             INSERT INTO Users (Username, Password, Role)
    #             VALUES (?, ?, ?)
    #         """, username, password, self.role)
    #         connection.commit()
    #         cursor.close()
    #         connection.close()
    #         QtWidgets.QMessageBox.information(self, "Success", "Registration successful!")
    #         self.close()
    #     except Exception as e:
    #         logging.error(f"Error registering user: {e}")
    #         QtWidgets.QMessageBox.critical(self, "Error", "Registration failed.")

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi('Login.ui', self)

    #     # Connect login button
    #     self.login_button.clicked.connect(self.login_user)

    # def login_user(self):
    #     username = self.username_input.text()
    #     password = self.password_input.text()

    #     try:
    #         connection = pyodbc.connect(connection_string)
    #         cursor = connection.cursor()
    #         cursor.execute("""
    #             SELECT * FROM Users WHERE Username = ? AND Password = ? AND Role = ?
    #         """, username, password, role)
    #         user = cursor.fetchone()
    #         cursor.close()
    #         connection.close()
    #         if user:
    #             QtWidgets.QMessageBox.information(self, "Success", "Login successful!")
    #             self.open_role_dashboard(role)
    #         else:
    #             QtWidgets.QMessageBox.warning(self, "Error", "Invalid credentials.")
    #     except Exception as e:
    #         logging.error(f"Error logging in user: {e}")
    #         QtWidgets.QMessageBox.critical(self, "Error", "Login failed.")

    # def open_role_dashboard(self, role):
    #     if role == 'Admin':
    #         self.dashboard = AdminDashboard()
    #     elif role == 'Cinema Manager':
    #         self.dashboard = ManagerDashboard()
    #     elif role == 'Premium Viewer':
    #         self.dashboard = PremiumViewerDashboard()
    #     elif role == 'Normal Viewer':
    #         self.dashboard = ViewerDashboard()
    #     self.dashboard.show()
    #     self.close()




app = QtWidgets.QApplication(sys.argv) 
window = UI()  
window.show()
app.exec() 
# try:
#     # # Establish a connection to the database
#     connection = pyodbc.connect(connection_string)
#     cursor = connection.cursor()

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

# except Exception as e:
#     error_message = f"An error occurred: {e}"
#     print(error_message)
#     logging.error(error_message)

# finally:
#     # Ensure resources are released properly
#     try:
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'connection' in locals() and connection:
#             connection.close()
#     except Exception as cleanup_error:
#         cleanup_message = f"Error during cleanup: {cleanup_error}"
#         print(cleanup_message)
#         logging.error(cleanup_message)






