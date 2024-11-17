-- Create a database called 'CinFlix'

CREATE TABLE Genre (
    GenreID INT IDENTITY(1,1) NOT NULL,
    GenreName VARCHAR(50) NOT NULL,
	PRIMARY KEY CLUSTERED 
(
    [GenreID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

SET IDENTITY_INSERT Genre ON
INSERT INTO Genre (GenreID, GenreName)
VALUES (1,'Horror'), (2,'Comedy'), (3,'Thriller'), (4,'Romance'), (5,'Action'), (6,'Sci-Fi');
SET IDENTITY_INSERT Genre OFF



CREATE TABLE Movies (
    MovieID INT  IDENTITY(1,1) NOT NULL,
    Title VARCHAR(100) NULL,
    IMDB_Rating DECIMAL(3,1) NULL,
    RottenTomatoes DECIMAL(3,1) NULL,
    Production_Date DATE NULL,
    Release_Date DATE NULL,
    Language VARCHAR(50) NULL,
    Duration int NULL ,
    Screening BIT NULL,
	Poster VARCHAR(255) NULL,
PRIMARY KEY CLUSTERED 
(
    [MovieID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

DECLARE @PosterFolderPath VARCHAR(255) = 'C:\Users\DELL\OneDrive - Habib University\Semesters\Semester 7\DBMS\Project\Posters\'; 

SET IDENTITY_INSERT Movies ON
INSERT INTO Movies (MovieID, Title, IMDB_Rating, RottenTomatoes, Production_Date, Release_Date, Language, Duration, Screening, Poster)
VALUES
    (1,'The Notebook', 7.8, 53.0, '2003-12-19', '2004-06-25', 'English', 123, 0, CONCAT(@PosterFolderPath, 1, '.jpg')),
    (2,'Titanic', 7.8, 88.0, '1997-11-18', '1997-12-19', 'English', 194, 0, CONCAT(@PosterFolderPath, 2, '.jpg')),
    (3,'La La Land', 8.0, 92.0, '2016-08-08', '2016-12-09', 'English', 128, 0, CONCAT(@PosterFolderPath, 3, '.jpg')),
    (4,'The Fault in Our Stars', 7.8, 81.0, '2013-12-13', '2014-06-06', 'English', 126, 0, CONCAT(@PosterFolderPath, 4, '.jpg')),
    (5,'John Wick: Chapter 4', 8.7, 96.0, '2022-12-16', '2023-03-24', 'English', 169, 1, CONCAT(@PosterFolderPath, 5, '.jpg')),
    (6,'Oppenheimer', 8.8, 94.0, '2022-07-11', '2023-07-21', 'English', 180, 1, CONCAT(@PosterFolderPath, 6, '.jpg')),
    (7,'Barbie', 7.1, 80.0, '2022-10-17', '2023-07-21', 'English', 114, 1, CONCAT(@PosterFolderPath, 7, '.jpg')),
    (8,'Dune: Part Two', 8.2, 85.0, '2022-10-21', '2023-11-03', 'English', 156, 1, CONCAT(@PosterFolderPath, 8, '.jpg')),
    (9,'Guardians of the Galaxy Vol. 3', 8.1, 88.0, '2022-12-08', '2023-05-05', 'English', 150, 0, CONCAT(@PosterFolderPath, 9, '.jpg')),
    (10,'Ant-Man and the Wasp: Quantumania', 6.8, 48.0, '2022-07-08', '2023-02-17', 'English', 125, 1, CONCAT(@PosterFolderPath, 10, '.jpg')),
    (11,'Avatar: The Way of Water', 7.8, 82.0, '2020-12-04', '2022-12-16', 'English', 192, 0, CONCAT(@PosterFolderPath, 11, '.jpg')),
    (12,'Everything Everywhere All At Once', 8.1, 96.0, '2021-09-17', '2022-03-11', 'English', 139, 1, CONCAT(@PosterFolderPath, 12, '.jpg')),
    (13,'Top Gun: Maverick', 8.3, 97.0, '2020-12-18', '2022-05-27', 'English', 131, 1, CONCAT(@PosterFolderPath, 13, '.jpg')),
    (14,'Black Panther: Wakanda Forever', 7.3, 84.0, '2021-07-08', '2022-11-11', 'English', 161, 1, CONCAT(@PosterFolderPath, 14, '.jpg')),
    (15,'Mission: Impossible - Dead Reckoning Part One', 7.9, 96.0, '2021-02-22', '2023-07-12', 'English', 163, 1, CONCAT(@PosterFolderPath, 15, '.jpg')),
    (16,'Scream VI', 6.5, 73.0, '2022-08-25', '2024-03-10', 'English', 122, 1, CONCAT(@PosterFolderPath, 16, '.jpg')),
    (17,'Insidious: The Red Door', 6.2, 57.0, '2022-10-17', '2023-07-07', 'English', 107, 0, CONCAT(@PosterFolderPath, 17, '.jpg')),
    (18,'Evil Dead Rise', 6.6, 72.0, '2022-06-17', '2023-04-21', 'English', 96, 1, CONCAT(@PosterFolderPath, 18, '.jpg')),
    (19,'M3GAN', 6.3, 77.0, '2022-05-13', '2022-12-02', 'English', 102, 1, CONCAT(@PosterFolderPath, 19, '.jpg')),
    (20,'Dont Worry Darling', 5.4, 47.0, '2021-11-08', '2022-09-23', 'English', 122, 0, CONCAT(@PosterFolderPath, 20, '.jpg')),
    (21,'Nope', 6.8, 84.0, '2022-07-08', '2022-07-22', 'English', 130, 1, CONCAT(@PosterFolderPath, 21, '.jpg')),
    (22,'The Matrix Resurrections', 5.7, 63.0, '2021-01-21', '2021-12-22', 'English', 148, 0,CONCAT(@PosterFolderPath, 22, '.jpg')),
    (23,'Spider-Man: No Way Home', 8.4, 93.0, '2020-07-23', '2021-12-17', 'English', 148, 1,CONCAT(@PosterFolderPath, 23, '.jpg')),
    (24,'Shazam! Fury of the Gods', 6.0, 49.0, '2022-08-15', '2023-03-17', 'English', 130, 1, CONCAT(@PosterFolderPath, 24, '.jpg')),
    (25,'Lightyear', 6.0, 75.0, '2021-08-20', '2022-06-17', 'English', 105, 0, CONCAT(@PosterFolderPath, 25, '.jpg')),
    (26,'The Batman', 7.9, 85.0, '2020-10-25', '2022-03-04', 'English', 176, 1, CONCAT(@PosterFolderPath, 26, '.jpg')),
    (27,'Jurassic World: Dominion', 5.7, 29.0, '2019-12-12', '2022-06-10', 'English', 147, 0, CONCAT(@PosterFolderPath, 27, '.jpg')),
    (28,'Doctor Strange in the Multiverse of Madness', 7.0, 74.0, '2020-04-04', '2022-05-06', 'English', 126, 1, CONCAT(@PosterFolderPath, 28, '.jpg')),
    (29,'Crazy Rich Asians', 7.0, 91.0, '2017-05-01', '2018-08-15', 'English', 121, 0, CONCAT(@PosterFolderPath, 29, '.jpg')),
    (30,'The Intern', 7.1, 73.0, '2014-02-05', '2015-09-25', 'English', 121, 0, CONCAT(@PosterFolderPath, 30, '.jpg')),
    (31,'Free Guy', 7.2, 80.0, '2019-10-20', '2021-08-13', 'English', 115, 0, CONCAT(@PosterFolderPath, 31, '.jpg')),
    (32,'The Conjuring: The Devil Made Me Do It', 6.3, 55.0, '2019-06-15', '2021-06-04', 'English', 112, 0, CONCAT(@PosterFolderPath, 32, '.jpg')),
    (33,'A Quiet Place Part II', 7.5, 91.0, '2019-09-15', '2021-05-28', 'English', 97, 0, CONCAT(@PosterFolderPath, 33, '.jpg')),
    (34,'Hereditary', 7.3, 89.0, '2017-01-01', '2018-06-08', 'English', 127, 0, CONCAT(@PosterFolderPath, 34, '.jpg'));
SET IDENTITY_INSERT Movies OFF

CREATE TABLE [dbo].[MovieGenre] (
    [MovieID] INT NOT NULL,
    [GenreID] INT NOT NULL,
    CONSTRAINT [PK_MovieGenre] PRIMARY KEY NONCLUSTERED (
        [MovieID] ASC,
        [GenreID] ASC
    ) WITH (
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY],
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID)
) ON [PRIMARY];
GO

-- Insert statements for the MovieGenre table
INSERT INTO MovieGenre (MovieID, GenreID)
VALUES
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 5), (6, 5), (7, 2), (8, 6), (9, 5), (10, 5),
    (11, 6), (12, 3), (13, 5), (14, 5), (15, 5), (16, 1), (17, 1), (18, 1), (19, 1), (20, 3),
    (21, 3), (22, 6), (23, 6), (24, 5), (25, 6), (26, 5), (27, 5), (28, 5), (29, 2), (30, 2), 
    (31, 2), (32, 1), (33, 1), (34, 1);


CREATE TABLE [dbo].[Crew] (
    [CrewID] INT NOT NULL IDENTITY(1,1),
    [CrewName] VARCHAR(100) NOT NULL,
    [CrewPosition] VARCHAR(50) NOT NULL,
    [MovieID] INT NOT NULL,
    CONSTRAINT [PK_Crew] PRIMARY KEY NONCLUSTERED (
        [CrewID] ASC
    ) WITH (
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY],
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON [PRIMARY];
GO


SET IDENTITY_INSERT [Crew] ON;

INSERT INTO [Crew] ([CrewID], [CrewName], [CrewPosition], [MovieID])
VALUES
    (1, 'Ryan Gosling', 'Actor', 1), (2, 'Rachel McAdams', 'Actor', 1), (3, 'Nick Cassavetes', 'Director', 1), (4, 'Gena Rowlands', 'Actor', 1), (5, 'James Garner', 'Actor', 1), (6, 'Leonardo DiCaprio', 'Actor', 2), (7, 'Kate Winslet', 'Actor', 2), (8, 'James Cameron', 'Director', 2), (9, 'Billy Zane', 'Actor', 2), (10, 'Kathy Bates', 'Actor', 2), 
	(11, 'Ryan Gosling', 'Actor', 3), (12, 'Emma Stone', 'Actor', 3), (13, 'Damien Chazelle', 'Director', 3), (14, 'John Legend', 'Actor', 3), (15, 'Rosemarie DeWitt', 'Actor', 3), (16, 'Shailene Woodley', 'Actor', 4), (17, 'Ansel Elgort', 'Actor', 4), (18, 'Josh Boone', 'Director', 4), (19, 'Nat Wolff', 'Actor', 4), (20, 'Laura Dern', 'Actor', 4), (21, 'Keanu Reeves', 'Actor', 5),
	(22, 'Donnie Yen', 'Actor', 5), (23, 'Chad Stahelski', 'Director', 5), (24, 'Bill Skarsgård', 'Actor', 5), (25, 'Laurence Fishburne', 'Actor', 5), (26, 'Cillian Murphy', 'Actor', 6), (27, 'Emily Blunt', 'Actor', 6), (28, 'Christopher Nolan', 'Director', 6), (29, 'Robert Downey Jr.', 'Actor', 6), (30, 'Matt Damon', 'Actor', 6), (31, 'Margot Robbie', 'Actor', 7),
	(32, 'Ryan Gosling', 'Actor', 7), (33, 'Greta Gerwig', 'Director', 7), (34, 'Simu Liu', 'Actor', 7), (35, 'America Ferrera', 'Actor', 7), (36, 'Timothée Chalamet', 'Actor', 8), (37, 'Zendaya', 'Actor', 8), (38, 'Denis Villeneuve', 'Director', 8), (39, 'Rebecca Ferguson', 'Actor', 8), (40, 'Josh Brolin', 'Actor', 8), (41, 'Chris Pratt', 'Actor', 9), (42, 'Zoe Saldana', 'Actor', 9), 
	(43, 'James Gunn', 'Director', 9), (44, 'Dave Bautista', 'Actor', 9), (45, 'Bradley Cooper', 'Voice Actor', 9), (46, 'Paul Rudd', 'Actor', 10), (47, 'Evangeline Lilly', 'Actor', 10), (48, 'Peyton Reed', 'Director', 10), (49, 'Michael Douglas', 'Actor', 10), (50, 'Michelle Pfeiffer', 'Actor', 10), (51, 'Sam Worthington', 'Actor', 11), (52, 'Zoe Saldana', 'Actor', 11), (53, 'James Cameron', 'Director', 11), 
	(54, 'Sigourney Weaver', 'Actor', 11), (55, 'Stephen Lang', 'Actor', 11), (56, 'Michelle Yeoh', 'Actor', 12), (57, 'Stephanie Hsu', 'Actor', 12), (58, 'Daniel Scheinert', 'Director', 12), (59, 'Ke Huy Quan', 'Actor', 12), (60, 'Jamie Lee Curtis', 'Actor', 12), (61, 'Tom Cruise', 'Actor', 13), (62, 'Jennifer Connelly', 'Actor', 13), (63, 'Joseph Kosinski', 'Director', 13), (64, 'Miles Teller', 'Actor', 13), 
	(65, 'Jon Hamm', 'Actor', 13), (66, 'Letitia Wright', 'Actor', 14), (67, 'Lupita Nyongo', 'Actor', 14), (68, 'Ryan Coogler', 'Director', 14), (69, 'Danai Gurira', 'Actor', 14), (70, 'Winston Duke', 'Actor', 14), (71, 'Tom Cruise', 'Actor', 15), (72, 'Hayley Atwell', 'Actor', 15), (73, 'Christopher McQuarrie', 'Director', 15), (74, 'Simon Pegg', 'Actor', 15), 
(75, 'Rebecca Ferguson', 'Actor', 15), (76, 'Melissa Barrera', 'Actor', 16), (77, 'Jenna Ortega', 'Actor', 16), (78, 'Matt Bettinelli-Olpin', 'Director', 16), (79, 'Courteney Cox', 'Actor', 16), (80, 'Neve Campbell', 'Actor', 16), (81, 'Patrick Wilson', 'Actor', 17), (82, 'Ty Simpkins', 'Actor', 17), (83, 'James Wan', 'Director', 
17), (84, 'Lin Shaye', 'Actor', 17), (85, 'Rose Byrne', 'Actor', 17), (86, 'Alyssa Sutherland', 'Actor', 18), (87, 'Lily Sullivan', 'Actor', 18), (88, 'Lee Cronin', 'Director', 18), (89, 'Gabrielle Echols', 'Actor', 18), (90, 'Morgan Davies', 'Actor', 18), (91, 'Allison Williams', 'Actor', 19), (92, 'Violet McGraw', 'Actor', 19), 
(93, 'Gerard Johnstone', 'Director', 19), (94, 'Ronny Chieng', 'Actor', 19), (95, 'Jenna Davis', 'Voice Actor', 19), (96, 'Florence Pugh', 'Actor', 20), (97, 'Harry Styles', 'Actor', 20), (98, 'Olivia Wilde', 'Director', 20), (99, 'Gemma Chan', 'Actor', 20), (100, 'Chris Pine', 'Actor', 20), (101, 'Daniel Kaluuya', 'Actor', 21), (102, 'Keke Palmer', 'Actor', 21), (103, 'Jordan Peele', 'Director', 21), 
(104, 'Steven Yeun', 'Actor', 21), (105, 'Brandon Perea', 'Actor', 21), (106, 'Keanu Reeves', 'Actor', 22), (107, 'Carrie-Anne Moss', 'Actor', 22), (108, 'Lana Wachowski', 'Director', 22), (109, 'Neil Patrick Harris', 'Actor', 22), (110, 'Jessica Henwick', 'Actor', 22), (111, 'Tom Holland', 'Actor', 23), (112, 'Zendaya', 'Actor', 23), (113, 'Jon Watts', 'Director', 23), (114, 'Benedict Cumberbatch', 'Actor', 23), 
(115, 'Jacob Batalon', 'Actor', 23), (116, 'Zachary Levi', 'Actor', 24), (117, 'Helen Mirren', 'Actor', 24), (118, 'David F. Sandberg', 'Director', 24), (119, 'Lucy Liu', 'Actor', 24), (120, 'Djimon Hounsou', 'Actor', 24), (121, 'Chris Evans', 'Voice Actor', 25), (122, 'Keke Palmer', 'Voice Actor', 25), (123, 'Angus MacLane', 'Director', 
25), (124, 'Taika Waititi', 'Voice Actor', 25), (125, 'Dale Soules', 'Voice Actor', 25), (126, 'Robert Pattinson', 'Actor', 26), (127, 'Zoë Kravitz', 'Actor', 26), (128, 'Matt Reeves', 'Director', 26), (129, 'Jeffrey Wright', 'Actor', 26), (130, 'Colin Farrell', 'Actor', 26), (131, 'Chris Pratt', 'Actor', 27), (132, 'Bryce Dallas 
Howard', 'Actor', 27), (133, 'Colin Trevorrow', 'Director', 27), (134, 'Laura Dern', 'Actor', 27), (135, 'Sam Neill', 'Actor', 27), (136, 'Benedict Cumberbatch', 'Actor', 28), (137, 'Elizabeth Olsen', 'Actor', 28), (138, 'Sam Raimi', 'Director', 28), (139, 'Rachel McAdams', 'Actor', 28), (140, 'Chiwetel Ejiofor', 'Actor', 28), (141, 'Constance Wu', 'Actor', 29), (142, 'Henry Golding', 'Actor', 29),
(143, 'Jon M. Chu', 'Director', 29), (144, 'Michelle Yeoh', 'Actor', 29), (145, 'Gemma Chan', 'Actor', 29), (146, 'Robert De Niro', 'Actor', 30), (147, 'Anne Hathaway', 'Actor', 30), (148, 'Nancy Meyers', 'Director', 30), (149, 'Rene Russo', 'Actor', 30), (150, 'Adam DeVine', 'Actor', 30), (151, 'Ryan Reynolds', 'Actor', 31), (152, 'Jodie Comer', 'Actor', 31), 
(153, 'Shawn Levy', 'Director', 31), (154, 'Taika Waititi', 'Actor', 31), (155, 'Joe Keery', 'Actor', 31), (156, 'Patrick Wilson', 'Actor', 32), (157, 'Vera Farmiga', 'Actor', 32), (158, 'Michael Chaves', 'Director', 32), (159, 'Ruairi O Connor', 'Actor', 32), (160, 'Sarah Catherine Hook', 'Actor', 32), 
(161, 'Emily Blunt', 'Actor', 33), (162, 'Cillian Murphy', 'Actor', 33), (163, 'John Krasinski', 'Director', 33), (164, 'Millicent Simmonds', 'Actor', 33), (165, 'Noah Jupe', 'Actor', 33), (166, 'Toni Collette', 'Actor', 34), (167, 'Alex Wolff', 'Actor', 34), (168, 'Ari Aster', 'Director', 34), (169, 'Milly Shapiro', 'Actor', 34), (170, 'Gabriel Byrne', 'Actor', 34);

SET IDENTITY_INSERT [Crew] OFF;
GO


CREATE TABLE [dbo].[Customer] (
    [CustomerID] INT NOT NULL IDENTITY(1,1),
    [CustomerRole] VARCHAR(50) NOT NULL,
    [CustomerName] VARCHAR(100) NOT NULL,
    [CustomerGender] VARCHAR(10) NOT NULL,
    [CustomerDateOfBirth] DATE NOT NULL,
    [CustomerAddress] VARCHAR(255) NOT NULL,
    [CustomerCity] VARCHAR(100) NOT NULL,
    [CustomerCountry] VARCHAR(100) NOT NULL,
    CONSTRAINT [PK_Customer] PRIMARY KEY NONCLUSTERED (
        [CustomerID] ASC
    ) WITH (
        PAD_INDEX = OFF,
        STATISTICS_NORECOMPUTE = OFF,
        IGNORE_DUP_KEY = OFF,
        ALLOW_ROW_LOCKS = ON,
        ALLOW_PAGE_LOCKS = ON
    ) ON [PRIMARY]
) ON [PRIMARY];
GO

SET IDENTITY_INSERT Customer ON;

INSERT INTO Customer (CustomerID, CustomerRole, CustomerName, CustomerGender, CustomerDateOfBirth, CustomerAddress, CustomerCity, CustomerCountry)
VALUES
    (1, 'Regular', 'John Doe', 'Male', '1985-05-15', '123 Elm St', 'Springfield', 'USA'),
    (2, 'Premium', 'Jane Smith', 'Female', '1990-08-20', '456 Maple Ave', 'Metropolis', 'USA'),
    (3, 'Regular', 'Alice Johnson', 'Female', '1988-02-11', '789 Oak St', 'Gotham', 'USA'),
    (4, 'Regular', 'Bob Brown', 'Male', '1992-04-05', '135 Pine St', 'Star City', 'USA'),
    (5, 'Premium', 'Chris Evans', 'Male', '1980-06-30', '246 Cedar Rd', 'Smallville', 'USA'),
    (6, 'Regular', 'Emily Davis', 'Female', '1986-12-12', '357 Birch Ln', 'Coast City', 'USA'),
    (7, 'Regular', 'Michael Wilson', 'Male', '1995-11-25', '468 Spruce Ct', 'Central City', 'USA'),
    (8, 'Premium', 'Sarah Taylor', 'Female', '1982-01-15', '579 Willow Blvd', 'National City', 'USA'),
    (9, 'Regular', 'David Martinez', 'Male', '1989-03-30', '690 Ash Dr', 'Bay City', 'USA'),
    (10, 'Regular', 'Emma Thompson', 'Female', '1993-09-05', '801 Cherry Ln', 'Starling City', 'USA'),
    (11, 'Premium', 'James Lee', 'Male', '1978-10-10', '912 Maple Rd', 'Pawnee', 'USA'),
    (12, 'Regular', 'Isabella Garcia', 'Female', '1991-07-22', '1020 Walnut St', 'Sunnydale', 'USA');

SET IDENTITY_INSERT Customer OFF;
GO


CREATE TABLE [dbo].[Reviews] (
    [ReviewID] INT NOT NULL IDENTITY(1,1),
    [Stars] INT CHECK (Stars BETWEEN 1 AND 5),
    [Comment] VARCHAR(255),
    [Create_Date] DATE,
    [Modify_Date] DATE,
    [ReviewerID] INT,
    [MovieID] INT,
    FOREIGN KEY (ReviewerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON [PRIMARY];
GO

SET IDENTITY_INSERT [Reviews] ON;

INSERT INTO Reviews (ReviewID, Stars, Comment, Create_Date, Modify_Date, ReviewerID, MovieID) VALUES
(1, 5, 'Amazing movie! Loved the performances.', '2024-01-01', '2024-01-01', 1, 1),
(2, 4, 'Great story, but a bit slow in the middle.', '2024-01-02', '2024-01-02', 2, 1),
(3, 3, 'It was okay, not my favorite.', '2024-01-03', '2024-01-03', 3, 2),
(4, 5, 'Incredible visuals and soundtrack!', '2024-01-04', '2024-01-04', 1, 2),
(5, 2, 'Did not live up to the hype.', '2024-01-05', '2024-01-05', 4, 3),
(6, 4, 'Fantastic movie! Would watch again.', '2024-01-06', '2024-01-06', 5, 3),
(7, 3, 'Had some good moments, but overall just okay.', '2024-01-07', '2024-01-07', 1, 4),
(8, 4, 'Great chemistry between the leads.', '2024-01-08', '2024-01-08', 6, 4),
(9, 5, 'One of the best movies of the year!', '2024-01-09', '2024-01-09', 7, 5),
(10, 4, 'Entertaining and fun!', '2024-01-10', '2024-01-10', 8, 5),
(11, 5, 'A masterpiece, highly recommended!', '2024-01-11', '2024-01-11', 1, 6),
(12, 4, 'Solid film with great performances.', '2024-01-12', '2024-01-12', 2, 6),
(13, 3, 'Not bad, but expected more.', '2024-01-13', '2024-01-13', 3, 7),
(14, 4, 'Enjoyable, with a few plot holes.', '2024-01-14', '2024-01-14', 4, 7),
(15, 5, 'Brilliant direction and acting!', '2024-01-15', '2024-01-15', 5, 8),
(16, 4, 'A solid continuation of the franchise.', '2024-01-16', '2024-01-16', 1, 9),
(17, 3, 'Had some good action scenes.', '2024-01-17', '2024-01-17', 2, 9),
(18, 5, 'Absolutely loved this movie!', '2024-01-18', '2024-01-18', 3, 10),
(19, 4, 'Funny and entertaining!', '2024-01-19', '2024-01-19', 4, 10),
(20, 5, 'The plot twist was unexpected!', '2024-01-20', '2024-01-20', 5, 11),
(21, 3, 'It was average.', '2024-01-21', '2024-01-21', 6, 12),
(22, 2, 'Not great, I expected better.', '2024-01-22', '2024-01-22', 7, 12),
(23, 5, 'A cinematic masterpiece!', '2024-01-23', '2024-01-23', 1, 13),
(24, 4, 'Great story and character development.', '2024-01-24', '2024-01-24', 2, 13),
(25, 5, 'One of my all-time favorites!', '2024-01-25', '2024-01-25', 3, 14),
(26, 4, 'Beautifully shot and well-acted.', '2024-01-26', '2024-01-26', 4, 14),
(27, 3, 'Decent but not memorable.', '2024-01-27', '2024-01-27', 5, 15),
(28, 5, 'Heartwarming and touching.', '2024-01-28', '2024-01-28', 6, 16),
(29, 4, 'Very enjoyable experience!', '2024-01-29', '2024-01-29', 7, 17),
(30, 3, 'Had its moments.', '2024-01-30', '2024-01-30', 8, 18),
(31, 4, 'Kept me on the edge of my seat!', '2024-01-31', '2024-01-31', 1, 19),
(32, 2, 'Disappointing sequel.', '2024-02-01', '2024-02-01', 2, 20),
(33, 5, 'Incredible performances by the cast!', '2024-02-02', '2024-02-02', 3, 21),
(34, 4, 'Good film, but a bit too long.', '2024-02-03', '2024-02-03', 4, 22),
(35, 5, 'Loved every minute of it!', '2024-02-04', '2024-02-04', 5, 23),
(36, 4, 'A great addition to the genre.', '2024-02-05', '2024-02-05', 6, 24),
(37, 3, 'It was fine, nothing special.', '2024-02-06', '2024-02-06', 7, 25),
(38, 2, 'Not my cup of tea.', '2024-02-07', '2024-02-07', 8, 26),
(39, 5, 'A brilliant and thought-provoking film.', '2024-02-08', '2024-02-08', 1, 27),
(40, 4, 'Engaging and well-paced.', '2024-02-09', '2024-02-09', 2, 28),
(41, 3, 'Had potential, but fell flat.', '2024-02-10', '2024-02-10', 3, 29),
(42, 5, 'A must-see for everyone!', '2024-02-11', '2024-02-11', 4, 30),
(43, 4, 'Interesting concept and execution.', '2024-02-12', '2024-02-12', 5, 31),
(44, 3, 'Could have been better, but worth a watch.', '2024-02-13', '2024-02-13', 6, 32),
(45, 4, 'A thrilling ride from start to finish.', '2024-02-14', '2024-02-14', 7, 33),
(46, 5, 'An unforgettable experience!', '2024-02-15', '2024-02-15', 8, 34);


SET IDENTITY_INSERT [Reviews] Off
GO


-- Create CustomerFavorites Table
CREATE TABLE [dbo].[CustomerFavorites] (
    [CustomerID] INT NOT NULL,
    [MovieID] INT NOT NULL,
    [DateAdded] DATE NOT NULL,
    CONSTRAINT [PK_CustomerFavorites] PRIMARY KEY ([CustomerID], [MovieID]) ON [PRIMARY],
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON [PRIMARY];
GO

INSERT INTO CustomerFavorites (CustomerID, MovieID, DateAdded) VALUES
(1, 1, '2024-01-01'),
(1, 2, '2024-01-02'),
(2, 3, '2024-01-03'),
(2, 5, '2024-01-04'),
(3, 6, '2024-01-05'),
(3, 9, '2024-01-06'),
(4, 10, '2024-01-07'),
(4, 11, '2024-01-08'),
(5, 12, '2024-01-09'),
(5, 14, '2024-01-10'),
(6, 15, '2024-01-11'),
(6, 16, '2024-01-12'),
(7, 18, '2024-01-13'),
(7, 19, '2024-01-14'),
(8, 21, '2024-01-15'),
(8, 22, '2024-01-16'),
(9, 23, '2024-01-17'),
(9, 25, '2024-01-18'),
(10, 27, '2024-01-19'),
(10, 28, '2024-01-20'),
(11, 29, '2024-01-21'),
(11, 31, '2024-01-22'),
(12, 32, '2024-01-23'),
(12, 34, '2024-01-24');
GO


-- Create Payment Table
CREATE TABLE [dbo].[Payment] (
    [PaymentID] INT PRIMARY KEY IDENTITY(1,1),
    [Card_Holder_Name] VARCHAR(100) NOT NULL,
    [Card_Number] NUMERIC(16, 0) NOT NULL,
    [CVV] NUMERIC(3, 0) NOT NULL,
    [Card_Expiration_Date] DATE NOT NULL,
    [CustomerID] INT NOT NULL,
    [CustomerRole] VARCHAR(50) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
) ON [PRIMARY];
GO

SET IDENTITY_INSERT [Payment] ON

INSERT INTO Payment (PaymentID, Card_Holder_Name, Card_Number, CVV, Card_Expiration_Date, CustomerID, CustomerRole) VALUES
(1, 'Jane Smith', 4567891234567890, 456, '2026-12-31', 2, 'Premium'),
(2, 'Chris Evans', 2468101214161820, 789, '2025-05-30', 5, 'Premium'),
(3, 'Sarah Taylor', 5791234567890123, 123, '2027-03-15', 8, 'Premium'),
(4, 'James Lee', 9123456789012345, 321, '2026-09-20', 11, 'Premium');
SET IDENTITY_INSERT [Payment] OFF
GO



-- Create CustomerHistory Table
CREATE TABLE [dbo].[CustomerHistory] (
    [CustomerID] INT NOT NULL,
    [MovieID] INT NOT NULL,
    [DateStarted] DATE NOT NULL,
    [DateFinished] DATE NOT NULL,
    CONSTRAINT [PK_CustomerHistory] PRIMARY KEY ([CustomerID], [MovieID]) ON [PRIMARY],
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON [PRIMARY];
GO

INSERT INTO CustomerHistory (CustomerID, MovieID, DateStarted, DateFinished) VALUES
(1, 1, '2024-01-01', '2024-01-02'),
(1, 3, '2024-01-03', '2024-01-04'),
(2, 5, '2024-01-05', '2024-01-06'),
(2, 7, '2024-01-07', '2024-01-08'),
(3, 9, '2024-01-09', '2024-01-10'),
(3, 10, '2024-01-11', '2024-01-12'),
(4, 12, '2024-01-13', '2024-01-14'),
(4, 14, '2024-01-15', '2024-01-16'),
(5, 15, '2024-01-17', '2024-01-18'),
(5, 20, '2024-01-19', '2024-01-20'),
(6, 21, '2024-01-21', '2024-01-22'),
(6, 22, '2024-01-23', '2024-01-24'),
(7, 24, '2024-01-25', '2024-01-26'),
(7, 26, '2024-01-27', '2024-01-28'),
(8, 28, '2024-01-29', '2024-01-30'),
(8, 30, '2024-01-31', '2024-02-01'),
(9, 31, '2024-02-02', '2024-02-03'),
(9, 33, '2024-02-04', '2024-02-05'),
(10, 34, '2024-02-06', '2024-02-07'),
(10, 8, '2024-02-08', '2024-02-09'),
(11, 2, '2024-02-10', '2024-02-11'),
(11, 4, '2024-02-12', '2024-02-13'),
(12, 6, '2024-02-14', '2024-02-15'),
(12, 16, '2024-02-16', '2024-02-17');
GO

CREATE TABLE [dbo].[Employee] (
    [EmployeeID] INT PRIMARY KEY IDENTITY(1,1),
    [EmployeeName] VARCHAR(100) NOT NULL,
    [EmployeeDepartment] VARCHAR(100) NOT NULL,
    [EmployeePosition] VARCHAR(100) NOT NULL,
    [EmployeeExperience] INT NOT NULL
) ON [PRIMARY];
GO

SET IDENTITY_INSERT [Employee] ON

INSERT INTO Employee (EmployeeID, EmployeeName, EmployeeDepartment, EmployeePosition, EmployeeExperience) VALUES
(1, 'John Doe', 'HR', 'Manager', 5),
(2, 'Jane Smith', 'IT', 'Developer', 3),
(3, 'Sam Wilson', 'Finance', 'Analyst', 7),
(4, 'Lucy Brown', 'Marketing', 'Executive', 2),
(5, 'Mike Johnson', 'Cinema Manager', 'Supervisor', 4),
(6, 'Emily Davis', 'Cinema Manager', 'Shift Manager', 6),
(7, 'Robert Lee', 'Cinema Manager', 'Senior Manager', 8),
(8, 'Anna White', 'Cinema Manager', 'Assistant Manager', 5),
(9, 'Mark Thompson', 'Sales', 'Sales Associate', 3),
(10, 'Sophia Turner', 'Cinema Manager', 'Operations Manager', 7);
SET IDENTITY_INSERT [Employee] OFF
GO

CREATE TABLE [dbo].[Cinema] (
    [CinemaID] INT PRIMARY KEY IDENTITY(1,1),
    [Cinema_Name] VARCHAR(100) NOT NULL,
    [Capacity] NUMERIC(5,0) NOT NULL,
    [Address] NVARCHAR(200) NOT NULL,
    [City] VARCHAR(50) NOT NULL,
    [Country] VARCHAR(50) NOT NULL,
    [Website_Link] NVARCHAR(200)
) ON [PRIMARY];
GO

SET IDENTITY_INSERT [Cinema] ON

INSERT INTO Cinema (CinemaID, Cinema_Name, Capacity, Address, City, Country, Website_Link) VALUES
(1, 'Silver Screen Palace', 200, '123 Main St', 'Los Angeles', 'USA', 'http://cinemaone.com'),
(2, 'DreamLight Cinemas', 150, '456 Broadway Ave', 'New York', 'USA', 'http://cinematwo.com'),
(3, 'The Velvet Reel', 180, '789 Hollywood Blvd', 'Los Angeles', 'USA', 'http://cinemathree.com'),
(4, 'CineVerse', 220, '101 Market St', 'San Francisco', 'USA', 'http://cinemafour.com'),
(5, 'Majestic Movieland', 250, '202 Grand Ave', 'Chicago', 'USA', 'http://cinemafive.com');
SET IDENTITY_INSERT [Cinema] OFF
GO

CREATE TABLE [dbo].[CinemaListing] (
    [CinemaID] INT NOT NULL,
    [MovieID] INT NOT NULL,
    [Hall_No] INT NOT NULL,
    [Date] DATE NOT NULL,
    [Start_Time] TIME NOT NULL,
    [End_Time] TIME NOT NULL,
    [Format] NVARCHAR(50) NOT NULL,
    CONSTRAINT [PK_CinemaListing] PRIMARY KEY ([CinemaID], [MovieID], [Hall_No], [Date], [Start_Time]) ON [PRIMARY],
    FOREIGN KEY (CinemaID) REFERENCES Cinema(CinemaID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
) ON [PRIMARY];
GO

INSERT INTO [dbo].[CinemaListing] (CinemaID, MovieID, Hall_No, Date, Start_Time, End_Time, Format)
VALUES
(1, 5, 1, '2024-11-20', '14:00:00', '16:49:00', 'IMAX'),
(1, 6, 2, '2024-11-20', '16:30:00', '19:00:00', 'Digital'),
(1, 7, 3, '2024-11-20', '18:45:00', '20:39:00', 'Standard'),
(2, 8, 1, '2024-11-10', '13:00:00', '15:36:00', 'IMAX'),
(2, 9, 2, '2024-11-10', '14:45:00', '17:15:00', 'Standard'),
(2, 10, 3, '2024-11-11', '16:30:00', '18:35:00', 'Digital'),
(3, 11, 1, '2024-12-17', '14:15:00', '16:07:00', 'IMAX'),
(3, 12, 2, '2024-12-17', '17:00:00', '18:20:00', '3D'),
(3, 13, 3, '2024-12-18', '19:30:00', '21:00:00', 'Standard'),
(4, 14, 1, '2024-11-25', '13:30:00', '15:35:00', 'Digital'),
(4, 15, 2, '2024-11-26', '15:45:00', '18:00:00', '3D'),
(4, 16, 3, '2024-12-02', '16:00:00', '17:45:00', 'IMAX'),
(5, 17, 1, '2024-10-05', '13:30:00', '15:30:00', 'Standard'),
(5, 18, 2, '2024-10-06', '16:00:00', '17:45:00', 'Digital'),
(5, 19, 3, '2024-10-10', '18:00:00', '19:40:00', 'IMAX');
GO

CREATE TABLE [dbo].[Account] (
    [Email] VARCHAR(100) PRIMARY KEY,
    [Password] VARCHAR(100) NOT NULL,
    [CustomerID] INT NULL,
    [EmployeeID] INT NULL,
    FOREIGN KEY (CustomerID) REFERENCES [dbo].[Customer](CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES [dbo].[Employee](EmployeeID)
) ON [PRIMARY];
GO

INSERT INTO [dbo].[Account] (Email, Password, CustomerID, EmployeeID)
VALUES
('customer1@example.com', 'R#2pqA1l', 1, NULL),
('customer2@example.com', '7VwI8zFq', 2, NULL),
('customer3@example.com', 'zJ3mK6L9', 3, NULL),
('customer4@example.com', 'Wm9D2qNx', 4, NULL),
('customer5@example.com', 'Lz8V2rB#', 5, NULL),
('customer6@example.com', 'uR9sWj6t', 6, NULL),
('customer7@example.com', 'Zb0C7oXs', 7, NULL),
('customer8@example.com', '3KvBb0Nj', 8, NULL),
('customer9@example.com', 'T9CwJhZr', 9, NULL),
('customer10@example.com', 'zD3Rk8L#', 10, NULL),
('customer11@example.com', 'PqX7vYb0', 11, NULL),
('customer12@example.com', 'HfW6bQz9', 12, NULL),
('employee1@example.com', 'Fq2nC7wZ', NULL, 1),
('employee2@example.com', 'N8nW1zA3', NULL, 2),
('employee3@example.com', 'Jb7zXs4M', NULL, 3),
('employee4@example.com', 'Sg3PzR1F', NULL, 4),
('employee5@example.com', 'WvR9mFq6', NULL, 5),
('employee6@example.com', 'YhB2vX9S', NULL, 6),
('employee7@example.com', 'VbF1qJ7N', NULL, 7),
('employee8@example.com', 'P9Nw8zHg', NULL, 8),
('employee9@example.com', 'K5fG3tV1', NULL, 9),
('employee10@example.com', 'RjZ2M7C#', NULL, 10);
GO

