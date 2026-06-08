import hashlib
import random
import os
from faker import Faker
from pymongo import MongoClient

fake = Faker()

# MongoDB connection (FROM GITHUB SECRET)
CONNECTION_STRING = os.getenv("MONGO_URI")

def hash_name(name_string):
    return hashlib.sha256(name_string.encode('utf-8')).hexdigest()

try:
    client = MongoClient(CONNECTION_STRING)
    db = client["LMS_Database"]

    print("Connected to MongoDB Atlas successfully!")

    # CLEAR OLD DATA
    db.students.delete_many({})
    db.courses.delete_many({})
    db.enrollments.delete_many({})

    print("Old data cleared.")

    # =========================
    # COURSES (1000)
    # =========================
    print("Generating courses...")

    course_ids = []
    courses_bulk = []

    faculties = ["FSKTM", "FKEE", "FKM", "FAST", "FPTP"]
    topics = ["Data Science", "Cloud Architecture", "Cybersecurity", "AI Engineering", "Networks"]

    for i in range(1, 1001):
        cid = f"CRS{1000+i}"
        course_ids.append(cid)

        courses_bulk.append({
            "course_id": cid,
            "course_name": f"Advanced {random.choice(topics)} Level {random.randint(1,3)}",
            "faculty": random.choice(faculties),
            "credits": random.choice([2,3,4])
        })

    db.courses.insert_many(courses_bulk)

    # =========================
    # STUDENTS (1000)
    # =========================
    print("Generating students...")

    student_ids = []
    students_bulk = []

    majors = ["Data Analytics", "Software Engineering", "Multimedia", "Security"]

    for i in range(1, 1001):
        sid = f"STU{1000+i}"
        student_ids.append(sid)

        raw_name = f"{fake.first_name()} {fake.last_name()}"
        masked_name = hash_name(raw_name)

        students_bulk.append({
            "student_id": sid,
            "name": masked_name,
            "email": f"{sid.lower()}@siswa.uthm.edu.my",
            "major": random.choice(majors),
            "year": random.choice([2023,2024,2025,2026])
        })

    db.students.insert_many(students_bulk)

    # =========================
    # ENROLLMENTS (1200)
    # =========================
    print("Generating enrollments...")

    enrollments_bulk = []

    for i in range(1, 1201):
        enrollments_bulk.append({
            "enrollment_id": f"ENR{10000+i}",
            "student_id": random.choice(student_ids),
            "course_id": random.choice(course_ids),
            "progress": random.randint(0,100),
            "status": random.choice(["Active","Completed","Dropped"]),
            "last_login": fake.date_between("-60d", "today").strftime("%Y-%m-%d")
        })

    db.enrollments.insert_many(enrollments_bulk)

    print("SUCCESS: 3200 records generated!")

except Exception as e:
    print(f"ERROR: {e}")
