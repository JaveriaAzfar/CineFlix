-- Register As Employee (Cinema Manager/Admin):
INSERT INTO Employee (EmployeeName, EmployeeDepartment, EmployeePosition, EmployeeExperience)
VALUES ('name', 'department', 'job_title', 'experience');

INSERT INTO Account (Email, Password, EmployeeID)
VALUES ('email', 'password', 'employeeID');

-- Cinema Managers to insert their cinema info upon registering:
INSERT INTO Cinema (Cinema_Name, Capacity, Address, City, Country, Website_Link)
VALUES ('cinema_name', 'cinema_capacity', 'cinema_address', 'cinema_city', 'cinema_country', 'cinema_website');

-- Register As Customer:
INSERT INTO Customer (CustomerRole, CustomerName, CustomerGender, CustomerDateOfBirth, CustomerAddress, CustomerCity, CustomerCountry)
VALUES ('role', 'name', 'gender', 'dob', 'address', 'city', 'country');

INSERT INTO Account (Email, Password, CustomerID)
VALUES ('email', 'password', 'customerID');

-- Premium Customer also have to enter their card details:
INSERT INTO Payment (Card_Holder_Name, Card_Number, CVV, Card_Expiration_Date, CustomerID, CustomerRole)
VALUES ('name', 'card_number', 'cvv', 'expiration_date', 'customer_id', 'role');

-- Login:
SELECT * FROM Account WHERE Email = 'email';

SELECT * FROM Account WHERE Email = 'email' AND Password = 'password';

---- Homepage:
-- Search by Title:
SELECT m.MovieID, m.Title
FROM Movies m
WHERE m.Title LIKE 'search_pattern';

-- using the title we get the entire movie description tuple from where we extract the movie id then use it to populate the decription table.

SELECT m.Title, 
       gen.GenreName, 
       c.CrewName AS Director, 
       YEAR(m.Release_Date), 
       m.Language, 
       m.Duration, 
       m.IMDB_Rating
FROM Movies m
LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director'
WHERE m.MovieID = 'movie_id';

-- Search by Genre:
SELECT m.Title, 
       YEAR(m.Release_Date), 
       m.Language, 
       m.Duration, 
       m.IMDB_Rating
FROM Movies m
LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
WHERE gen.GenreName = 'genre_name';

-- Search by Crew:
SELECT DISTINCT m.Title, 
                YEAR(m.Release_Date), 
                m.Language, 
                m.Duration, 
                m.IMDB_Rating
FROM Movies m
INNER JOIN Crew c ON m.MovieID = c.MovieID
WHERE c.CrewName = 'crew_name';

-- Search by Language:
SELECT m.Title, 
       YEAR(m.Release_Date), 
       m.Language, 
       m.Duration, 
       m.IMDB_Rating
FROM Movies m
WHERE m.Language = 'language';

-------- User Profile:
SELECT CustomerRole 
FROM Customer 
WHERE CustomerID = 'customer_id';

------ Non-Premium:
---- Favorites:
SELECT m.Title, 
       f.DateAdded
FROM CustomerFavorites f
JOIN Movies m ON f.MovieID = m.MovieID
WHERE f.CustomerID = 'customer_id';

---- History:
SELECT m.Title, 
       h.DateStarted, 
       h.DateFinished
FROM CustomerHistory h
JOIN Movies m ON h.MovieID = m.MovieID
WHERE h.CustomerID = 'customer_id';

------ Premium User Profile:
---- Favorites:
SELECT m.Title, 
       f.DateAdded
FROM CustomerFavorites f
JOIN Movies m ON f.MovieID = m.MovieID
WHERE f.CustomerID = 'customer_id';

---- History:
SELECT m.Title, 
       h.DateStarted, 
       h.DateFinished
FROM CustomerHistory h
JOIN Movies m ON h.MovieID = m.MovieID
WHERE h.CustomerID = 'customer_id';

---- Payment Details:
SELECT PaymentID, 
       Card_Holder_Name, 
       Card_Number, 
       CVV, 
       Card_Expiration_Date, 
       CustomerID, 
       CustomerRole
FROM Payment
WHERE CustomerID = 'customer_id';

---- Display Reviews:
SELECT r.ReviewID, 
       r.Stars, 
       r.Comment, 
       r.Create_Date, 
       r.Modify_Date, 
       r.MovieID, 
       m.Title
FROM Reviews r
JOIN Movies m ON r.MovieID = m.MovieID
WHERE r.ReviewerID = 'reviewer_id';

---- Delete Reviews:
DELETE FROM Reviews 
WHERE ReviewID = 'review_id';

---- Add Reviews:
SELECT MovieID 
FROM Movies 
WHERE Title LIKE 'movie_title';

INSERT INTO Reviews (Stars, Comment, Create_Date, Modify_Date, ReviewerID, MovieID)
VALUES ('stars', 'comment', 'GETDATE()', 'GETDATE()', 'reviewer_id', 'movie_id');

---- Update Reviews:
-- Fetch the MovieID for a title that matches the given pattern
SELECT MovieID 
FROM Movies 
WHERE Title LIKE 'movie_title';

-- Update the Reviews table with new details
UPDATE Reviews
SET Stars = stars, 
    Comment = 'comment', 
    Modify_Date = GETDATE(), 
    MovieID = 'movie_id'
WHERE ReviewID = 'review_id';

-------- Employee Profile:
SELECT EmployeePosition FROM Employee WHERE EmployeeID = 'employee_id'

------ Cinema Manager:
---- Display Cinema Listings:
select c.cinema_Name, m.title, w.hall_no, w.date, w.start_time, w.end_time, w.format
from CinemaListing w
inner join Cinema c on w.CinemaID = c.CinemaID
inner join Movies m on w.MovieID = m.MovieID

---- Delete Cinema Listings:
-- Fetch the CinemaID for the given Cinema_Name
SELECT CinemaID 
FROM Cinema 
WHERE Cinema_Name = 'cinema_name';

-- Fetch the MovieID for the given Title
SELECT MovieID 
FROM Movies 
WHERE Title = 'movie_title';

-- Delete the CinemaListing entry for the given CinemaID and MovieID
DELETE FROM CinemaListing 
WHERE CinemaID = 'cinema_id' 
  AND MovieID = 'movie_id';

-- Count the number of screenings for the given MovieID
SELECT COUNT(*) 
FROM CinemaListing 
WHERE MovieID = 'movie_id';

-- Update the Screening column in Movies table if no screenings exist
UPDATE Movies 
SET Screening = 0 
WHERE MovieID = 'movie_id';

---- Update Screening Status:
UPDATE Movies 
SET Screening = 'value' 
WHERE MovieID = 'movie_id';

---- Add Cinema Lisiting:
-- Fetch the CinemaID for the given Cinema_Name
SELECT CinemaID 
FROM Cinema 
WHERE Cinema_Name = 'cinema_name';

-- Fetch the MovieID for the given Title
SELECT MovieID 
FROM Movies 
WHERE Title = 'movie_title';

-- Insert a new CinemaListing entry
INSERT INTO CinemaListing (CinemaID, MovieID, Hall_No, Date, Start_Time, End_Time, Format)
VALUES ('cinema_id', 'movie_id', 'hall_no', 'date', 'start_time', 'end_time', 'format_');

-- Update the Screening column in the Movies table
UPDATE Movies 
SET Screening = 1 
WHERE MovieID = 'movie_id';

------ Admin:
---- Display Movies:
SELECT m.MovieID, 
       m.Title, 
       gen.GenreName, 
       c.CrewName AS Director, 
       YEAR(m.Release_Date), 
       m.Language,
       m.Duration, 
       m.IMDB_Rating, 
       m.Screening
FROM Movies m
LEFT JOIN MovieGenre g ON m.MovieID = g.MovieID
LEFT JOIN Genre gen ON g.GenreID = gen.GenreID
LEFT JOIN Crew c ON m.MovieID = c.MovieID AND c.CrewPosition = 'Director';

---- Add New Movies:
-- Insert a new movie into the Movies table
INSERT INTO Movies (Title, IMDB_Rating, Release_Date, Language, Duration)
VALUES ('title', 'rating', 'release_date', 'language', 'runtime');

-- Fetch the GenreID for the given GenreName
SELECT GenreID 
FROM Genre 
WHERE GenreName = 'genre';

-- Insert a new genre into the Genre table if it does not exist
INSERT INTO Genre (GenreName) 
VALUES ('genre');

-- Associate the MovieID with the GenreID in the MovieGenre table
INSERT INTO MovieGenre (MovieID, GenreID) 
VALUES ('movie_id', 'genre_id');

-- Add a director to the Crew table for the given movie
INSERT INTO Crew (MovieID, CrewName, CrewPosition) 
VALUES ('movie_id', 'director', 'Director');

---- Update Existing Movie:
-- Update the Movies table with new details for a specific MovieID
UPDATE Movies
SET Title = 'title', 
    Release_Date = 'release_date', 
    Language = 'language', 
    Duration = 'runtime', 
    IMDB_Rating = 'rating'
WHERE MovieID = 'movie_id';

-- Fetch the GenreID for the given GenreName
SELECT GenreID 
FROM Genre 
WHERE GenreName = 'genre';

-- Update the MovieGenre table to associate the new GenreID with the MovieID
UPDATE MovieGenre 
SET GenreID = 'genre_id' 
WHERE MovieID = 'movie_id';

-- Update the Crew table with a new director name for a specific MovieID
UPDATE Crew 
SET CrewName = 'director' 
WHERE MovieID = 'movie_id' 
AND CrewPosition = 'Director';

---- Delete Movies:
-- Delete the movie genre association for the given MovieID
DELETE FROM MovieGenre 
WHERE MovieID = 'movie_id';

-- Delete the director and other crew members for the given MovieID
DELETE FROM Crew 
WHERE MovieID = 'movie_id';

-- Delete the movie from the Movies table for the given MovieID
DELETE FROM Movies 
WHERE MovieID = 'movie_id';
