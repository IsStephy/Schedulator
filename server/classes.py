class Teacher:
    def __init__(self, name, courses, language):
        self.name = name
        self.courses = courses  
        self.language = language 

    def __str__(self):
        courses_info = "\n".join(f"{course[0]} ({course[1]})" for course in self.courses)
        return f"Teacher Name: {self.name}\nCourses:\n{courses_info}"


class Course:
    def __init__(self, name, course_type):
        self.name = name
        self.course_type = course_type

    def __str__(self):
        return f"Course Name: {self.name}\nCourse Type: {self.course_type}"


class Group:
    def __init__(self, name, courses, language):
        self.name = name
        self.courses = courses
        self.language = language

    def __str__(self):
        course_info = "\n".join(f"{course[0]} ({course[1]}): {course[2]} times/week" for course in self.courses)
        return f"Group Name: {self.name}\nCourses:\n{course_info}"

class Offices:
    def __init__(self, name, office_type):
        self.name = name
        self.office_type = office_type

    def __str__(self):
        return f"Office Name: {self.name}\nOffice Type: {self.office_type}"
