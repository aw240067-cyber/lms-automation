import hashlib
import random
import os
from faker import Faker
from pymongo import MongoClient

fake = Faker()

CONNECTION_STRING = os.getenv("MONGO_URI")

def hash_name(name_string):
    return hashlib.sha256(name_string.encode('utf-8')).hexdigest()

try:
    client = MongoClient(CONNECTION_STRING)
    db = client["LMS_Database"]

    print("Successfully connected to MongoDB Atlas!")

    db.students.delete_many({})
    db.courses.delete_many({})
    db.enrollments.delete_many({})

    print("Old records deleted.")

    # COURSES
    print("Generating 1000 courses...")
    course_ids = []
    courses_bulk = []

    faculties = ["FSKTM", "FKEE", "FKM", "FAST", "FPTP"]
    course_topics = [
        "Data Science",
        "Cloud Architecture",
        "Cybersecurity",
        "Network Systems",
        "AI Engineering"
    ]

    for i in range(1, 1001):
        c_id = f"CRS{1000+i}"
        course_ids.append(c_id)

        courses_bulk.append({
            "course_id": c_id,
            "course_name": f"Advanced {random.choice(course_topics)} - Level {random.choice([1,2,3])}",
            "faculty": random.choice(faculties),
            "credits": random.choice([2,3,4])
        })

    db.courses.insert_many(courses_bulk)

    # STUDENTS
    print("Generating 1000 students...")
    student_ids = []
    students_bulk = []

    majors = [
        "Data Analytics",
        "Software Engineering",
        "Multimedia",
        "Information Security"
    ]

    for i in range(1, 1001):
        s_id = f"STU{1000+i}"
        student_ids.append(s_id)

        raw_name = f"{fake.first_name()} {fake.last_name()}"
        masked_name = hash_name(raw_name)

        students_bulk.append({
            "student_id": s_id,
            "name": masked_name,
            "email": f"student{s_id.lower()}@siswa.uthm.edu.my",
            "major": random.choice(majors),
            "enrollment_year": random.choice([2023,2024,2025,2026])
        })

    db.students.insert_many(students_bulk)

    # ENROLLMENTS
    print("Generating 1200 enrollments...")
    enrollments_bulk = []

    for i in range(1, 1201):
        enrollments_bulk.append({
            "enrollment_id": f"ENR{10000+i}",
            "student_id": random.choice(student_ids),
            "course_id": random.choice(course_ids),
            "progress_percentage": random.randint(0,100),
            "last_login_date": fake.date_between(
                start_date='-60d',
                end_date='today'
            ).strftime('%Y-%m-%d'),
            "status": random.choice([
                "Active",
                "Completed",
                "Dropped"
            ])
        })

    db.enrollments.insert_many(enrollments_bulk)

    print("SUCCESS: 3200 records generated.")

except Exception as e:
    print(f"ERROR: {e}")
