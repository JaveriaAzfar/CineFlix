import pyodbc
import logging
import bcrypt
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
from datetime import datetime
import smtplib 
from email.mime.text import MIMEText
from datetime import datetime

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
        uic.loadUi('./Screens/MainScreen.ui', self)
    
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
        uic.loadUi('./Screens/Register Options.ui', self)

        # Connect role buttons
        self.AdminRole.clicked.connect(self.open_admin_register_screen)
        self.CMRole.clicked.connect(self.open_manager_register_screen)
        self.PViewerRole.clicked.connect(self.open_premium_register_screen)
        self.ViewerRole.clicked.connect(self.open_normal_register_screen)

        # Connect login instead button
        self.AlreadyLogin.clicked.connect(self.open_login_screen)
        self.backButton.clicked.connect(self.firstscreen)

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

    def firstscreen(self):
        self.login_screen = UI()
        self.login_screen.show()
        self.close()

class RegisterScreenAsAdmin(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsAdmin, self).__init__()
        uic.loadUi('./Screens/RegisterAsAdministrator.ui', self)
        
        # Connect register button
        self.RegisterButton_Admin.clicked.connect(self.register_user)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterOptions()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

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

            cursor.execute("""
                           SELECT Email FROM Account WHERE Email = ?""", email)
            existing_email = cursor.fetchone()

            if existing_email: 
                QtWidgets.QMessageBox.warning(self, "Error", "This email is already registered.") 
                cursor.close() 
                connection.close()

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
        uic.loadUi('./Screens/RegisterAsCinemaManager.ui', self)
        
        # Connect register button for manager info
        self.nextButton.clicked.connect(self.register_manager_info)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterOptions()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

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

            
            cursor.execute("""
                           SELECT Email FROM Account WHERE Email = ?""", email)
            existing_email = cursor.fetchone()

            if existing_email: 
                QtWidgets.QMessageBox.warning(self, "Error", "This email is already registered.") 
                cursor.close() 
                connection.close()

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
        uic.loadUi('./Screens/RegisterAsCinemaManager - second screen.ui', self)

        # Store employee_id for associating the manager with the cinema
        self.employee_id = employee_id

        # Connect register button for cinema info
        self.cinemaRegisterButton.clicked.connect(self.register_cinema_info)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterScreenAsCinemaManager()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

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
        uic.loadUi('./Screens/RegisterAsViewer.ui', self)

        # Connect register button
        self.registerButtonViewer.clicked.connect(self.register_user)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterOptions()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

    def register_user(self):
        name = self.lineEditname.text()
        email = self.lineEditemail.text()
        password = self.lineEditpassword.text()
        dob = self.dateEdit.date().toString('yyyy-MM-dd')
        gender = self.genderBox.currentText()
        address = self.lineEditaddress.text()
        city = self.lineEditcity.text()
        country = self.lineEditcountry.text()

        # Role assignment
        role = "Regular" 

        if not (name and email and dob and password and gender and address and city and country):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            # Parse the date of birth and current date 
            dob_date_obj = datetime.strptime(dob, '%Y-%m-%d') 
            current_date_obj = datetime.now() 
            
            if dob_date_obj > current_date_obj: 
                QtWidgets.QMessageBox.warning(self, "Error", "Date of birth cannot be in the future.") 
                return
            
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("""
                           SELECT Email FROM Account WHERE Email = ?""", email)
            existing_email = cursor.fetchone()

            if existing_email: 
                QtWidgets.QMessageBox.warning(self, "Error", "This email is already registered.") 
                cursor.close() 
                connection.close()

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
        self.home_page = LoginScreen()
        self.home_page.show()
        # Close the registration screen
        self.close()

class HomePageScreenCustomer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/homePageCustomer.ui', self)
    
         # Find the search bar and button
        self.lineEditsearch = self.findChild(QtWidgets.QLineEdit, "lineEditsearch")
        self.searchButton = self.findChild(QtWidgets.QPushButton, "searchButton")

        # Find the filter buttons 
        self.genreButton = self.findChild(QtWidgets.QPushButton, "genre") 
        self.languageButton = self.findChild(QtWidgets.QPushButton, "language") 
        self.crewButton = self.findChild(QtWidgets.QPushButton, "crew")
        # Find the reset button 
        self.resetButton = self.findChild(QtWidgets.QPushButton, "reset")

          # Connect the search button to search functionality
        self.searchButton.clicked.connect(self.search_movies)

        self.userProfileButton.clicked.connect(self.open_profile)


        # Connect search bar to search functionality
        self.lineEditsearch.returnPressed.connect(self.search_movies)

        # Connect filter buttons to their respective functions 
        self.genreButton.clicked.connect(self.set_genre_filter) 
        self.languageButton.clicked.connect(self.set_language_filter) 
        self.crewButton.clicked.connect(self.set_crew_filter) 

        # Connect reset button to reset styles and active filter 
        self.resetButton.clicked.connect(self.reset_filters)
        self.logoutButton.clicked.connect(self.logout)
        # Variable to track the active filter 
        self.active_filter = None

    def set_genre_filter(self): 
        self.active_filter = 'genre' 
        self.reset_button_styles() 
        self.genreButton.setStyleSheet("background-color: yellow") 
    
    def set_language_filter(self): 
        self.active_filter = 'language' 
        self.reset_button_styles() 
        self.languageButton.setStyleSheet("background-color: yellow") 
    
    def set_crew_filter(self): 
        self.active_filter = 'crew' 
        self.reset_button_styles() 
        self.crewButton.setStyleSheet("background-color: yellow") 
    
    def reset_button_styles(self): 
        self.genreButton.setStyleSheet("") 
        self.languageButton.setStyleSheet("") 
        self.crewButton.setStyleSheet("") 
    
    def reset_filters(self): 
        self.active_filter = None 
        self.reset_button_styles() 
        self.lineEditsearch.clear()

    def search_movies(self):
        search_query = self.lineEditsearch.text().strip()
        if not search_query:
            return  # Skip if the search query is empty

        try:
            if self.active_filter == 'genre':
                print("Searching by genre...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_genre(search_query)
            
            elif self.active_filter == 'language':
                print("Searching by langauge...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_language(search_query)

            elif self.active_filter == 'crew':
                print("Searching by crew...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_crew(search_query)
            else: 
                print("Searching by title...") 
                self.search_movies_by_title(search_query)
        except Exception as e:
            logging.error(f"Error searching movies: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def search_movies_by_title(self, search_query):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            query = """
                SELECT m.MovieID, m.Title
                FROM Movies m
                WHERE m.Title LIKE ?
            """
            cursor.execute(query, f"%{search_query}%")
            results = cursor.fetchall()
            print(f"Results: {results}")  # Debugging

            if results:
                movie_id = results[0][0]
                movie_title = results[0][1]  # Assuming the title is the second column in the results
                print(f"Found movie: {movie_title}")
                self.show_movie_details(movie_id)
            else:
                QtWidgets.QMessageBox.information(self, "No Results", "No movies found matching your search query.")
        except Exception as e:
            logging.error(f"Error searching movies by title: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def show_movie_details(self, movie_id):
        # Open the MovieDescriptionScreen with the selected movie ID
        print(f"Opening MovieDescriptionScreen for movie ID: {movie_id}") # Debug
        self.description_screen = MovieDescriptionScreen(movie_id)
        self.description_screen.show()
    
    def open_profile(self):
        self.profile = UserProfileCustomer()
        self.profile.show()
    
    def logout(self):
        # Open the RegisterOptions screen
        self.registration_screen = LoginScreen()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class AddReview(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('./Screens/addReview.ui', self)

        self.parent = parent
        self.saveButton = self.findChild(QtWidgets.QPushButton, "addButton")
        self.saveButton.clicked.connect(self.add_review_to_db)
        self.backButton.clicked.connect(self.open_premium_customer_profile)

    def add_review_to_db(self):
        stars = self.stars.text()
        comment = self.comment.text()
        movie_title = self.title.text()

        if not stars or not comment or not movie_title:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT MovieID FROM Movies WHERE Title LIKE ?", (movie_title,))
            movie_id = cursor.fetchone()
            if movie_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Movie title not found.")
                return
            movie_id = movie_id[0]

            query = """
                INSERT INTO Reviews (Stars, Comment, Create_Date, Modify_Date, ReviewerID, MovieID)
                VALUES (?, ?, GETDATE(), GETDATE(), ?, ?)
            """
            cursor.execute(query, (stars, comment, self.parent.customer_id, movie_id))
            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Review added successfully!")
            self.parent.refresh_reviews_table()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def open_premium_customer_profile(self):
        # Open the RegisterOptions screen
        self.registration_screen = UserProfileCustomer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class UpdateReview(QtWidgets.QMainWindow):
    def __init__(self, parent, review_id, stars, comment, movie_title):
        super().__init__()
        uic.loadUi('./Screens/updateReview.ui', self)

        self.parent = parent
        self.review_id = review_id
        self.stars.setText(stars)
        self.comment.setText(comment)
        self.title.setText(movie_title)

        self.saveButton = self.findChild(QtWidgets.QPushButton, "updateButton")
        self.saveButton.clicked.connect(self.update_review_in_db)
        self.backButton.clicked.connect(self.get_to_profile)

    def update_review_in_db(self):
        stars = self.stars.text()
        comment = self.comment.text()
        movie_title = self.title.text()

        if not stars or not comment or not movie_title:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT MovieID FROM Movies WHERE Title Like ?", (movie_title,))
            movie_id = cursor.fetchone()
            if movie_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Movie title not found.")
                return
            movie_id = movie_id[0]

            query = """
                UPDATE Reviews
                SET Stars = ?, Comment = ?, Modify_Date = GETDATE(), MovieID = ?
                WHERE ReviewID = ?
            """
            cursor.execute(query, (stars, comment, movie_id, self.review_id))
            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Review updated successfully!")
            self.parent.refresh_reviews_table()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def get_to_profile(self):
        # Open the RegisterOptions screen
        self.registration_screen = UserProfileCustomer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class UserProfileCustomer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/userProfile.ui', self)

        # Accessing CustomerID
        self.customer_id = Session.get_customer_id()
        if self.customer_id:
            print(f"Logged-in Customer ID: {self.customer_id}")

        # Check user role and load the appropriate UI
        if self.is_premium_customer(self.customer_id):
            uic.loadUi('./Screens/premiumUserProfile.ui', self)  # Load premium UI
            self.setup_premium_ui()
            self.populate_favorites_and_history(include_payment=True, include_reviews=True)
        else:
            self.populate_favorites_and_history(include_payment=False, include_reviews=False)

        self.backButton.clicked.connect(self.homepage)
    
    def homepage(self):
        # Open the RegisterOptions screen
        self.registration_screen = HomePageScreenCustomer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

    def is_premium_customer(self, customer_id):
        """Check if the customer is a premium user."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT CustomerRole FROM Customer WHERE CustomerID = ?", (customer_id,))
        customer_role = cursor.fetchone()
        connection.close()

        if customer_role and customer_role[0] == "Premium":
            return True
        return False

    def setup_premium_ui(self): 
        """Setup the premium user UI components.""" 
        self.reviewsTable = self.findChild(QtWidgets.QTableWidget, "reviewsTable") 
        if not self.reviewsTable: 
            QtWidgets.QMessageBox.warning(self, "Error", "Reviews table not found in the UI.") 
            return 
        self.addReviewButton = self.findChild(QtWidgets.QPushButton, "add") 
        self.addReviewButton.clicked.connect(self.show_add_review_ui) 
        self.updateReviewButton = self.findChild(QtWidgets.QPushButton, "update") 
        self.updateReviewButton.clicked.connect(self.show_update_review_ui) 
        self.deleteReviewButton = self.findChild(QtWidgets.QPushButton, "delete_2") 
        self.deleteReviewButton.clicked.connect(self.delete_review)

    def show_add_review_ui(self):
        self.add_review_window = AddReview(self)
        self.add_review_window.show()

    def show_update_review_ui(self):
        current_row = self.reviewsTable.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "No review selected.")
            return

        review_id = int(self.reviewsTable.item(current_row, 0).text())
        stars = self.reviewsTable.item(current_row, 1).text()
        comment = self.reviewsTable.item(current_row, 2).text()
        movie_title = self.reviewsTable.item(current_row, 6).text()

        self.update_review_window = UpdateReview(self, review_id, stars, comment, movie_title)
        self.update_review_window.show()


    def populate_favorites_and_history(self, include_payment=False, include_reviews=False):
        # Fetch favorite movies and watch history
        favorites = self.get_favorite_movies(self.customer_id)
        history = self.get_watch_history(self.customer_id)

        # Populate the favorite movies table
        self.populate_movies_table(self.favoritesTable, favorites)
        
        # Populate the watch history table
        self.populate_movies_table(self.historyTable, history)

        # If the user is a premium customer, populate the payment details table
        if include_payment:
            payment = self.get_payment_details(self.customer_id)
            self.populate_movies_table(self.paymentTable, payment)

        # If the user is a premium customer, populate the reviews table
        if include_reviews:
            reviews = self.get_reviews(self.customer_id)
            self.populate_reviews_table(reviews)

    def get_favorite_movies(self, customer_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT m.Title, f.DateAdded 
            FROM CustomerFavorites f 
            JOIN Movies m ON f.MovieID = m.MovieID 
            WHERE f.CustomerID = ?
        """, (customer_id,))
        favorite_movies = cursor.fetchall()
        connection.close()
        return favorite_movies

    def get_watch_history(self, customer_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT m.Title, h.DateStarted, h.DateFinished 
            FROM CustomerHistory h 
            JOIN Movies m ON h.MovieID = m.MovieID 
            WHERE h.CustomerID = ?
        """, (customer_id,))
        watch_history = cursor.fetchall()
        connection.close()
        return watch_history

    def get_payment_details(self, customer_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = """
            SELECT PaymentID, Card_Holder_Name, Card_Number, CVV, Card_Expiration_Date, CustomerID, CustomerRole
            FROM Payment
            WHERE CustomerID = ?
        """
        cursor.execute(query, (customer_id,))
        payment_details = cursor.fetchall()
        connection.close()
        return payment_details

    def get_reviews(self, customer_id):
        """Fetch and display user reviews."""
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Fetch reviews for the current user
            query = """
                SELECT r.ReviewID, r.Stars, r.Comment, r.Create_Date, r.Modify_Date, r.MovieID, m.Title
                FROM Reviews r
                JOIN Movies m ON r.MovieID = m.MovieID
                WHERE r.ReviewerID = ?
            """
            cursor.execute(query, (customer_id,))
            reviews = cursor.fetchall()
            connection.close()

            return reviews
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def delete_review(self):
        current_row = self.reviewsTable.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "No review selected.")
            return

        review_id = int(self.reviewsTable.item(current_row, 0).text())
        
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Reviews WHERE ReviewID = ?", (review_id,))
            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Review deleted successfully!")
            self.refresh_reviews_table()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def refresh_reviews_table(self):
        reviews = self.get_reviews(self.customer_id)
        self.populate_reviews_table(reviews)

    def populate_reviews_table(self, reviews):
        """Populate the reviews table with data."""
        self.reviewsTable.setRowCount(0)  # Clear previous rows

        if not reviews:
            QtWidgets.QMessageBox.warning(self, "No Results", "No reviews found.")
            return

        # Set the number of columns and headers
        self.reviewsTable.setColumnCount(7)
        self.reviewsTable.setHorizontalHeaderLabels(['ReviewID', 'Stars', 'Comment', 'Create Date', 'Modify Date', 'MovieID', 'Title'])

        # Populate rows
        for review in reviews:
            row_position = self.reviewsTable.rowCount()
            self.reviewsTable.insertRow(row_position)
            for col, value in enumerate(review):
                self.reviewsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))

        self.reviewsTable.resizeColumnsToContents()
        self.reviewsTable.horizontalHeader().setStretchLastSection(True)
        self.reviewsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    def populate_movies_table(self, table, movie_list):
        """Populate the table with movie data."""
        table.setRowCount(0)  # Clear previous rows

        if not movie_list:
            QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
            return

        # Set the number of columns and headers based on the first row of movie_list
        table.setColumnCount(len(movie_list[0]))

        # Assuming the columns correspond to Title, DateAdded or DateStarted, DateFinished
        if len(movie_list[0]) == 2:
            table.setHorizontalHeaderLabels(['Title', 'DateAdded'])
        elif len(movie_list[0]) == 3:
            table.setHorizontalHeaderLabels(['Title', 'DateStarted', 'DateFinished'])
        elif len(movie_list[0]) == 7:
            table.setHorizontalHeaderLabels(['PaymentID', 'Card Holder Name', 'Card Number', 'CVV', 'Card Expiration Date', 'CustomerID', 'CustomerRole'])

        for movie in movie_list:
            row_position = table.rowCount()
            table.insertRow(row_position)

            for col, value in enumerate(movie):
                table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

class HomePageScreenEmployee(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/homePageCustomer.ui', self)
    
         # Find the search bar and button
        self.lineEditsearch = self.findChild(QtWidgets.QLineEdit, "lineEditsearch")
        self.searchButton = self.findChild(QtWidgets.QPushButton, "searchButton")

        # Find the filter buttons 
        self.genreButton = self.findChild(QtWidgets.QPushButton, "genre") 
        self.languageButton = self.findChild(QtWidgets.QPushButton, "language") 
        self.crewButton = self.findChild(QtWidgets.QPushButton, "crew")
        # Find the reset button 
        self.resetButton = self.findChild(QtWidgets.QPushButton, "reset")

          # Connect the search button to search functionality
        self.searchButton.clicked.connect(self.search_movies)

        self.userProfileButton.clicked.connect(self.open_profile)


        # Connect search bar to search functionality
        self.lineEditsearch.returnPressed.connect(self.search_movies)

        # Connect filter buttons to their respective functions 
        self.genreButton.clicked.connect(self.set_genre_filter) 
        self.languageButton.clicked.connect(self.set_language_filter) 
        self.crewButton.clicked.connect(self.set_crew_filter) 

        # Connect reset button to reset styles and active filter 
        self.resetButton.clicked.connect(self.reset_filters)

        self.logoutButton.clicked.connect(self.Logout)
        
        # Variable to track the active filter 
        self.active_filter = None

    def set_genre_filter(self): 
        self.active_filter = 'genre' 
        self.reset_button_styles() 
        self.genreButton.setStyleSheet("background-color: yellow") 
    
    def set_language_filter(self): 
        self.active_filter = 'language' 
        self.reset_button_styles() 
        self.languageButton.setStyleSheet("background-color: yellow") 
    
    def set_crew_filter(self): 
        self.active_filter = 'crew' 
        self.reset_button_styles() 
        self.crewButton.setStyleSheet("background-color: yellow") 
    
    def reset_button_styles(self): 
        self.genreButton.setStyleSheet("") 
        self.languageButton.setStyleSheet("") 
        self.crewButton.setStyleSheet("") 
    
    def reset_filters(self): 
        self.active_filter = None 
        self.reset_button_styles() 
        self.lineEditsearch.clear()

    def search_movies(self):
        search_query = self.lineEditsearch.text().strip()
        if not search_query:
            return  # Skip if the search query is empty

        try:
            if self.active_filter == 'genre':
                print("Searching by genre...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_genre(search_query)
            
            elif self.active_filter == 'language':
                print("Searching by langauge...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_language(search_query)

            elif self.active_filter == 'crew':
                print("Searching by crew...")
                self.description_screen = MovieListScreen([])
                self.description_screen.fetch_and_display_movies_by_crew(search_query)
            else: 
                print("Searching by title...") 
                self.search_movies_by_title(search_query)
        except Exception as e:
            logging.error(f"Error searching movies: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def search_movies_by_title(self, search_query):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            query = """
                SELECT m.MovieID, m.Title
                FROM Movies m
                WHERE m.Title LIKE ?
            """
            cursor.execute(query, f"%{search_query}%")
            results = cursor.fetchall()
            print(f"Results: {results}")  # Debugging

            if results:
                movie_id = results[0][0]
                movie_title = results[0][1]  # Assuming the title is the second column in the results
                print(f"Found movie: {movie_title}")
                self.show_movie_details(movie_id)
            else:
                QtWidgets.QMessageBox.information(self, "No Results", "No movies found matching your search query.")
        except Exception as e:
            logging.error(f"Error searching movies by title: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def show_movie_details(self, movie_id):
        # Open the MovieDescriptionScreen with the selected movie ID
        print(f"Opening MovieDescriptionScreen for movie ID: {movie_id}") # Debug
        self.description_screen = MovieDescriptionScreen(movie_id)
        self.description_screen.show()
    
    def open_profile(self):
        self.profile = UserProfileEmployee()
        self.profile.show()

    def Logout(self):
        # Open the RegisterOptions screen
        self.registration_screen = LoginScreen()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class UserProfileEmployee(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Accessing EmployeeID
        self.employee_id = Session.get_employee_id()
        if self.employee_id:
            print(f"Logged-in Employee ID: {self.employee_id}")
        

        # Check employee role and load the corresponding UI
        role = self.get_employee_role(self.employee_id)
        if role == "Admin":
            uic.loadUi('./Screens/adminProfile.ui', self)
            self.setup_admin_ui()
        elif role == "Cinema Manager":
            uic.loadUi('./Screens/cinemaManagerProfile.ui', self)
            self.setup_cinema_ui()
        else:
            QtWidgets.QMessageBox.warning(self, "Access Denied", "You do not have access to this feature.")

        # Additional setup can be done here
        # self.setup_admin_ui()
        self.backButton.clicked.connect(self.homepage)
    
    def homepage(self):
        # Open the RegisterOptions screen
        self.registration_screen = HomePageScreenEmployee()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen
        
    def get_employee_role(self, employee_id):
        """Check the role of the employee."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT EmployeePosition FROM Employee WHERE EmployeeID = ?", (employee_id))
        role = cursor.fetchone()
        connection.close()

        if role:
            print(role)
            return role[0]
        else:
            return None
    

    def get_all_movies(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = """
            SELECT m.MovieID, m.Title, gen.GenreName, c.CrewName AS Director, year(m.Release_Date), m.Language,
                m.Duration, m.IMDB_Rating, m.Screening
            FROM Movies m
            LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
            LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
            LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director'
        """
        cursor.execute(query)
        all_movies = cursor.fetchall()
        connection.close()
        return all_movies
    
    def setup_cinema_ui(self):
        """Setup the cinema manager UI with buttons and connections."""
        # Connect buttons to functions
        self.addButton = self.findChild(QtWidgets.QPushButton, "add")
        self.deleteButton = self.findChild(QtWidgets.QPushButton, "delete_2")
        self.updateButton = self.findChild(QtWidgets.QPushButton, "update_2")

        # Debug: Print the buttons to check if they are found 
        print(f"Add Button: {self.addButton}") 
        print(f"Delete Button: {self.deleteButton}")
        print(f"Update Button: {self.updateButton}")

        if not self.addButton or not self.deleteButton or not self.updateButton: 
            QtWidgets.QMessageBox.warning(self, "Error", "Buttons not found in the UI.") 
            return

        self.addButton.clicked.connect(self.add_cinema_listing)
        self.deleteButton.clicked.connect(self.delete_cinema_listing)
        self.updateButton.clicked.connect(self.update_movie_data_cinema)

        # Movie table
        self.cinemaTable = self.findChild(QtWidgets.QTableWidget, "cinemaListingsTable")
        self.moviesTable = self.findChild(QtWidgets.QTableWidget, "cinemaListingsTable_2")

        self.moviesTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        # Debug: Print the movieTable to check if it is found 
        print(f"Cinema Listings Table: {self.cinemaTable}")
        print(f"Movies Table: {self.moviesTable}")

        if not self.cinemaTable or not self.moviesTable: 
            QtWidgets.QMessageBox.warning(self, "Error", "Cinema Listings or Movies Table not found in the UI.")
            return

        # Populate the tables
        self.populate_screenings_table(self.cinemaTable, self.get_all_screenings())
        self.populate_movies_table_cinema(self.moviesTable, self.get_all_movies())


    def add_cinema_listing(self):
        """Show the UI for adding a new movie.""" 
        self.add_movie_window = AddCinemaListing(self) 
        self.add_movie_window.show()

    def delete_cinema_listing(self): 
        current_row = self.cinemaListingsTable.currentRow() 
        if current_row == -1: 
            QtWidgets.QMessageBox.warning(self, "Error", "No listing selected.") 
            return 
        cinema_name = self.cinemaListingsTable.item(current_row, 0).text() 
        movie_title = self.cinemaListingsTable.item(current_row, 1).text()
        
        try: 
            connection = pyodbc.connect(connection_string) 
            cursor = connection.cursor()

            cursor.execute("SELECT CinemaID FROM Cinema WHERE Cinema_Name = ?", (cinema_name,))
            cinema_id = cursor.fetchone()
            if cinema_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Cinema name not found.")
                return
            cinema_id = cinema_id[0]

            cursor.execute("SELECT MovieID FROM Movies WHERE Title = ?", (movie_title,))
            movie_id = cursor.fetchone()
            if movie_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Movie title not found.")
                return
            movie_id = movie_id[0]
            
            cursor.execute("DELETE FROM CinemaListing WHERE CinemaID = ? AND MovieID = ?", (cinema_id, movie_id))

            # Check if the movie has other screenings
            cursor.execute("SELECT COUNT(*) FROM CinemaListing WHERE MovieID = ?", (movie_id,))
            screenings_count = cursor.fetchone()[0]

            # Update the Screening column in the Movies table
            if screenings_count == 0:
                cursor.execute("UPDATE Movies SET Screening = 0 WHERE MovieID = ?", (movie_id,))

            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Cinema listing deleted successfully!")
            self.refresh_cinema_table()
        except Exception as e: 
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def refresh_cinema_table(self): 
        """Refresh the movie table with the latest data.""" 
        self.populate_screenings_table(self.cinemaTable, self.get_all_screenings())

    def populate_screenings_table(self, table, screenings_list): 
        """Populate the table with cinema screenings data.""" 
        table.setRowCount(0) # Clear previous rows 
        
        if not screenings_list: 
            QtWidgets.QMessageBox.warning(self, "No Results", "No screenings found to display.") 
            return 
        # Set the number of columns and headers based on the screenings_list 
        table.setColumnCount(len(screenings_list[0])) 
        
        # Setting headers 
        table.setHorizontalHeaderLabels(['Cinema Name', 'Title', 'Hall_No', 'Date', 'Start_Time', 'End_Time', 'Format']) 
        
        # Populate rows 
        # 
        for screening in screenings_list: 
            row_position = table.rowCount() 
            table.insertRow(row_position) 
            for col, value in enumerate(screening): 
                table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value))) 
        
        table.resizeColumnsToContents() 
        table.horizontalHeader().setStretchLastSection(True) 
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 
        
        # Debug: Check the number of rows and columns 
        # 
        print(f"Rows: {table.rowCount()}, Columns: {table.columnCount()}")

    def setup_admin_ui(self):
        """Setup the admin UI with buttons and connections."""
        # Connect buttons to functions
        self.addButton = self.findChild(QtWidgets.QPushButton, "add")
        self.updateButton = self.findChild(QtWidgets.QPushButton, "update")
        self.deleteButton = self.findChild(QtWidgets.QPushButton, "delete_2")

        # Debug: Print the buttons to check if they are found 
        print(f"Add Button: {self.addButton}") 
        print(f"Update Button: {self.updateButton}") 
        print(f"Delete Button: {self.deleteButton}")

        if not self.addButton or not self.updateButton or not self.deleteButton: 
            QtWidgets.QMessageBox.warning(self, "Error", "Buttons not found in the UI.") 
            return

        self.addButton.clicked.connect(self.add_movie)
        self.updateButton.clicked.connect(self.update_movie)
        self.deleteButton.clicked.connect(self.delete_movie)

        # Movie table
        self.movieTable = self.findChild(QtWidgets.QTableWidget, "listedTable")
        # Debug: Print the movieTable to check if it is found 
        print(f"Movie Table: {self.movieTable}")

        if not self.movieTable: 
            QtWidgets.QMessageBox.warning(self, "Error", "Movie table not found in the UI.")
        # Populate the movie table with all movies

        # Connect double-click to the edit function 
        self.movieTable.cellDoubleClicked.connect(self.update_movie)

        self.populate_movies_table(self.movieTable, self.get_all_movies())

        # Populate the screenings table with all screenings 
        self.populate_screenings_table(self.CinemaScreeningsTable, self.get_all_screenings())
    
    def add_movie(self):
        """Show the UI for adding a new movie.""" 
        self.add_movie_window = AddMovieDetails(self) 
        self.add_movie_window.show()

   
    def delete_movie(self):
        """Delete a movie from the database."""
        current_row = self.movieTable.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "No movie selected.")
            return

        movie_id = int(self.movieTable.item(current_row, 0).text())

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Delete from MovieGenre table
            cursor.execute("DELETE FROM MovieGenre WHERE MovieID = ?", (movie_id,))

            # Delete from Crew table
            cursor.execute("DELETE FROM Crew WHERE MovieID = ?", (movie_id,))

            # Delete from Movies table
            cursor.execute("DELETE FROM Movies WHERE MovieID = ?", (movie_id,))

            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Movie deleted successfully!")
            self.refresh_movie_table()  # Refresh the movie table to reflect changes
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def refresh_movie_table(self): 
        """Refresh the movie table with the latest data.""" 
        self.populate_movies_table(self.movieTable, self.get_all_movies())

    def update_movie(self): 
        """Show the UI for updating an existing movie.""" 
        current_row = self.movieTable.currentRow()# Use the row from the double-clicked signal 
        if current_row == -1: 
            QtWidgets.QMessageBox.warning(self, "Error", "No movie selected.") 
            return 
        
        movie_id = int(self.movieTable.item(current_row, 0).text()) 
        title = self.movieTable.item(current_row, 1).text() 
        genre = self.movieTable.item(current_row, 2).text() 
        director = self.movieTable.item(current_row, 3).text() 
        release_date = self.movieTable.item(current_row, 4).text()
        language = self.movieTable.item(current_row, 5).text() 
        runtime = self.movieTable.item(current_row, 6).text() 
        rating = self.movieTable.item(current_row, 7).text() 
        
        self.update_movie_window = UpdateMovieDetails( 
            self, movie_id, title, genre, director, release_date, language, runtime, rating )
        
        self.update_movie_window.show()

    def get_all_screenings(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query =""" select c.cinema_Name, m.title, w.hall_no, w.date, w.start_time, w.end_time, w.format
                    from CinemaListing w
                    inner join Cinema c on w.CinemaID = c.CinemaID
                    inner join Movies m on w.MovieID = m.MovieID
                """
        cursor.execute(query)
        all_screenings = cursor.fetchall()
        connection.close()
        return all_screenings
    
    def populate_screenings_table(self, table, screenings_list):
        """Populate the table with cinema screenings data."""
        table.setRowCount(0)  # Clear previous rows

        if not screenings_list:
            QtWidgets.QMessageBox.warning(self, "No Results", "No screenings found to display.")
            return

        # Set the number of columns and headers based on the screenings_list
        table.setColumnCount(len(screenings_list[0]))

        # Setting headers
        table.setHorizontalHeaderLabels(['Cinema Name', 'Movie Title', 'Hall_No', 'Date', 'Start_Time', 'End_Time', 'Format'])

        # Populate rows
        for screening in screenings_list:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for col, value in enumerate(screening):
                table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))
        
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Debug: Check the number of rows and columns
        print(f"Rows: {table.rowCount()}, Columns: {table.columnCount()}")

    def populate_movies_table_cinema(self, table, movie_list):
        """Populate the table with movie data."""
        table.setRowCount(0)  # Clear previous rows

        if not movie_list:
            QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
            return

        # Set the number of columns and headers based on the first row of movie_list
        table.setColumnCount(len(movie_list[0]))

        # Setting headers based on the movie data structure
        table.setHorizontalHeaderLabels(['MovieID', 'Title', 'Genre', 'Director', 'Release Year', 'Language', 'Runtime', 'Rating', 'Screening'])

        # Populate rows
        for movie in movie_list:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for col, value in enumerate(movie):
                item = QtWidgets.QTableWidgetItem(str(value))
                # Allow editing only for the Screening column
                if col != 8:  # Assuming 'Screening' is column 8
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                table.setItem(row_position, col, item)
        
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Debug: Check the number of rows and columns
        print(f"Rows: {table.rowCount()}, Columns: {table.columnCount()}")


    def update_movie_data_cinema(self):
        """Update the movie data in the database."""
        row = self.moviesTable.currentRow()
        if row == -1:  # No row is selected
            QtWidgets.QMessageBox.warning(self, "Error", "No movie selected.")
            return

        # Get the column index of the updated cell
        column = self.moviesTable.currentColumn()

        # Check if the MovieID cell is valid
        cell_item = self.moviesTable.item(row, 0)  # MovieID is in column 0
        if not cell_item:
            QtWidgets.QMessageBox.warning(self, "Error", "No MovieID found in the selected row.")
            return

        movie_id = cell_item.text()
        new_value = self.moviesTable.item(row, column).text()  # New value
        column_name = self.moviesTable.horizontalHeaderItem(column).text()  # Column header name

        # Allow updates only for the Screening column
        if column_name == "Screening":
            if new_value not in ["0", "1"]:
                QtWidgets.QMessageBox.warning(self, "Invalid Input", "Screening must be 0 (No) or 1 (Yes).")
                return

            try:
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()

                # Update query
                query = f"UPDATE Movies SET {column_name} = ? WHERE MovieID = ?"
                cursor.execute(query, (new_value, movie_id))
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Success", "Movie data updated successfully.")
                
                # Refresh the table to reflect the updated data
                self.populate_movies_table_cinema(self.moviesTable, self.get_all_movies())
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update movie data: {e}")
            finally:
                cursor.close()
                connection.close()


    def populate_movies_table(self, table, movie_list):
        """Populate the table with movie data."""
        table.setRowCount(0)  # Clear previous rows

        if not movie_list:
            QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
            return

        # Set the number of columns and headers based on the first row of movie_list
        table.setColumnCount(len(movie_list[0]))

        # Setting headers based on the movie data structure
        table.setHorizontalHeaderLabels(['MovieID', 'Title', 'Genre', 'Director', 'Release Year', 'Language', 'Runtime', 'Rating', 'Screeming'])

        # Populate rows
        for movie in movie_list:
            row_position = table.rowCount()
            table.insertRow(row_position)
            for col, value in enumerate(movie):
                table.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))
        
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Enable table to be editable
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        # Debug: Check the number of rows and columns
        print(f"Rows: {table.rowCount()}, Columns: {table.columnCount()}")

class UpdateMovieDetails(QtWidgets.QMainWindow):
    def __init__(self, parent, movie_id, title, genre, director, release_date, language, runtime, rating):
        super().__init__()
        uic.loadUi('./Screens/updateMovieDetails.ui', self)
        
        self.parent = parent
        self.movie_id = movie_id
        self.title.setText(title)
        self.genre.setText(genre)
        self.director.setText(director)
        self.releasedate.setText(release_date)
        self.language.setText(language)
        self.runtime.setText(runtime)
        self.rating.setText(rating)

        self.saveButton = self.findChild(QtWidgets.QPushButton, "saveButton")
        self.saveButton.clicked.connect(self.update_movie_in_db)
        self.backButton.clicked.connect(self.open_admin_profile)

    def update_movie_in_db(self):
        # Get movie details from the UI
        title = self.title.text()
        genre = self.genre.text()
        director = self.director.text()
        release_date = self.releasedate.text()
        language = self.language.text()
        runtime = self.runtime.text()
        rating = self.rating.text()

        # Validate the inputs
        if not title or not genre or not director or not release_date or not language or not runtime or not rating:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            # Connect to the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Update the movie in the Movies table
            query = """
                UPDATE Movies
                SET Title = ?, Release_Date = ?, Language = ?, Duration = ?, IMDB_Rating = ?
                WHERE MovieID = ?
            """
            cursor.execute(query, (title, release_date, language, runtime, rating, self.movie_id))

            # Update Genre table and MovieGenre table
            genre_id = cursor.execute("SELECT GenreID FROM Genre WHERE GenreName = ?", (genre,)).fetchone()
            if genre_id is None:
                cursor.execute("INSERT INTO Genre (GenreName) VALUES (?)", (genre,))
                genre_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            else:
                genre_id = genre_id[0]

            cursor.execute("UPDATE MovieGenre SET GenreID = ? WHERE MovieID = ?", (genre_id, self.movie_id))

            # Update Crew table
            cursor.execute("UPDATE Crew SET CrewName = ? WHERE MovieID = ? AND CrewPosition = 'Director'", (director, self.movie_id))

            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Movie updated successfully!")
            self.parent.refresh_movie_table()  # Call parent's method to refresh the table
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def open_admin_profile(self):
        # Open the RegisterOptions screen
        self.registration_screen = UserProfileEmployee()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class AddMovieDetails(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('./Screens/addMovieDetails.ui', self)

        self.parent = parent
        # Connect the add button to the function
        self.addButton = self.findChild(QtWidgets.QPushButton, "addButton")
        self.addButton.clicked.connect(self.add_movie_to_db)
        self.backButton.clicked.connect(self.open_admin_profile)

    def add_movie_to_db(self):
        # Get movie details from the UI
        title = self.title.text()
        genre = self.genre.text()
        director = self.director.text()
        release_date = self.releasedate.text()
        language = self.language.text()
        runtime = self.runtime.text()
        rating = self.rating.text()
        # rottenTomatoes = self.rottenTomates.text()

        # Validate the inputs
        if not title or not genre or not director or not release_date or not language or not runtime or not rating:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            # Connect to the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Insert the movie into the Movies table
            query = """
                INSERT INTO Movies (Title, IMDB_Rating, Release_Date, Language, Duration)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (title, rating, release_date, language, runtime ))
            connection.commit()

            # Get the newly added movie's ID
            movie_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            # Insert into Genre table and MovieGenre table
            genre_id = cursor.execute("SELECT GenreID FROM Genre WHERE GenreName = ?", (genre)).fetchone()
            if genre_id is None:
                cursor.execute("INSERT INTO Genre (GenreName) VALUES (?)", (genre))
                genre_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            else:
                genre_id = genre_id[0]

            cursor.execute("INSERT INTO MovieGenre (MovieID, GenreID) VALUES (?, ?)", (movie_id, genre_id))

            # Insert into Crew table
            cursor.execute("INSERT INTO Crew (MovieID, CrewName, CrewPosition) VALUES (?, ?, 'Director')", (movie_id, director))

            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Movie added successfully!")
            self.parent.refresh_movie_table()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def open_admin_profile(self):
        # Open the RegisterOptions screen
        self.registration_screen = UserProfileEmployee()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class AddCinemaListing(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('./Screens/addCinemaListings.ui', self)

        self.parent = parent
        self.saveButton = self.findChild(QtWidgets.QPushButton, "addButton")
        self.saveButton.clicked.connect(self.add_listing_to_db)
        self.backButton.clicked.connect(self.open_manager_profile)

    def add_listing_to_db(self):
        cinema_name = self.cinema.text()
        movie_title = self.title.text()
        hall_no = self.hallno.text()
        date = self.date.text()
        start_time = self.starttime.text()
        end_time = self.endtime.text()
        format_ = self.format.text()

        if not cinema_name or not movie_title or not hall_no or not date or not start_time or not end_time or not format_:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT CinemaID FROM Cinema WHERE Cinema_Name = ?", (cinema_name,))
            cinema_id = cursor.fetchone()
            if cinema_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Cinema name not found.")
                return
            cinema_id = cinema_id[0]

            cursor.execute("SELECT MovieID FROM Movies WHERE Title = ?", (movie_title,))
            movie_id = cursor.fetchone()
            if movie_id is None:
                QtWidgets.QMessageBox.warning(self, "Error", "Movie title not found.")
                return
            movie_id = movie_id[0]

            query = """
                INSERT INTO CinemaListing (CinemaID, MovieID, Hall_No, Date, Start_Time, End_Time, Format)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (cinema_id, movie_id, hall_no, date, start_time, end_time, format_))

            # Update the Screening column in the Movies table
            cursor.execute("UPDATE Movies SET Screening = 1 WHERE MovieID = ?", (movie_id,))

            connection.commit()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Cinema listing added successfully!")
            self.parent.refresh_cinema_table()
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
    
    def open_manager_profile(self):
        # Open the RegisterOptions screen
        self.registration_screen = UserProfileEmployee()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class MovieDescriptionScreen(QtWidgets.QMainWindow):
    def __init__(self, movie_id=None):
        super(MovieDescriptionScreen, self).__init__()
        uic.loadUi('./Screens/MovieDescription.ui', self)  # Load the UI file for movie details
        self.movie_id = movie_id
        self.play_button = self.findChild(QtWidgets.QPushButton, "play")  # Ensure the button is correctly referenced
        self.favorites_button = self.findChild(QtWidgets.QPushButton, "favorites")  # Ensure the button is correctly referenced
        
        self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
        if movie_id: 
            self.fetch_and_display_movie_details(movie_id)
        self.play_button.clicked.connect(self.play_movie)
        self.favorites_button.clicked.connect(self.fav_movie)
        self.backButton.clicked.connect(self.homepage_viewer)

    def fetch_and_display_movie_details(self, movie_id):
        """Fetch movie details from the database and populate the UI."""
        try:
            # Establish database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Query to fetch detailed information about the movie
            query = """                
                SELECT m.Title, gen.GenreName, c.CrewName AS Director, year(m.Release_Date), m.Language,
                    m.Duration, m.IMDB_Rating
                FROM Movies m
                LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
                LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
                LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director'
                WHERE m.MovieID = ?
            """
            cursor.execute(query, movie_id)
            movie_data = cursor.fetchone()
            logging.info(f"Fetched movie data: {movie_data}")  # Debugging

            if not movie_data:
                logging.warning(f"Movie details not found for MovieID: {movie_id}")
                QtWidgets.QMessageBox.warning(self, "Error", "Movie details not found.")
                return

            # Organize movie details into a dictionary
            movie_details = {
                'Title': movie_data[0] or 'N/A',  # Handle null values
                'Genre': movie_data[1] or 'N/A',
                'Director': movie_data[2] or 'N/A',
                'Release Year': movie_data[3] or 'N/A',
                'Language': movie_data[4] or 'N/A',
                'Runtime': movie_data[5] or 'N/A',
                'Rating': movie_data[6] or 'N/A',
            }
            print(f"Retrieved MovieID: {movie_id}")

            self.populate_movie_details_table_single(movie_details)

        except Exception as e:
            logging.error(f"Error fetching movie details for MovieID {movie_id}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movie details.")
        finally:
            cursor.close()
            connection.close()

    def populate_movie_details_table_single(self, movie_details):
        """Populate the details table with movie information in a horizontal layout."""
        if isinstance(movie_details, dict):  # Checking if movie_details is a dictionary
            # Set the number of columns based on the movie_details dictionary
            self.movieDetailsTable.setColumnCount(len(movie_details))

            # Set column headers (keys from the movie_details dictionary)
            self.movieDetailsTable.setHorizontalHeaderLabels(movie_details.keys())

            # Insert only one row to display the movie data horizontally
            row_position = self.movieDetailsTable.rowCount()
            self.movieDetailsTable.insertRow(row_position)

            # Populate the row with movie details (values from the movie_details dictionary)
            for col, (field, value) in enumerate(movie_details.items()):
                self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))

            # Resize columns to fit the content
            self.movieDetailsTable.resizeColumnsToContents()
            # Resize columns for better visibility
            self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
            self.movieDetailsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


    def fav_movie(self):
        print("Attempting to add to favorites...")
        connection = None
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            movie_id = self.movie_id
            self.customer_id = Session.get_customer_id()
            print(f"movie id: {movie_id}, customer id: {self.customer_id}")
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            print("Connection established, preparing to insert...")

            insert_query = """
                INSERT INTO CustomerFavorites (CustomerID, MovieID, DateAdded)
                VALUES (?, ?, ?)
            """
            logging.info(f"Executing insert query: {insert_query} with values: {self.customer_id}, {movie_id}, {today_date}")
            cursor.execute(insert_query, self.customer_id, movie_id, today_date)
            connection.commit()
            logging.info(f"Inserted new favorite entry for MovieID {movie_id} and CustomerID {self.customer_id}.")
            print("Inserted new favorite entry.")
        except Exception as e:
            logging.error(f"Error inserting into CustomerFavorites: {e}")
            print(f"Exception occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            print("Connection closed.")

    def play_movie(self):
        print("Attempting to update play history...")
        connection = None
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            movie_id = self.movie_id
            self.customer_id = Session.get_customer_id()
            print(f"movie id: {movie_id}, customer id: {self.customer_id}")
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            print("Connection established, preparing to insert...")

            insert_query = """
                INSERT INTO CustomerHistory (CustomerID, MovieID, DateStarted, DateFinished)
                VALUES (?, ?, ?, ?)
            """
            logging.info(f"Executing insert query: {insert_query} with values: {self.customer_id}, {movie_id}, {today_date}, {today_date}")
            cursor.execute(insert_query, self.customer_id, movie_id, today_date, today_date)
            connection.commit()
            logging.info(f"Inserted new play history entry for MovieID {movie_id} and CustomerID {self.customer_id}.")
            print("Inserted new play history entry.")
        except Exception as e:
            logging.error(f"Error inserting into CustomerHistory: {e}")
            print(f"Exception occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            print("Connection closed.")

    def homepage_viewer(self):
        # Open the RegisterOptions screen
        self.registration_screen = HomePageScreenCustomer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class MovieListScreen(QtWidgets.QMainWindow):
    def __init__(self, movie_list):
        super(MovieListScreen, self).__init__()
        print("Initializing MovieListScreen...")  # Debug
        uic.loadUi('./Screens/MovieDescriptionPremium.ui', self)  # Load the UI file for movie list

        self.movie_list = movie_list
        self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
        if self.movie_list:
            self.populate_movie_details_table()
        self.backButton.clicked.connect(self.homepage_premium_viewer)

    def fetch_and_display_movies_by_genre(self, genre_name):
        query = """
            SELECT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
            FROM Movies m
            LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
            LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
            WHERE gen.GenreName = ?
        """
        self.fetch_and_display_movies(query, genre_name, "Genre")
        self.show()

    def fetch_and_display_movies_by_language(self, language_name):
        query = """
            SELECT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
            FROM Movies m
            WHERE m.Language = ?
        """
        self.fetch_and_display_movies(query, language_name, "Language")
        self.show()

    def fetch_and_display_movies_by_crew(self, crew_name):
        query = """
            SELECT DISTINCT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
            FROM Movies m
            INNER JOIN Crew c ON m.MovieID = c.MovieID
            WHERE c.CrewName = ?
        """
        self.fetch_and_display_movies(query, crew_name, "Crew")
        self.show()

    def fetch_and_display_movies(self, query, params, filter_name):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            movies = cursor.fetchall()

            if not movies:
                logging.warning(f"No movies found for {filter_name}: {params}")
                QtWidgets.QMessageBox.warning(self, "No Movies Found", f"No movies found for {filter_name} '{params}'.")
                return

            movie_list = []
            for movie in movies:
                movie_details = {
                    'Title': movie[0] or 'N/A',
                    'Release Year': movie[1] or 'N/A',
                    'Language': movie[2] or 'N/A',
                    'Runtime': movie[3] or 'N/A',
                    'Rating': movie[4] or 'N/A',
                }
                movie_list.append(movie_details)

            print(f"Movie list for table: {movie_list}")  # Debug
            self.show_movie_list(movie_list)
        except Exception as e:
            logging.error(f"Error fetching movies for {filter_name} {params}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    def show_movie_list(self, movie_list):
         # Populate the details table with the movie list 
        self.movie_list = movie_list 
        self.populate_movie_details_table()
        self.show()

    def populate_movie_details_table(self):
        """Populate the details table with movie information."""
        self.movieDetailsTable.setRowCount(0)  # Clear existing rows
        print(f"Received movie list: {self.movie_list}")  # Debug

        if isinstance(self.movie_list, list) and all(isinstance(movie, dict) for movie in self.movie_list):
            if not self.movie_list:
                QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
                return

            # Set the table column headers using the keys from the first dictionary
            self.movieDetailsTable.setColumnCount(len(self.movie_list[0]))
            self.movieDetailsTable.setHorizontalHeaderLabels(self.movie_list[0].keys())

            for movie in self.movie_list:
                row_position = self.movieDetailsTable.rowCount()
                self.movieDetailsTable.insertRow(row_position)
                for col, (key, value) in enumerate(movie.items()):
                    self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))
            print(f"Inserted {self.movieDetailsTable.rowCount()} rows.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid data format. Cannot populate table.")
            return

        # Resize columns to fit the content
        self.movieDetailsTable.resizeColumnsToContents()
        # Stretch the last column for better visibility
        self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
        self.movieDetailsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    def homepage_premium_viewer(self):
        # Open the RegisterOptions screen
        self.registration_screen = HomePageScreenCustomer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

class RegisterScreenAsPremiumViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsPremiumViewer, self).__init__()
        uic.loadUi('./Screens/RegisterAsPremiumViewer.ui', self)

        # Connect register button
        self.registerButtonPViewer.clicked.connect(self.register_user)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterOptions()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

    def register_user(self):
        name = self.lineEditname.text()
        email = self.lineEditemail.text()
        password = self.lineEditpassword.text()
        dob = self.dateEdit.date().toString('yyyy-MM-dd')
        gender = self.genderBox.currentText()
        address = self.lineEditaddress.text()
        city = self.lineEditcity.text()
        country = self.lineEditcountry.text()

        # Role assignment
        role = "Premium" 

        if not (name and email and dob and password and gender and address and city and country):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            # Parse the date of birth and current date 
            dob_date_obj = datetime.strptime(dob, '%Y-%m-%d') 
            current_date_obj = datetime.now() 
            
            if dob_date_obj > current_date_obj: 
                QtWidgets.QMessageBox.warning(self, "Error", "Date of birth cannot be in the future.") 
                return
            
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("""
                           SELECT Email FROM Account WHERE Email = ?""", email)
            existing_email = cursor.fetchone()

            if existing_email: 
                QtWidgets.QMessageBox.warning(self, "Error", "This email is already registered.") 
                cursor.close() 
                connection.close()

            cursor.execute("""
                INSERT INTO Customer ([CustomerRole], [CustomerName], [CustomerGender], [CustomerDateOfBirth], [CustomerAddress], [CustomerCity], [CustomerCountry])
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, role, name, gender, dob, address, city, country)

            connection.commit()

            # Retrieve the generated Cinema ID
            cursor.execute("SELECT @@IDENTITY")  # Retrieve last inserted identity
            customer_id = cursor.fetchone()[0]
            logging.info(f"Customer ID retrieved: {customer_id}")

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
            self.go_to_payment_page(customer_id, role)

        except Exception as e:
            logging.error(f"Error registering user: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Registration failed.")

    def go_to_payment_page(self, customer_id, role):
        # Load the Home Page UI
        self.payment_page = PremiumViewerPayment(customer_id, role)
        self.payment_page.show()
        # Close the registration screen
        self.close()

class PremiumViewerPayment(QtWidgets.QMainWindow):
    def __init__(self, customer_id, role):
        super().__init__()
        uic.loadUi('./Screens/PaymentPremiumPlan.ui', self)

        # Connect login button
        self.submitPayment.clicked.connect(self.update_plan)
        self.cancel.clicked.connect(self.go_to_register_option)
        self.customer_id = customer_id
        self.role = role
        # Disable the submit button initially
        self.submitPayment.setEnabled(False)

        # Connect the terms radio button
        self.radioButton.toggled.connect(self.toggle_submit_button)
        self.backButton.clicked.connect(self.Register_Options_Screen)
    
    def Register_Options_Screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterScreenAsPremiumViewer()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

    def toggle_submit_button(self):
        # Enable the button only if the terms checkbox is checked
        self.submitPayment.setEnabled(self.radioButton.isChecked())

    def update_plan(self):
        name = self.name.text()
        card_number = self.number.text()
        cvv = self.cvv.text()
        expiration_date = self.dateEdit.date().toString('yyyy-MM-dd')
        city = self.city.text()
        country = self.country.text()
        postal_code = self.postalcode.text()
        plan = self.planbox.currentText()

        # Validate input fields
        if not name and not card_number and not cvv and not expiration_date and not city and not country and not postal_code and not plan:
            QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
            return
        
        try:
            # Parse the expiration date and current date 
            expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d') 
            current_date_obj = datetime.now() 
            
            if expiration_date_obj < current_date_obj: 
                QtWidgets.QMessageBox.warning(self, "Error", "Payment cannot be processed: The card expiration date is in the past.") 
                return
            
            # Connect to the database
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO Payment ([Card_Holder_Name], [Card_Number], [CVV], [Card_Expiration_Date], [CustomerID], [CustomerRole])
                VALUES (?, ?, ?, ?, ?, ?)
            """,name, card_number, cvv, expiration_date, self.customer_id, self.role)
            connection.commit()

            # Close the connection
            cursor.close()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Payment successful!")
            self.go_to_home_page()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Payment failed: {e}")

    def go_to_home_page(self):
        # Load the Home Page UI
        self.home_page = HomePageScreenCustomer()
        self.home_page.show()
        # Close the registration screen
        self.close()

    def go_to_register_option(self):
        # Load the Home Page UI
        self.register_options_page = RegisterOptions()
        self.register_options_page.show()
        # Close the registration screen
        self.close()
                   
class Session:

    current_customer_id = None
    current_employee_id = None

    @classmethod
    def set_customer_data(cls, customer_id):
        cls.current_customer_id = customer_id
        cls.current_employee_id = None  # Reset employee data when customer logs in
        

    @classmethod
    def set_employee_data(cls, employee_id):
        cls.current_employee_id = employee_id
        cls.current_customer_id = None  # Reset customer data when employee logs in

    @classmethod
    def get_customer_id(cls):
        return cls.current_customer_id

    @classmethod
    def get_employee_id(cls):
        return cls.current_employee_id

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/Login.ui', self)

        # Connect login button
        self.loginButton.clicked.connect(self.login_user)

        # Connect login button
        self.forgotPassword.clicked.connect(self.forgot_password)

        self.registerButton.clicked.connect(self.show_registration_screen)

        # Mask password field to show '*' for entered characters
        self.lineEditpassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def forgot_password(self): 
        email = self.lineEditemail.text() 
        # Get the email from the input field 
        if not email: 
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter your email address.") 
            return 
        # Placeholder for sending the recovery email 
        try: # Create the email content 
            # msg = MIMEText("Click the link below to reset your password:\n\nhttp://example.com/recover_password") 
            # msg['Subject'] = 'Password Recovery' 
            # msg['From'] = 'no-reply@example.com' 
            # msg['To'] = email 
            # # Send the email (using a dummy SMTP server) 
            # with smtplib.SMTP('smtp.example.com') as server: 
            #     server.sendmail(msg['From'], [msg['To']], msg.as_string()) 
            
            QtWidgets.QMessageBox.information(self, "Success", "Recovery link has been sent to your email.") 
        
        except Exception as e: 
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to send recovery email: {e}")
        
    def login_user(self):
        email = self.lineEditemail.text()  # Change username to email
        password = self.lineEditpassword.text()

        # Validate input fields
        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Email and/or password cannot be empty.")
            return

        # user = self.authenticate_user(email, password)
        
        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Update SQL query to match email instead of username
            cursor.execute("""
                SELECT * FROM Account WHERE Email = ?
            """, email)
            user = cursor.fetchone()
          
            if user:
                # Check if the password matches 
                cursor.execute(""" SELECT * FROM Account WHERE Email = ? AND Password = ? 
                            """, email, password) 
                user_with_password = cursor.fetchone() 

                
                cursor.close()
                connection.close()

                if user_with_password:
                    customer_id = user_with_password[2]  # Modify column index if needed
                    employee_id = user_with_password[3]  # Modify column index if needed

                    if customer_id is not None:
                        QtWidgets.QMessageBox.information(self, "Success", "Customer Login Successful!")
                        Session.set_customer_data(customer_id)  # Store the CustomerID
                        self.open_homepage_customer()  # Open homepage for customeri

                    elif employee_id is not None:
                        QtWidgets.QMessageBox.information(self, "Success", "Employee Login Successful!")
                        Session.set_employee_data(employee_id)  # Store Employee data
                        self.open_homepage_employeee()  # Open homepage for employee
                
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", "Invalid Password.")

                else: 
                    QtWidgets.QMessageBox.warning(self, "Error", "Invalid Password.")
            else:
                reply = QtWidgets.QMessageBox.question(self, "Not Registered", "This email is not registered. Would you like to register?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                
                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                    self.show_registration_screen()  # Open RegisterOptions screen
                else:
                    QtWidgets.QMessageBox.information(self, "Info", "Please register to access the platform.")

        except Exception as e:
                logging.error(f"Error logging in user: {e}")
                QtWidgets.QMessageBox.critical(self, "Error", "Login failed.")

    def show_registration_screen(self):
        # Open the RegisterOptions screen
        self.registration_screen = RegisterOptions()  # Open your RegisterOptions class
        self.registration_screen.show()
        self.close()  # Close login screen

    def open_homepage_customer(self):
        try:
            self.homepage = HomePageScreenCustomer()  # Ensure HomePageScreen is correctly imported
            self.homepage.show()
            self.close()
        except Exception as e:
            logging.error(f"Error opening homepage: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to open homepage.")
    
    def open_homepage_employeee(self):
        try:
            self.homepage = HomePageScreenEmployee()  # Ensure HomePageScreen is correctly imported
            self.homepage.show()
            self.close()
        except Exception as e:
            logging.error(f"Error opening homepage: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to open homepage.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())
