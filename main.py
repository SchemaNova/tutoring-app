##SchemaNova
##4202375
##4203232
##4253243
##4384756
##4383832
##main.py

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
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
        with open("migrations/init.sql", "r") as f:
            # Split by semicolon to execute multiple statements
            statements = f.read().split(";")
            for statement in statements:
                if statement.strip():
                    cur.execute(statement)
        conn.commit()

        # Read and execute insert.sql
        with open("migrations/insert.sql", "r") as f:
            # Split by semicolon to execute multiple statements
            statements = f.read().split(";")
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


def _format_value(col, val):
    # Format common types: datetime and Decimal
    if val is None:
        return "NULL"
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M")
    if isinstance(val, Decimal):
        # Heuristics based on column name
        name = col.lower()
        if "avg" in name or "rating" in name:
            return f"{val:.4f}"
        if "amount" in name or "payment" in name or "revenue" in name or "total" in name:
            return f"{val:.2f}"
        return format(val, 'f')
    return str(val)


def _print_table(title, rows):
    print(f"\n--- {title} ---")
    if not rows:
        print("No records found.")
        return
    # determine columns from first row (preserve order)
    cols = list(rows[0].keys())
    # compute column widths
    col_widths = {c: max(len(c), *(len(_format_value(c, r.get(c))) for r in rows)) for c in cols}
    # header
    header = " | ".join(c.ljust(col_widths[c]) for c in cols)
    sep = "-+-".join("-" * col_widths[c] for c in cols)
    print(header)
    print(sep)
    # rows
    for r in rows:
        line = " | ".join(_format_value(c, r.get(c)).ljust(col_widths[c]) for c in cols)
        print(line)


def run_all_queries():
    """Executes all SQL queries from Section 6.0 and prints formatted results."""
    queries = [
        # Query 1
        ("All Registered Students",
         "SELECT student_id, first_name, last_name, email FROM student;"),
        # Query 2
        ("Available Courses",
         "SELECT course_id, course_name, difficulty_level FROM course ORDER BY difficulty_level;"),
        # Query 3
        ("Lessons for Tutor T001",
         "SELECT lesson_id, lesson_date, duration_minutes, course_id FROM lesson WHERE tutor_id = 'T001' ORDER BY lesson_date;"),
        # Query 4
        ("Payments and Lesson Details",
         """SELECT P.payment_id, P.amount, P.status, S.first_name AS Student,
                   T.first_name AS Tutor, L.lesson_date
            FROM payment P
            JOIN lesson L ON P.lesson_id = L.lesson_id
            JOIN student S ON L.student_id = S.student_id
            JOIN tutor T ON L.tutor_id = T.tutor_id
            ORDER BY P.payment_date DESC;"""),
        # Query 5
        ("All Reviews",
         """SELECT R.review_id, S.first_name AS Student, T.first_name AS Tutor,
                   R.rating, R.comment, R.review_date
            FROM review R
            JOIN lesson L ON R.lesson_id = L.lesson_id
            JOIN student S ON L.student_id = S.student_id
            JOIN tutor T ON L.tutor_id = T.tutor_id
            ORDER BY R.review_date DESC;"""),
        # Query 6
        ("Lessons Per Tutor",
         """SELECT T.tutor_id, T.first_name, T.last_name, COUNT(L.lesson_id) AS total_lessons
            FROM tutor T
            LEFT JOIN lesson L ON T.tutor_id = L.tutor_id
            GROUP BY T.tutor_id, T.first_name, T.last_name
            ORDER BY total_lessons DESC;"""),
        # Query 7
        ("Average Payment per Course",
         """SELECT C.course_name, AVG(P.amount) AS average_payment
            FROM course C
            JOIN lesson L ON C.course_id = L.course_id
            JOIN payment P ON L.lesson_id = P.lesson_id
            GROUP BY C.course_name
            ORDER BY average_payment DESC;"""),
        # Query 8
        ("Tutors with Rating > 4.0",
         """SELECT T.tutor_id, T.first_name, T.last_name, AVG(R.rating) AS avg_rating
            FROM tutor T
            JOIN lesson L ON T.tutor_id = L.tutor_id
            JOIN review R ON L.lesson_id = R.lesson_id
            GROUP BY T.tutor_id, T.first_name, T.last_name
            HAVING avg_rating > 4.0;"""),
        # Query 9
        ("Students Taking Multiple Courses",
         """SELECT S.student_id, S.first_name, S.last_name, COUNT(DISTINCT L.course_id) AS course_count
            FROM student S
            JOIN lesson L ON S.student_id = L.student_id
            GROUP BY S.student_id, S.first_name, S.last_name
            HAVING course_count > 1;"""),
        # Query 10
        ("Total Revenue per Tutor",
         """SELECT T.tutor_id, T.first_name, T.last_name, SUM(P.amount) AS total_revenue
            FROM tutor T
            JOIN lesson L ON T.tutor_id = L.tutor_id
            JOIN payment P ON L.lesson_id = P.lesson_id
            GROUP BY T.tutor_id, T.first_name, T.last_name
            ORDER BY total_revenue DESC;""")
    ]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    print("\nExecuting SQL queries...\n")

    for title, sql in queries:
        cur.execute(sql)
        rows = cur.fetchall()
        _print_table(title, rows)

    cur.close()
    conn.close()
    print("\nAll queries executed successfully.\n")


#Main execution
def main():
    print(f"\nConnecting to {USER}@{HOST}:{PORT} - DB: {DATABASE}\n")

    # Step 1: Run migrations (create + insert)
    run_migrations()

    # Step 2: Execute all SQL queries from section 6.0
    run_all_queries()


if __name__ == "__main__":
    main()
