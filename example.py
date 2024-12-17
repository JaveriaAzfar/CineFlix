import pyodbc
import logging
import bcrypt
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
from datetime import datetime
import smtplib 
from email.mime.text import MIMEText

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
        uic.loadUi('./Screens/RegisterAsAdministrator.ui', self)
        
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
        self.home_page = HomePageScreenCustomer()
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

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            if self.active_filter == 'genre':
                print("Searching by genre...")
                self.description_screen = MovieDescriptionScreen()
                self.description_screen.fetch_and_display_movies_by_genre(search_query)
            
            if self.active_filter == 'language':
                print("Searching by langauge...")
                self.description_screen = MovieDescriptionScreen()
                self.description_screen.fetch_and_display_movies_by_language(search_query)

            if self.active_filter == 'crew':
                print("Searching by crew...")
                self.description_screen = MovieDescriptionScreen()
                self.description_screen.fetch_and_display_movies_by_crew(search_query)
            # Query to search movies based on title
            print("Searching by title...")
            query = """
                SELECT m.MovieID, m.Title
                FROM Movies m
                WHERE m.Title LIKE ?
            """
            cursor.execute(query, f"%{search_query}%")
            results = cursor.fetchall()
            print(f"Results: {results}")  # Debugging

            if results:
                # Display the first result
                movie_id = results[0][0]
                movie_title = results[0][1]  # Assuming the title is the second column in the results
                print(f"Found movie: {movie_title}")
                self.show_movie_details(movie_id)
            else:
                QtWidgets.QMessageBox.information(self, "No Results", "No movies found matching your search query.")

        except Exception as e:
            logging.error(f"Error searching movies: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def show_movie_details(self, movie_id):
        # Open the MovieDescriptionScreen with the selected movie ID
        self.description_screen = MovieDescriptionScreen(movie_id)
        self.description_screen.show()
    
    def open_profile(self):
        self.profile = UserProfileCustomer()
        self.profile.show()

class UserProfileCustomer(QtWidgets.QMainWindow):
     def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/userProfile.ui', self)

class HomePageScreenEmployee(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/homePageEmployee.ui', self)
    
         # Find the search bar and button
        self.lineEditsearch = self.findChild(QtWidgets.QLineEdit, "lineEditsearch")
        self.searchButton = self.findChild(QtWidgets.QPushButton, "searchButton")

        self.userProfileButton.clicked.connect(self.open_profile)


          # Connect the search button to search functionality
        self.searchButton.clicked.connect(self.search_movies)

        # Connect search bar to search functionality
        self.lineEditsearch.returnPressed.connect(self.search_movies)

    def search_movies(self):
        search_query = self.lineEditsearch.text().strip()
        if not search_query:
            return  # Skip if the search query is empty

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to search movies based on title
            query = """
                SELECT m.MovieID, m.Title
                FROM Movies m
                WHERE m.Title LIKE ?
            """
            cursor.execute(query, f"%{search_query}%")
            results = cursor.fetchall()

            if results:
                # Display the first result
                movie_id = results[0][0]
                movie_title = results[0][1]  # Assuming the title is the second column in the results
                print(f"Found movie: {movie_title}")
                self.show_movie_details(movie_id)
            else:
                QtWidgets.QMessageBox.information(self, "No Results", "No movies found matching your search query.")

        except Exception as e:
            logging.error(f"Error searching movies: {e}")
        finally:
            cursor.close()
            connection.close()

    def show_movie_details(self, movie_id):
        # Open the MovieDescriptionScreen with the selected movie ID
        self.description_screen = MovieDescriptionScreen(movie_id)
        self.description_screen.show()

    def open_profile(self):
        self.profile = UserProfileEmployee()
        self.profile.show()

class UserProfileEmployee(QtWidgets.QMainWindow):
     def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/adminProfile.ui', self)

class MovieDescriptionScreen(QtWidgets.QMainWindow):
    def __init__(self, movie_id=None):
        super(MovieDescriptionScreen, self).__init__()
        uic.loadUi('./Screens/MovieDescription.ui', self)  # Load the UI file for movie details

        self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
        if movie_id:
            self.fetch_and_display_movie_details(movie_id)
        
        self.play.clicked.connect(self.play_movie)
        self.favorites.clicked.connect(self.fav_movie)
        

    def fetch_and_display_movie_details(self, movie_id):
        """Fetch movie details from the database and populate the UI."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
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
            print(f"Fetched movie data: {movie_data}")  # Debugging line

            if not movie_data:
                logging.warning(f"Movie details not found for MovieID: {movie_id}")
                QtWidgets.QMessageBox.warning(self, "Error", "Movie details not found.")
                return

            movie_details = {
                'Title': movie_data[0] or 'N/A',  # Ensure null values are handled
                'Genre': movie_data[1] or 'N/A',
                'Director': movie_data[2] or 'N/A',
                'Release Year': movie_data[3] or 'N/A',
                'Language': movie_data[4] or 'N/A',
                'Runtime': movie_data[5] or 'N/A',
                'Rating': movie_data[6] or 'N/A',
            }


            self.populate_movie_details_table_single(movie_details)
        except Exception as e:
            logging.error(f"Error fetching movie details for MovieID {movie_id}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movie details.")
        finally:
            cursor.close()
            connection.close()

    def fetch_and_display_movies_by_genre(self, genre_name):
        """Fetch movies by genre from the database and populate the UI."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to fetch movies of the given genre
            query = """
                SELECT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
                FROM Movies m
                LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
                LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
                WHERE gen.GenreName = ?
            """
            cursor.execute(query, genre_name)
            movies = cursor.fetchall()

            if not movies:
                logging.warning(f"No movies found for Genre: {genre_name}")
                QtWidgets.QMessageBox.warning(self, "No Movies Found", f"No movies found for the genre '{genre_name}'.")
                return

            # Prepare the list of movie details for display
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
            # Populate the UI table or list with the movies
            self.populate_movie_details_table(movie_list)

        except Exception as e:
            logging.error(f"Error fetching movies for Genre {genre_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def fetch_and_display_movies_by_language(self, language_name):
        """Fetch movies by language from the database and populate the UI."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to fetch movies of the given language
            query = """
                SELECT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
                FROM Movies m
                WHERE m.Language = ?
            """
            cursor.execute(query, language_name)
            movies = cursor.fetchall()

            if not movies:
                logging.warning(f"No movies found for Language: {language_name}")
                QtWidgets.QMessageBox.warning(self, "No Movies Found", f"No movies found for the language '{language_name}'.")
                return

            # Prepare the list of movie details for display
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
            # Populate the UI table or list with the movies
            self.populate_movie_details_table(movie_list)
        except Exception as e:
            logging.error(f"Error fetching movies for Language {language_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movies.")
        finally:
            cursor.close()
            connection.close()

    def fetch_and_display_movies_by_crew(self, crew_name):
        """Fetch movies by a specific director or actor from the database and populate the UI."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to fetch movies by director or actor
            query = """
                SELECT DISTINCT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
                FROM Movies m
                INNER JOIN Crew c ON m.MovieID = c.MovieID
                WHERE c.CrewName = ?
            """
            cursor.execute(query, crew_name)
            movies = cursor.fetchall()

            if not movies:
                logging.warning(f"No movies found for: {crew_name}")
                QtWidgets.QMessageBox.warning(self, "No Movies Found", 
                                            f"No movies found for '{crew_name}'.")
                return

            # Prepare the list of movie details for display
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
            # Populate the UI table or list with the movies
            self.populate_movie_details_table(movie_list)
        except Exception as e:
            logging.error(f"Error fetching movies for {crew_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movies.")
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

            # Extract movie_id from movie_details and store it
            self.movie_id = movie_details.get("Title")
            logging.info(f"Title {self.movie_id} extracted.")

            self.play_movie(self.movie_id) 
            
            
            self.fav_movie(self.movie_id)

    # if play button pressed, call this function
    def play_movie(self, movie_id):
        """Update DateStarted when the movie finishes playing."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        customer_id = 28

        try:
            # Today's date for 'DateStarted'
            today_date = datetime.now().strftime('%Y-%m-%d')

            update_query = """
                UPDATE CustomerHistory
                SET DateStarted = ?
                WHERE CustomerID = ? AND Title = ?
            """
            logging.info(f"Executing query: {update_query} with values: {today_date}, {customer_id}, {movie_id}")
            cursor.execute(update_query, today_date, customer_id, movie_id)
            connection.commit()
            logging.info(f"Updated DateStarted for MovieID {movie_id} and CustomerID {customer_id}.")
        except Exception as e:
            logging.error(f"Error updating DateStarted: {e}")
        finally:
            cursor.close()
            connection.close()

# if watched button pressed, call this function
    def mark_movie_as_watched(self, movie_id, customer_id):
        """Mark a movie as watched by updating DateEnded in WatchedHistory."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Today's date for 'DateEnded'
            today_date = datetime.now().strftime('%Y-%m-%d')

            # Check if the movie exists in WatchedHistory
            check_query = """
                SELECT * FROM CustomerHistory
                WHERE CustomerID = ? AND MovieID = ?
            """
            cursor.execute(check_query, customer_id, movie_id)
            result = cursor.fetchone()

            if result:
                # Update DateFinished for the watched movie
                update_query = """
                    UPDATE CustomerHistory
                    SET DateFinished = ?
                    WHERE CustomerID = ? AND MovieID = ?
                """
                cursor.execute(update_query, today_date, customer_id, movie_id)
                connection.commit()
                logging.info(f"Updated DateFinished for MovieID {movie_id} and CustomerID {customer_id}.")
                QtWidgets.QMessageBox.information(self, "Success", "Movie marked as watched!")
            else:
                logging.warning(f"MovieID {movie_id} not found in WatchedHistory for CustomerID {customer_id}.")
                QtWidgets.QMessageBox.warning(self, "Error", "Movie is not in your watch history.")
        except Exception as e:
            logging.error(f"Error marking movie as watched: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to mark movie as watched.")
        finally:
            cursor.close()
            connection.close()

# if fav/like button pressed, call this function
    def fav_movie(self, movie_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        customer_id = 28

        try:
            today_date = datetime.now().strftime('%Y-%m-%d')

            update_query = """
                UPDATE CustomerFavorites
                SET DateAdded = ?
                WHERE CustomerID = ? AND Title = ?
            """
            logging.info(f"Executing query: {update_query} with values: {today_date}, {customer_id}, {movie_id}")
            cursor.execute(update_query, today_date, customer_id, movie_id)
            connection.commit()
            logging.info(f"Updated DateAdded for MovieID {movie_id} and CustomerID {customer_id}.")
        except Exception as e:
            logging.error(f"Error updating DateAdded: {e}")
        finally:
            cursor.close()
            connection.close()

    


    def populate_movie_details_table(self, movie_details):
        """Populate the details table with movie information."""
        self.movieDetailsTable.setRowCount(0)  # Clear existing rows

        # Debug: Print the incoming movie details 
        print(f"Received movie details: {movie_details}")

         # Case 2: If a list of dictionaries is passed
        if isinstance(movie_details, list) and all(isinstance(movie, dict) for movie in movie_details):
            if not movie_details:
                QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
                return
            
            # Set the table column headers using the keys from the first dictionary
            self.movieDetailsTable.setColumnCount(len(movie_details[0]))
            self.movieDetailsTable.setHorizontalHeaderLabels(movie_details[0].keys())
            
            # Populate rows with each dictionary in the list
            for movie in movie_details:
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





class RegisterScreenAsPremiumViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsPremiumViewer, self).__init__()
        uic.loadUi('./Screens/RegisterAsPremiumViewer.ui', self)

        # Connect register button
        self.registerButtonPViewer.clicked.connect(self.register_user)

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
                   
class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Screens/Login.ui', self)

        # Connect login button
        self.loginButton.clicked.connect(self.login_user)

        # Connect login button
        self.forgotPassword.clicked.connect(self.forgot_password)

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
                        self.open_homepage_customer()

                    elif employee_id is not None:
                        QtWidgets.QMessageBox.information(self, "Success", "Employee Login Successful!")
                        self.open_homepage_employeee()
                
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
