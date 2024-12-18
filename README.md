# CineFlix: Movie Database Management System

This project is a Movie Database Management System (MDBMS) called CineFlix that manages movies, genres, crew members, cinema screenings, and customer-related activities such as reviews, favorites, and payment processing. The system allows adding, updating, deleting, and fetching movie data, associated genres, crew, cinema screenings, and customer interactions. This was completed as part of the course CS/CE 355/373: Database Systems.

## Features

1. **Movies Management:**
   - **Add a Movie:** Insert new movie details such as title, IMDB rating, release date, language, and duration.
   - **Update a Movie:** Modify existing movie details like title, release date, language, duration, and IMDB rating.
   - **Delete a Movie:** Remove a movie from the database, including its associated genres and crew members.

2. **Genres Management:**
   - **Add a Genre:** Insert a new genre into the database if it does not already exist.
   - **Update Movie Genre:** Associate a movie with a genre by updating the `MovieGenre` table.
   - **Delete Genre Association:** Remove a genre from a movie if the genre association is no longer required.

3. **Cinema Screenings Management**
    - **Add Cinema Screening:** Link a movie to a cinema and its screening schedule, including hall number, start time, end time, and format (e.g., 2D, 3D).
    - **Update Cinema Screening:** Modify the cinema hall, date, time, and format for existing movie screenings.
    - **Delete Cinema Screening:** Remove a movie from a specific cinema's screening schedule.
    - **Update Movie Screening Status:** If a movie has no more screenings, update the movie’s screening status.

4. **Crew Management:**
   - **Assign a Director:** Add or update the director's name for a movie.
   - **Remove Crew Members:** Delete crew members associated with a movie.

5. **Customer Interaction:**
   - **Review a Movie:** Customers can leave a review for a movie by rating it and adding comments.
   - **Favorite a Movie:** Customers can add movies to their favorites.
   - **View Customer History:** Track the movies watched by a customer and their review history.

6. **Payment Processing:**
   - **Store Payment Details:** Save customer payment details securely, including card information.

## Database Operations

The system uses SQL queries to interact with the database. Below are the key queries implemented in the project:

### Movies Table
- **Add a Movie:**
  ```sql
  INSERT INTO Movies (Title, IMDB_Rating, Release_Date, Language, Duration)
  VALUES (?, ?, ?, ?, ?);
  ```

- **Update a Movie:**
  ```sql
  UPDATE Movies
  SET Title = ?, Release_Date = ?, Language = ?, Duration = ?, IMDB_Rating = ?
  WHERE MovieID = ?;
  ```

- **Delete a Movie:**
  ```sql
  DELETE FROM MovieGenre WHERE MovieID = ?;
  DELETE FROM Crew WHERE MovieID = ?;
  DELETE FROM Movies WHERE MovieID = ?;
  ```

### Genres Table
- **Add a Genre:**
  ```sql
  INSERT INTO Genre (GenreName) VALUES (?);
  ```

- **Update Movie Genre:**
  ```sql
  UPDATE MovieGenre SET GenreID = ? WHERE MovieID = ?;
  ```

### Crew Table
- **Assign a Director:**
  ```sql
  INSERT INTO Crew (MovieID, CrewName, CrewPosition) VALUES (?, ?, 'Director');
  ```

- **Update Crew Member (Director):**
  ```sql
  UPDATE Crew SET CrewName = ? WHERE MovieID = ? AND CrewPosition = 'Director';
  ```

### Cinema Screenings Table
- **Add Cinema Screening:**
  ```sql
  INSERT INTO CinemaListing (CinemaID, MovieID, Hall_No, Date, Start_Time, End_Time, Format)
  VALUES (?, ?, ?, ?, ?, ?, ?);
  ```

- **Update Cinema Screening:**
  ```sql
  UPDATE CinemaListing
  SET Hall_No = ?, Date = ?, Start_Time = ?, End_Time = ?, Format = ?
  WHERE CinemaID = ? AND MovieID = ?;
  ```

- **Delete Cinema Screening:**
  ```sql
  DELETE FROM CinemaListing WHERE CinemaID = ? AND MovieID = ?;
  ```

- **Update Movie Screening Status:**
  ```sql
  SELECT COUNT(*) FROM CinemaListing WHERE MovieID = ?;
  -- If the count is 0, update the movie screening status
  UPDATE Movies SET Screening = 0 WHERE MovieID = ?;
  ```

### Customer Interaction
- **Add a Review:**
  ```sql
  INSERT INTO Reviews (Stars, Comment, Create_Date, Modify_Date, ReviewerID, MovieID)
  VALUES (?, ?, GETDATE(), GETDATE(), ?, ?);
  ```

- **Update a Review:**
  ```sql
  UPDATE Reviews
  SET Stars = ?, Comment = ?, Modify_Date = GETDATE(), MovieID = ?
  WHERE ReviewID = ?;
  ```

- **Add a Movie to Favorites:**
  ```sql
  INSERT INTO CustomerFavorites (CustomerID, MovieID)
  VALUES (?, ?);
  ```

### Payment Table
- **Store Payment Details:**
  ```sql
  INSERT INTO Payment (Card_Holder_Name, Card_Number, CVV, Card_Expiration_Date, CustomerID, CustomerRole)
  VALUES (?, ?, ?, ?, ?, ?);
  ```
  ```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie-db-management.git
   ```

2. Install the required dependencies.

3. Set up the database schema and tables as per the provided SQL scripts.

4. Configure the database connection settings in the application.

## Usage

- **Add a Movie:** To add a movie, use the "Add Movie" feature in the system, providing the movie title, IMDB rating, release date, language, and duration.
- **View Movies:** Movies can be viewed along with their genre, director, and IMDB rating.
- **Update Movie Information:** Modify movie details through the "Update Movie" feature.
- **Delete a Movie:** Remove a movie from the system, including its genre and crew members.
- **Add a Cinema Screening:** To add a screening, use the "Add Cinema Screening" feature, providing the cinema name, movie title, hall number, date, start time, end time, and format (e.g., 2D, 3D).
- **View Cinema Screenings:** Cinema screenings can be viewed along with movie details such as title, genre, and director.
- **Update a Cinema Screening:** Modify cinema hall, date, and time for existing movie screenings.
- **Delete a Cinema Screening:** Remove a movie from a specific cinema’s screening schedule.

### Movies, Genres, Crew, and Customer Interactions
Movies, genres, crew, and customer interactions are managed as described in the respective sections above.

## Contributions

Feel free to fork the repository and make contributions. Open a pull request to propose changes or improvements to the system.

## License

This project is licensed under the MIT License.

---
