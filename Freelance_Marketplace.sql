-- Create type user_type_enum as enum for Users Table
CREATE TYPE user_type_enum AS ENUM ('freelancer', 'client');

-- Create table Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type user_type_enum NOT NULL
);

-- Insert 20 records into Users table with real names including Aditya, Robin, and Alex
INSERT INTO Users (username, pass, email, user_type) VALUES
('Aditya', 'root', 'aditya@example.com', 'freelancer'),
('Robin', 'root', 'robin@example.com', 'freelancer'),
('Alex', 'root', 'alex@example.com', 'freelancer'),
('John_Doe', 'password123', 'john.doe@example.com', 'freelancer'),
('Jane_Smith', 'password124', 'jane.smith@example.com', 'client'),
('Michael_Johnson', 'password125', 'michael.johnson@example.com', 'freelancer'),
('Emily_Davis', 'password126', 'emily.davis@example.com', 'client'),
('Daniel_Moore', 'password127', 'daniel.moore@example.com', 'freelancer'),
('Liam_Wright', 'password198', 'liam.wright@example.com', 'freelancer'),
('Sophia_Hill', 'password199', 'sophia.hill@example.com', 'client'),
('Ethan_Baker', 'password200', 'ethan.baker@example.com', 'freelancer'),
('Olivia_Wilson', 'password201', 'olivia.wilson@example.com', 'client'),
('Robert_Brown', 'password128', 'robert.brown@example.com', 'freelancer'),
('Sarah_Johnson', 'password129', 'sarah.johnson@example.com', 'client'),
('David_Taylor', 'password130', 'david.taylor@example.com', 'freelancer'),
('Emma_Miller', 'password131', 'emma.miller@example.com', 'client'),
('James_Anderson', 'password132', 'james.anderson@example.com', 'freelancer'),
('Mia_Walker', 'password133', 'mia.walker@example.com', 'client'),
('Chris_White', 'password134', 'chris.white@example.com', 'freelancer'),
('Ava_Clark', 'password135', 'ava.clark@example.com', 'client');

-- Create type status_enum as enum for Jobs table
CREATE TYPE status_enum AS ENUM ('open', 'closed');

-- Create table Jobs
CREATE TABLE Jobs (
    job_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    budget INT,
    status status_enum,
    FOREIGN KEY (client_id) REFERENCES Users(user_id)
);

-- Insert 20 records into Jobs table (client_id values refer to actual users from Users table)
INSERT INTO Jobs (client_id, title, budget, status) VALUES
(5, 'Web Design Project', 500, 'open'),
(6, 'Mobile App Development', 1500, 'open'),
(8, 'Data Science Consultation', 700, 'closed'),
(10, 'E-commerce Website', 2000, 'open'),
(12, 'SEO Optimization', 300, 'closed'),
(14, 'Social Media Campaign', 800, 'open'),
(16, 'Custom Logo Design', 150, 'open'),
(18, 'Business Analytics Report', 950, 'closed'),
(20, 'Backend API Development', 1200, 'open'),
(5, 'Content Writing for Blog', 400, 'closed'),
(7, 'Graphic Design', 500, 'open'),
(9, 'App Testing', 1000, 'open'),
(11, 'Data Entry', 200, 'closed'),
(13, 'Database Management', 1200, 'open'),
(15, 'Copywriting', 700, 'closed'),
(17, 'Digital Marketing', 900, 'open'),
(19, 'Video Editing', 600, 'open'),
(4, 'Project Management', 1500, 'closed'),
(6, 'Logo Creation', 250, 'open'),
(8, 'Photography Services', 300, 'open');

-- Create type status_enum_proposals as enum for Proposals table
CREATE TYPE status_enum_proposals AS ENUM('submitted', 'accepted', 'rejected');

-- Create table Proposals
CREATE TABLE Proposals (
    proposal_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    proposed_amount INT,
    status status_enum_proposals,
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id),
    FOREIGN KEY (freelancer_id) REFERENCES Users(user_id)
);

-- Insert 20 records into Proposals table (matching job_id and freelancer_id)
INSERT INTO Proposals (job_id, freelancer_id, proposed_amount, status) VALUES
(1, 1, 550, 'submitted'), -- Aditya applies for Job 1
(2, 3, 1450, 'accepted'), -- Alex applies for Job 2
(3, 5, 670, 'submitted'),
(4, 7, 1900, 'rejected'),
(5, 9, 280, 'submitted'),
(6, 1, 1500, 'submitted'), -- Aditya applies for Job 6
(7, 3, 500, 'submitted'),  -- Alex applies for Job 7
(8, 5, 670, 'accepted'),
(9, 7, 1200, 'submitted'),
(10, 9, 450, 'submitted'),
(11, 1, 600, 'submitted'), -- Aditya applies for Job 11
(12, 3, 400, 'submitted'), -- Alex applies for Job 12
(13, 5, 1200, 'submitted'),
(14, 7, 800, 'rejected'),
(15, 9, 600, 'accepted'),
(16, 1, 950, 'submitted'), -- Aditya applies for Job 16
(17, 3, 870, 'accepted'),  -- Alex applies for Job 17
(18, 5, 700, 'submitted'),
(19, 7, 400, 'submitted'),
(20, 9, 300, 'submitted');


-- Create table Client_Feedback
CREATE TABLE Client_Feedback (
    feedback_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL,
    client_id INT NOT NULL,
    freelancer_id INT NOT NULL,
    feedback TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id),
    FOREIGN KEY (client_id) REFERENCES Users(user_id),
    FOREIGN KEY (freelancer_id) REFERENCES Users(user_id)
);

-- Sample data for Client_Feedback
INSERT INTO Client_Feedback (job_id, client_id, freelancer_id, feedback, rating) VALUES
(1, 5, 1, 'Excellent work on web design!', 5),
(2, 6, 3, 'Great job on the mobile app development.', 4),
(3, 8, 5, 'Good data science consultation.', 4),
(4, 10, 7, 'The graphic design was top-notch.', 5),
(10, 20, 9, 'Delivered backend API development as requested.', 4),
(11, 5, 11, 'Content writing was satisfactory.', 3),
(13, 15, 13, 'Good job on database management.', 4),
(17, 15, 15, 'Digital marketing campaign was effective.', 5);

-- Create table Freelancer_Performance
CREATE TABLE Freelancer_Performance (
    performance_id SERIAL PRIMARY KEY,
    freelancer_id INT NOT NULL,
    job_id INT NOT NULL,
    performance_rating INT CHECK (performance_rating >= 1 AND performance_rating <= 5),
    FOREIGN KEY (freelancer_id) REFERENCES Users(user_id),
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id)
);

-- Sample data for Freelancer_Performance
INSERT INTO Freelancer_Performance (freelancer_id, job_id, performance_rating) VALUES
(1, 1, 5),
(3, 2, 4),
(5, 3, 4),
(7, 4, 5),
(9, 10, 4),
(11, 11, 3),
(13, 13, 4),
(15, 17, 5);


