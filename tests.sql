select * from account
select * from Movies
select * from Customer
select * from Payment
select * from MovieGenre
select * from Crew
select * from Employee
select * from Genre
select * from CustomerFavorites
select * from CustomerHistory
select * from CinemaListing
select * from Cinema
select * from Reviews
select * from Movies

update Employee
set EmployeePosition = 'Cinema Manager'
where EmployeeName  = 'Javeria';
select * from Employee

DELETE FROM Account WHERE Email = '';
DELETE FROM Customer WHERE CustomerID = '43';


SELECT m.MovieID, m.Title
FROM Movies m
JOIN MovieGenre g ON m.MovieID = g.MovieID
JOIN Genre gen ON g.GenreID = gen.GenreID
WHERE gen.GenreName LIKE '%romance%'

select c.cinema_Name, m.title, w.hall_no, w.date, w.start_time, w.end_time, w.format
from CinemaListing w
inner join Cinema c on w.CinemaID = c.CinemaID
inner join Movies m on w.MovieID = m.MovieID

SELECT CinemaID FROM Cinema WHERE Cinema_Name = 'CineVerse'

SELECT CinemaID FROM Cinema WHERE Cinema_Name like 'CineVerse'
SELECT MovieID FROM Movies WHERE Title like 'Oppenheimer'

SELECT MovieID FROM Movies WHERE Title = 'The Notebook';
