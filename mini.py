import json

class Student:
    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks  # dict of subject: marks
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        avg = sum(self.marks.values()) / len(self.marks)
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "marks": self.marks,
            "grade": self.grade
        }

class ReportCardSystem:
    def __init__(self, db_file='students.json'):
        self.db_file = db_file
        self.students = self.load_data()

    def load_data(self):
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, roll_no, name, marks):
        if not isinstance(roll_no, int) or not name or not isinstance(marks, dict):
            print("Invalid entry. Please check the details.")
            return
        if roll_no in self.students:
            print("Roll number already exists.")
            return
        if not all(isinstance(m, (int, float)) and 0 <= m <= 100 for m in marks.values()):
            print("Invalid marks. Must be between 0 and 100.")
            return
        student = Student(roll_no, name, marks)
        self.students[roll_no] = student.to_dict()
        self.save_data()
        print("Student added successfully.")

    def fetch_student(self, roll_no):
        student = self.students.get(roll_no)
        if not student:
            print("Student not found.")
            return
        print(f"Roll No: {student['roll_no']}")
        print(f"Name: {student['name']}")
        print("Marks:")
        for subject, mark in student['marks'].items():
            print(f"  {subject}: {mark}")
        print(f"Grade: {student['grade']}")

if __name__ == "__main__":
    system = ReportCardSystem()
    while True:
        print("\n1. Add Student\n2. Fetch Student\n3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            try:
                roll_no = int(input("Enter roll number: "))
                name = input("Enter name: ")
                marks = {}
                subjects = input("Enter subjects separated by comma: ").split(',')
                for subject in subjects:
                    subject = subject.strip()
                    mark = float(input(f"Enter marks for {subject}: "))
                    marks[subject] = mark
                system.add_student(roll_no, name, marks)
            except Exception as e:
                print("Error:", e)
        elif choice == '2':
            try:
                roll_no = int(input("Enter roll number to fetch: "))
                system.fetch_student(roll_no)
            except Exception as e:
                print("Error:", e)
        elif choice == '3':
            break
        else:
            print("Invalid choice.")