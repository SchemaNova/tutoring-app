INSERT INTO COURSE (course_id, course_name, description, difficulty_level) VALUES
('COS101', 'Introduction to Programming', 'Learn basic programming concepts', 'Beginner'),
('MAT211', 'Advanced Calculus', 'Deep dive into calculus topics', 'Advanced');

INSERT INTO STUDENT (student_id, first_name, last_name, email) VALUES
('S001', 'John', 'Doe', 'john.doe@email.com'),
('S002', 'Jane', 'Smith', 'jane.smith@email.com');

INSERT INTO TUTOR (tutor_id, first_name, last_name, specialization) VALUES
('T001', 'Dr. Alice', 'Johnson', 'Computer Science'),
('T002', 'Prof. Bob', 'Brown', 'Mathematics');

INSERT INTO LESSON (lesson_id, lesson_date, duration_minutes, student_id, tutor_id, course_id) VALUES
('L001', '2024-01-15 10:00:00', 60, 'S001', 'T001', 'COS101'),
('L002', '2024-01-16 14:00:00', 90, 'S002', 'T002', 'MAT211');

INSERT INTO PAYMENT (payment_id, amount, payment_date, status, lesson_id) VALUES
('P001', 50.00, '2024-01-14 09:00:00', 'completed', 'L001'),
('P002', 75.00, '2024-01-15 10:00:00', 'completed', 'L002');

INSERT INTO REVIEW (review_id, rating, comment, review_date, lesson_id) VALUES
('R001', 5, 'Excellent teaching style', '2024-01-15 12:00:00', 'L001'),
('R002', 4, 'Very knowledgeable tutor', '2024-01-16 16:00:00', 'L002');
