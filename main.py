import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os


HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", 3306))
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASS", "")
DATABASE = os.getenv("DB_NAME", "tutoring_platform")


# defining a function that will get all the required endpoints make a connection
def get_connection():
    return mysql.connector.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE
    )


def run_migrations():
    conn = None
    try:
        # First connect without database to create it if needed
        conn = mysql.connector.connect(
            host=HOST, port=PORT, user=USER, password=PASSWORD
        )
        cur = conn.cursor()
        
        # Read and execute init.sql
        with open('migrations/init.sql', 'r') as f:
            # Split by semicolon to execute multiple statements
            statements = f.read().split(';')
            for statement in statements:
                if statement.strip():
                    cur.execute(statement)
        conn.commit()
        
        # Read and execute insert.sql
        with open('migrations/insert.sql', 'r') as f:
            # Split by semicolon to execute multiple statements
            statements = f.read().split(';')
            for statement in statements:
                if statement.strip():
                    cur.execute(statement)
        conn.commit()
        print("Migrations completed successfully")
    except Error as e:
        print("Error running migrations:", e)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


# defining a function that will get all the attributes from the Course table
def fetch_courses():
    conn = None
    try:
        conn = (
            get_connection()
        )  # setting up the connection by calling the get_connection defined above
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM COURSE;")
        return cur.fetchall()  # using fetchall to get all the information recieved by the SQL query and not fragments
    except Error as e:  # error handling
        print("Error fetching courses:", e)
        return []
    finally:
        if conn:
            conn.close()  # closing the connection afterwards


# defining a function that will get fetch all lessons for a specific tutor
def get_tutor_lessons(tutor_id):
    conn = None
    sql = """
    SELECT l.lesson_id, l.lesson_date, l.duration_minutes,
           s.first_name AS student_first, s.last_name AS student_last,
           c.course_name
    FROM LESSON l
    JOIN STUDENT s ON l.student_id = s.student_id
    JOIN COURSE c ON l.course_id = c.course_id
    WHERE l.tutor_id = %s
    ORDER BY l.lesson_date;
    """
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (tutor_id,))
        return cur.fetchall()
    except Error as e:  # error handling
        print("Error fetching tutor lessons:", e)
        return []
    finally:
        if conn:
            conn.close()


# defining a main function that will call all our other functions to deliver a connection as well as SQL queries
def main():
    print(f"\nConnecting to {USER}@{HOST}:{PORT} - DB: {DATABASE}\n")
    
    # Run migrations first
    run_migrations()

    # Fetch and print courses
    courses = fetch_courses()
    print("Courses:")
    if courses:
        for c in courses:
            print(
                f" - {c['course_id']}: {c['course_name']} ({c.get('difficulty_level')})"
            )
    else:
        print(" No courses found.")

    # Fetch and print lessons for tutor T001
    print("\nLessons for tutor T001:")
    lessons = get_tutor_lessons("T001")
    if lessons:
        for l in lessons:
            dt = l["lesson_date"]
            dt_str = (
                dt.strftime("%Y-%m-%d %H:%M") if isinstance(dt, datetime) else str(dt)
            )
            print(
                f" - {l['lesson_id']} on {dt_str} ({l['duration_minutes']} min) | {l['course_name']} - {l['student_first']} {l['student_last']}"
            )
    else:
        print(" No lessons found for T001.")


if __name__ == "__main__":
    main()
