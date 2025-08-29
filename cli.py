from db import init_db, add_student, add_grade, get_student, list_students, calculate_student_average, subject_topper, class_average, backup_to_csv

def menu():
    print("\n=== Student Performance Tracker (CLI) ===")
    print("1. Add Student")
    print("2. Add/Update Grade")
    print("3. View Student Details")
    print("4. Calculate Student Average")
    print("5. List All Students")
    print("6. Subject-wise Topper (Bonus)")
    print("7. Class Average for Subject (Bonus)")
    print("8. Backup to CSV (Bonus)")
    print("9. Exit")

def main():
    init_db()
    while True:
        menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            name = input("Student Name: ").strip()
            roll = input("Roll Number: ").strip()
            if add_student(name, roll):
                print("✅ Student added.")
            else:
                print("❌ Roll already exists.")
        elif choice == "2":
            roll = input("Roll Number: ").strip()
            subject = input("Subject (e.g., Math, Science, English): ").strip()
            try:
                grade = float(input("Grade (0-100): ").strip())
            except ValueError:
                print("❌ Invalid grade.")
                continue
            ok, msg = add_grade(roll, subject, grade)
            print(("✅ " if ok else "❌ ") + msg)
        elif choice == "3":
            roll = input("Roll Number: ").strip()
            stu = get_student(roll)
            if not stu:
                print("❌ Student not found.")
            else:
                print(f"\nName: {stu['name']} | Roll: {stu['roll']}")
                if stu["grades"]:
                    for sub, gr in stu["grades"].items():
                        print(f" - {sub}: {gr}")
                else:
                    print("No grades yet.")
                print(f"Average: {stu['average']}")
        elif choice == "4":
            roll = input("Roll Number: ").strip()
            avg = calculate_student_average(roll)
            print(f"Average for {roll}: {avg}")
        elif choice == "5":
            students = list_students()
            if not students:
                print("No students yet.")
            for s in students:
                print(f"{s['roll']} - {s['name']}")
        elif choice == "6":
            subject = input("Subject: ").strip()
            top = subject_topper(subject)
            if top:
                print(f"Topper in {top['subject']}: {top['name']} ({top['roll']}) - {top['grade']}")
            else:
                print("No data for that subject.")
        elif choice == "7":
            subject = input("Subject: ").strip()
            avg = class_average(subject)
            print(f"Class average in {subject.title()}: {avg}")
        elif choice == "8":
            path = input("CSV path (e.g., backup.csv): ").strip() or "backup.csv"
            backup_to_csv(path)
            print(f"✅ Backup saved to {path}")
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
