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


        

app = QtWidgets.QApplication(sys.argv) 
window = UI()  
window.show()
app.exec() 
