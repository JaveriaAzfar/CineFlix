# import pyodbc
# import logging
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtCore import QDate
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
# import sys


# # Configure logging to write errors to a file
# logging.basicConfig(
#     filename="db_errors.log",
#     level=logging.ERROR,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Replace these with your own database connection details
# server = 'JAVERIASLAPTOP\\SQLSERVER1'
# database = 'CineFlix'
# use_windows_authentication = False
# username = 'sa'
# password = 'f4d238ea'

# # Create the connection string based on the authentication method chosen
# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# class UI(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(UI, self).__init__()
#         uic.loadUi('homePage.ui', self)
    
#          # Find the search bar and button
#         self.lineEditsearch = self.findChild(QtWidgets.QLineEdit, "lineEditsearch")
#         self.searchButton = self.findChild(QtWidgets.QPushButton, "searchButton")

#           # Connect the search button to search functionality
#         self.searchButton.clicked.connect(self.search_movies)

#         # Connect search bar to search functionality
#         self.lineEditsearch.returnPressed.connect(self.search_movies)

#     def search_movies(self):
#         search_query = self.lineEditsearch.text().strip()
#         if not search_query:
#             return  # Skip if the search query is empty

#         connection = pyodbc.connect(connection_string)
#         cursor = connection.cursor()

#         try:
#             # Query to search movies based on title
#             query = """
#                 SELECT m.MovieID, m.Title
#                 FROM Movies m
#                 WHERE m.Title LIKE ?
#             """
#             cursor.execute(query, f"%{search_query}%")
#             results = cursor.fetchall()

#             if results:
#                 # Display the first result
#                 movie_id = results[0][0]
#                 movie_title = results[0][1]  # Assuming the title is the second column in the results
#                 print(f"Found movie: {movie_title}")
#                 self.show_movie_details(movie_id)
#             else:
#                 QtWidgets.QMessageBox.information(self, "No Results", "No movies found matching your search query.")

#         except Exception as e:
#             logging.error(f"Error searching movies: {e}")
#         finally:
#             cursor.close()
#             connection.close()

#     def show_movie_details(self, movie_id):
#         # Open the MovieDescriptionScreen with the selected movie ID
#         self.description_screen = MovieDescriptionScreen(movie_id)
#         self.description_screen.show()

# class MovieDescriptionScreen(QtWidgets.QMainWindow):
#     def __init__(self, movie_id):
#         super(MovieDescriptionScreen, self).__init__()
#         uic.loadUi('MovieDescription.ui', self)  # Load the UI file for movie details

#         self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
#         self.fetch_and_display_movie_details(movie_id)

#     def fetch_and_display_movie_details(self, movie_id):
#         """Fetch movie details from the database and populate the UI."""
#         connection = pyodbc.connect(connection_string)
#         cursor = connection.cursor()

#         try:
#             # Query to fetch detailed information about the movie
#             query = """                
#                 SELECT m.Title, gen.GenreName, c.CrewName AS Director, year(m.Release_Date), m.Language,
#                        m.Duration, m.IMDB_Rating
#                 FROM Movies m
#                 LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
#                 LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
#                 LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director'
#                 WHERE m.MovieID = ?
#             """
#             cursor.execute(query, movie_id)
#             movie_data = cursor.fetchone()

#             if not movie_data:
#                 logging.warning(f"Movie details not found for MovieID: {movie_id}")
#                 QtWidgets.QMessageBox.warning(self, "Error", "Movie details not found.")
#                 return

#             movie_details = {
#                 'Title': movie_data[0] or 'N/A',  # Ensure null values are handled
#                 'Genre': movie_data[1] or 'N/A',
#                 'Director': movie_data[2] or 'N/A',
#                 'Release Year': movie_data[3] or 'N/A',
#                 'Language': movie_data[4] or 'N/A',
#                 'Runtime': movie_data[5] or 'N/A',
#                 'Rating': movie_data[6] or 'N/A',
#             }


#             self.populate_movie_details_table(movie_details)
#         except Exception as e:
#             logging.error(f"Error fetching movie details for MovieID {movie_id}: {e}")
#             QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while fetching movie details.")
#         finally:
#             cursor.close()
#             connection.close()

#     def populate_movie_details_table(self, movie_details):
#         """Populate the details table with movie information in a horizontal layout."""
#         # Set the number of columns based on the movie_details dictionary
#         self.movieDetailsTable.setColumnCount(len(movie_details))

#         # Set column headers (keys from the movie_details dictionary)
#         self.movieDetailsTable.setHorizontalHeaderLabels(movie_details.keys())

#         # Insert only one row to display the movie data horizontally
#         row_position = self.movieDetailsTable.rowCount()
#         self.movieDetailsTable.insertRow(row_position)

#         # Populate the row with movie details (values from the movie_details dictionary)
#         for col, (field, value) in enumerate(movie_details.items()):
#             self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))

#         # Resize columns to fit the content
#         self.movieDetailsTable.resizeColumnsToContents()

#         # Resize columns for better visibility
#         self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
#         self.movieDetailsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


        

# app = QtWidgets.QApplication(sys.argv) 
# window = UI()  
# window.show()
# app.exec() 
# from PyQt6 import QtWidgets
# import sys


# class TestApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Set up the main window
#         self.setWindowTitle("Movie Details Test")
#         self.setGeometry(100, 100, 800, 400)

#         # Create a QTableWidget
#         self.movieDetailsTable = QtWidgets.QTableWidget(self)
#         self.movieDetailsTable.setGeometry(50, 50, 700, 300)

#         # Create a test button
#         self.testButton = QtWidgets.QPushButton("Test with Dummy Data", self)
#         self.testButton.setGeometry(50, 10, 200, 30)
#         self.testButton.clicked.connect(self.test_table_with_dummy_data)

#     def populate_movie_details_table(self, movie_details):
#         """Populate the QTableWidget with movie details."""
#         self.movieDetailsTable.setRowCount(0)  # Clear existing rows

#         # Check if data is valid
#         if isinstance(movie_details, list) and all(isinstance(movie, dict) for movie in movie_details):
#             if not movie_details:
#                 QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
#                 return

#             # Set the table column headers using the keys from the first dictionary
#             self.movieDetailsTable.setColumnCount(len(movie_details[0]))
#             self.movieDetailsTable.setHorizontalHeaderLabels(movie_details[0].keys())

#             # Populate rows with data
#             for movie in movie_details:
#                 row_position = self.movieDetailsTable.rowCount()
#                 self.movieDetailsTable.insertRow(row_position)
#                 for col, (key, value) in enumerate(movie.items()):
#                     self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))
#         else:
#             QtWidgets.QMessageBox.warning(self, "Error", "Invalid data format. Cannot populate table.")
#             return

#         # Resize columns to fit content
#         self.movieDetailsTable.resizeColumnsToContents()

#         # Stretch the last column for better visibility
#         self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)

#     def test_table_with_dummy_data(self):
#         """Test the table with dummy data."""
#         dummy_data = [
#             {'Title': 'Inception', 'Release Year': 2010, 'Language': 'English', 'Runtime': '148 mins', 'Rating': '8.8'},
#             {'Title': 'Interstellar', 'Release Year': 2014, 'Language': 'English', 'Runtime': '169 mins', 'Rating': '8.6'},
#             {'Title': 'The Dark Knight', 'Release Year': 2008, 'Language': 'English', 'Runtime': '152 mins', 'Rating': '9.0'},
#             {'Title': 'Dunkirk', 'Release Year': 2017, 'Language': 'English', 'Runtime': '106 mins', 'Rating': '7.9'}
#         ]

#         self.populate_movie_details_table(dummy_data)


# # Run the application
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     mainWin = TestApp()
#     mainWin.show()
#     sys.exit(app.exec())
class MovieDescriptionScreen(QtWidgets.QMainWindow):
    def __init__(self, movie_id=None):
        super(MovieDescriptionScreen, self).__init__()
        uic.loadUi('./Screens/MovieDescription.ui', self)  # Load the UI file for movie details

        self.play_button = self.findChild(QtWidgets.QPushButton, "play")  # Ensure the button is correctly referenced
        self.favorites_button = self.findChild(QtWidgets.QPushButton, "favorites")  # Ensure the button is correctly referenced

        self.movieDetailsTable = self.findChild(QtWidgets.QTableWidget, "MovieDescriptionTable")
        if movie_id:
            self.fetch_and_display_movie_details(movie_id)
        
        self.play_button.clicked.connect(self.play_movie)
        self.favorites_button.clicked.connect(self.fav_movie)
        

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

    def fetch_movies_by_crew(self, crew_name):
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
            return movies
            # if not movies:
            #     logging.warning(f"No movies found for: {crew_name}")
            #     QtWidgets.QMessageBox.warning(self, "No Movies Found", 
            #                                 f"No movies found for '{crew_name}'.")
            #     return

            # # Prepare the list of movie details for display
            # movie_list = []
            # for movie in movies:
            #     movie_details = {
            #         'Title': movie[0] or 'N/A',
            #         'Release Year': movie[1] or 'N/A',
            #         'Language': movie[2] or 'N/A',
            #         'Runtime': movie[3] or 'N/A',
            #         'Rating': movie[4] or 'N/A',
            #     }
            #     movie_list.append(movie_details)

            # print(f"Movie list for table: {movie_list}")  # Debug
            # # Populate the UI table or list with the movies
            # self.populate_movie_details_table(movie_list)

        except Exception as e:
            logging.error(f"Database error: {e}")
            return []  # Return an empty list if there's an error
        finally:
            cursor.close()
            connection.close()
    
    def format_movies_for_table(self, movies):
        """Convert database rows into a list of dictionaries."""
        formatted_movies = []
        for movie in movies:
            formatted_movies.append({
                'Title': movie[0] or 'N/A',
                'Release Year': movie[1] or 'N/A',
                'Language': movie[2] or 'N/A',
                'Runtime': movie[3] or 'N/A',
                'Rating': movie[4] or 'N/A',
            })
        return formatted_movies
        
    def populate_movie_details_table(self, movie_details):
        """Populate the details table with movie information."""
        self.movieDetailsTable.setRowCount(0)  # Clear existing rows
        print(f"Populating table with {len(movie_details)} entries.")  # Debug print

        if not movie_details:
            print("No movies to display!")  # Debug print
            QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
            return

        # Set the table headers
        headers = movie_details[0].keys()
        self.movieDetailsTable.setColumnCount(len(headers))
        self.movieDetailsTable.setHorizontalHeaderLabels(headers)

        # Add rows to the table
        for movie in movie_details:
            row_position = self.movieDetailsTable.rowCount()
            self.movieDetailsTable.insertRow(row_position)
            print(f"Adding row at position {row_position}: {movie}")  # Debug print
            for col, (key, value) in enumerate(movie.items()):
                self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))

        # Adjust the table layout
        self.movieDetailsTable.resizeColumnsToContents()
        self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
        print("Table population complete!")  # Debug print


    def fetch_and_display_movies_by_crew(self, crew_name):
        """Fetch movies by crew member and display them in the table."""
        print(f"Fetching movies for crew: {crew_name}")
        movies = self.fetch_movies_by_crew(crew_name)
        print(f"Movies fetched: {movies}")

        movie_details = self.format_movies_for_table(movies)
        print(f"Formatted movie details: {movie_details}")

        self.populate_movie_details_table([
    {'Title': 'Titanic', 'Release Year': 1997, 'Language': 'English', 'Runtime': 194, 'Rating': '7.8'}
])
        print("Movies displayed in the table.")



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
        print(f"movie id:{movie_id}")
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

    
    def test_table_with_dummy_data(self):
        # Dummy data for testing
        dummy_data = [
            {'Title': 'Inception', 'Release Year': 2010, 'Language': 'English', 'Runtime': '148', 'Rating': '8.8'},
            {'Title': 'Interstellar', 'Release Year': 2014, 'Language': 'English', 'Runtime': '169', 'Rating': '8.6'},
            {'Title': 'The Dark Knight', 'Release Year': 2008, 'Language': 'English', 'Runtime': '152', 'Rating': '9.0'}
        ]

        # Populate the table with dummy data
        self.populate_movie_details_table(dummy_data)

    # def populate_movie_details_table(self, movie_details):
    #     """Populate the details table with movie information."""
    #     self.movieDetailsTable.setRowCount(0)  # Clear existing rows

    #     # Debug: Print the incoming movie details 
    #     print(f"Received movie details: {movie_details}")

    #      # Case 2: If a list of dictionaries is passed
    #     if isinstance(movie_details, list) and all(isinstance(movie, dict) for movie in movie_details):
    #         if not movie_details:
    #             QtWidgets.QMessageBox.warning(self, "No Results", "No movies found to display.")
    #             return
            
    #         # Set the table column headers using the keys from the first dictionary
    #         self.movieDetailsTable.setColumnCount(len(movie_details[0]))
    #         self.movieDetailsTable.setHorizontalHeaderLabels(movie_details[0].keys())
            
    #         # Populate rows with each dictionary in the list
    #         for movie in movie_details:
    #             row_position = self.movieDetailsTable.rowCount()
    #             self.movieDetailsTable.insertRow(row_position)
    #             for col, (key, value) in enumerate(movie.items()):
    #                 self.movieDetailsTable.setItem(row_position, col, QtWidgets.QTableWidgetItem(str(value)))
    #         print(f"Inserted {self.movieDetailsTable.rowCount()} rows.")
    #     else:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Invalid data format. Cannot populate table.")
    #         return

    #     # Resize columns to fit the content
    #     self.movieDetailsTable.resizeColumnsToContents()

    #     # Stretch the last column for better visibility
    #     self.movieDetailsTable.horizontalHeader().setStretchLastSection(True)
    #     self.movieDetailsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

