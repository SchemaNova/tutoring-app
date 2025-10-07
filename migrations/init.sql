CREATE DATABASE IF NOT EXISTS tutoring_platform;
USE tutoring_platform;

CREATE TABLE COURSE (
    course_id VARCHAR(50) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(20)
);

CREATE TABLE STUDENT (
    student_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE TUTOR (
    tutor_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100)
);

CREATE TABLE LESSON (
    lesson_id VARCHAR(50) PRIMARY KEY,
    lesson_date DATETIME NOT NULL,
    duration_minutes INT NOT NULL CHECK (duration_minutes > 0),
    student_id VARCHAR(50) NOT NULL,
    tutor_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES TUTOR(tutor_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_lesson_time (tutor_id, lesson_date) -- Prevents overlapping lessons for tutors
);

CREATE TABLE PAYMENT (
    payment_id VARCHAR(50) PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    payment_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    lesson_id VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (lesson_id) REFERENCES LESSON(lesson_id) ON DELETE CASCADE
);

CREATE TABLE REVIEW (
    review_id VARCHAR(50) PRIMARY KEY,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date DATETIME NOT NULL,
    lesson_id VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (lesson_id) REFERENCES LESSON(lesson_id) ON DELETE CASCADE
);
