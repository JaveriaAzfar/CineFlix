import pyodbc
import logging
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
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
        super(UI, self).__init__()
        uic.loadUi('homePage.ui', self)
    
         # Find the search bar and button
        self.lineEditsearch = self.findChild(QtWidgets.QLineEdit, "lineEditsearch")
        self.searchButton = self.findChild(QtWidgets.QPushButton, "searchButton")

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


class MovieDescriptionScreen(QtWidgets.QMainWindow):
    def __init__(self, movie_id):
        super(MovieDescriptionScreen, self).__init__()
        uic.loadUi('MovieDescription.ui', self)  # Load the UI file for movie details

        self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
        self.fetch_and_display_movie_details(movie_id)

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


            self.populate_movie_details_table(movie_details)
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

            # Populate the UI table or list with the movies
            self.populate_movies_table(movie_list)
        except Exception as e:
            logging.error(f"Error fetching movies for Genre {genre_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movies.")
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


            # Populate the UI table or list with the movies
            self.populate_movies_table(movie_list)
        except Exception as e: 
            logging.error(f"Error fetching movies for Language {language_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movies.")
        finally:
            cursor.close()
            connection.close()

    def fetch_and_display_movies_by_crew(self, crew_name, crew_position):
        """Fetch movies by a specific director or actor from the database and populate the UI."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to fetch movies by director or actor
            query = """
                SELECT DISTINCT m.Title, year(m.Release_Date), m.Language, m.Duration, m.IMDB_Rating
                FROM Movies m
                INNER JOIN Crew c ON m.MovieID = c.MovieID
                WHERE c.CrewName = ? AND c.CrewPosition = ?
            """
            cursor.execute(query, crew_name, crew_position)
            movies = cursor.fetchall()

            if not movies:
                logging.warning(f"No movies found for {crew_position}: {crew_name}")
                QtWidgets.QMessageBox.warning(self, "No Movies Found", 
                                            f"No movies found for {crew_position.lower()} '{crew_name}'.")
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

            # Populate the UI table or list with the movies
            self.populate_movies_table(movie_list)
        except Exception as e:
            logging.error(f"Error fetching movies for {crew_position} {crew_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movies.")
        finally:
            cursor.close()
            connection.close()



    # if play button pressed, call this function
    def play_movie(self, movie_id, customer_id):
        """Update DateStarted when the movie finishes playing."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Today's date for 'DateStarted'
            today_date = datetime.now().strftime('%Y-%m-%d')

            update_query = """
                UPDATE CustomerHistory
                SET DateStarted = ?
                WHERE CustomerID = ? AND MovieID = ?
            """
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
    def fav_movie(self, movie_id, customer_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            today_date = datetime.now().strftime('%Y-%m-%d')

            update_query = """
                UPDATE CustomerFavorites
                SET DateAdded = ?
                WHERE CustomerID = ? AND MovieID = ?
            """
            cursor.execute(update_query, today_date, customer_id, movie_id)
            connection.commit()
            logging.info(f"Updated DateAdded for MovieID {movie_id} and CustomerID {customer_id}.")
        except Exception as e:
            logging.error(f"Error updating DateAdded: {e}")
        finally:
            cursor.close()
            connection.close()

    def allow_movie_download(self, movie_id, customer_id):
        """Allow a premium customer to download a movie for offline viewing."""
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            # Query to check the customer's role
            check_role_query = """
                SELECT CustomerRole FROM Customer
                WHERE CustomerID = ?
            """
            cursor.execute(check_role_query, customer_id)
            result = cursor.fetchone()

            if result and result[0] == "Premium":
                # Allow download for premium customers
                logging.info(f"CustomerID {customer_id} is a premium user. Download allowed for MovieID {movie_id}.")
                QtWidgets.QMessageBox.information(self, "Success", "Download initiated for the movie!")
                # Here, you can add code to initiate the movie download process.
            elif result and result[0] == "Regular":
                logging.warning(f"CustomerID {customer_id} is not a premium user. Download denied.")
                QtWidgets.QMessageBox.warning(self, "Error", "Only premium users can download movies for offline viewing.")
            else:
                logging.warning(f"CustomerID {customer_id} not found in the database.")
                QtWidgets.QMessageBox.warning(self, "Error", "Customer not found.")
        except Exception as e:
            logging.error(f"Error checking premium status for CustomerID {customer_id}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to check premium status.")
        finally:
            cursor.close()
            connection.close()



    def populate_movie_details_table(self, movie_details):
        """Populate the details table with movie information in a horizontal layout."""
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



class RegisterScreenAsPremiumViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterScreenAsPremiumViewer, self).__init__()
        uic.loadUi('RegisterAsPremiumViewer.ui', self)

        # Connect register button
        self.registerButtonPViewer.clicked.connect(self.register_user)

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
        role = "Premium" 

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

class LoginScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi('Login.ui', self)

        # Connect login button
        self.loginButton.clicked.connect(self.login_user)

    def login_user(self):
        email = self.lineEditemail.text()  # Change username to email
        password = self.lineEditpassword.text()

        try:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            # Update SQL query to match email instead of username
            cursor.execute("""
                SELECT * FROM Account WHERE Email = ? AND Password = ?
            """, email, password)
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                customer_id = user[2]  # Assuming CustomerID is the 3rd column (index 2)
                employee_id = user[3]  # Assuming EmployeeID is the 4th column (index 3)

                if customer_id is not None:
                    # User is a customer, open customer dashboard
                    QtWidgets.QMessageBox.information(self, "Success", "Customer Login Successful!")
                    self.open_homepage()

                elif employee_id is not None:
                    # User is an employee, open employee dashboard (Admin, Manager, etc.)
                    QtWidgets.QMessageBox.information(self, "Success", "Employee Login Successful!")
                    self.open_homepage()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Invalid credentials.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid credentials.")
                
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Login failed.")

    def open_homepage(self):
        # Open the Homepage UI for both customers and employees
        self.homepage = HomePageScreen()  # Assuming you have a class for the Homepage UI
        self.homepage.show()
        self.close()

app = QtWidgets.QApplication(sys.argv) 
window = UI()  
window.show()
app.exec() 
