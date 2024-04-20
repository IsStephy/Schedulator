import json
import networkx as nx
import matplotlib.pyplot as plt
from classes import Teacher, Course, Group, Offices
from models import db, User


def load_data_from_json(user_id):
    user = db.query.get(user_id)
    data = json.load(user.schedule_data)
    teachers, courses, groups, offices = [], [], [], []
    for entry in data:
        if entry['type'] == 'Teacher':
            teacher_data = entry['data']
            teachers.append(
                Teacher(teacher_data['name'], [(course[0], course[1]) for course in teacher_data['courses']],
                        teacher_data['language']))
        elif entry['type'] == 'Course':
            course_data = entry['data']
            courses.append(Course(course_data['name'], course_data['course_type']))
        elif entry['type'] == 'Group':
            group_data = entry['data']
            groups.append(Group(group_data['name'],
                                [(course[0], course[1], course[2]) for course in group_data['courses'] if
                                 len(course) == 3], group_data['language']))
        elif entry['type'] == 'Office':
            office_data = entry['data']
            offices.append(Offices(office_data['name'], office_data['office_type']))
    return teachers, courses, groups, offices


def create_list_of_tuples(teachers, courses, groups, offices):
    result = []
    teacher_course_lang = {}
    for teacher in teachers:
        for course_name, course_type in teacher.courses:
            teacher_course_lang.setdefault((course_name, course_type, teacher.language), []).append(teacher)
    office_course_type = {}
    for office in offices:
        office_course_type.setdefault(office.office_type, []).append(office)

    teacher_total_assignments = {teacher.name: 0 for teacher in teachers}
    office_total_assignments = {office.name: 0 for office in offices}

    teacher_office_group_assignments = {}
    group_course_teacher_office = {}
    for group in groups:
        group_prefix = ''.join(filter(str.isalpha, group.name))
        for course_name, course_type, frequency in group.courses:
            eligible_teachers = teacher_course_lang.get((course_name, course_type, group.language), [])
            eligible_offices = office_course_type.get(course_type, [])
            if not eligible_teachers or not eligible_offices:
                continue

            assignment_key = (group_prefix, course_name, course_type, group.language)
            if course_type == "Curs" and assignment_key in group_course_teacher_office:
                assigned_teacher, assigned_office = group_course_teacher_office[assignment_key]
            else:
                assigned_teacher = min(eligible_teachers, key=lambda teacher: teacher_total_assignments[teacher.name])
                teacher_total_assignments[assigned_teacher.name] += 1
                assigned_office = min(eligible_offices, key=lambda office: office_total_assignments[office.name])
                office_total_assignments[assigned_office.name] += 1
                if course_type == "Curs":
                    group_course_teacher_office[assignment_key] = (assigned_teacher, assigned_office)
            teacher_office_group_assignments[assignment_key] = (assigned_teacher, assigned_office)
            if course_name != "Ed. Fiz":
                for _ in range(int(frequency)):
                    result.append((group.name, course_name, course_type, assigned_teacher.name, assigned_office.name,
                                   frequency, group.language))
            else:
                result.append((group.name, course_name, " ", assigned_teacher.name, "Sala Sp.", " ", group.language))

    return result


def are_conflicting(class1, class2):
    if (class1[1] == class2[1] and class1[2] == "Curs" and class2[2] == "Curs" and
            class1[3] == class2[3] and class1[4] == class2[4] and class1[6] == class2[6]):
        return False
    if (class1[1] == class2[1] and class1[1] == "Ed. Fiz" and class1[6] != class2[6]):
        return False
    return class1[3] == class2[3] or class1[4] == class2[4] or class1[0] == class2[0]


def custom_coloring(G, num_slots_per_day):
    colors = {node: -1 for node in G.nodes()}
    sorted_nodes = sorted(G.nodes(), key=lambda x: (x[0], x[2]))
    for node in sorted_nodes:
        group = node[0]
        available_colors = set(range(num_slots_per_day))
        for neighbor in G.neighbors(node):
            if colors[neighbor] != -1:
                available_colors.discard(colors[neighbor])
        last_color = max([colors[n] for n in sorted_nodes if n[0] == group and colors[n] != -1], default=-1)
        next_color = last_color + 1 if last_color + 1 in available_colors else None
        if next_color is None:
            next_color = min(available_colors, default=None)
        if next_color is not None:
            colors[node] = next_color
    return colors


def create_graph_and_apply_coloring(user_id, num_slots_per_day):
    teachers, courses, groups, offices = load_data_from_json(user_id)
    tuples_list = create_list_of_tuples(teachers, courses, groups, offices)
    G = nx.Graph()
    for class1 in tuples_list:
        for class2 in tuples_list:
            if class1 != class2 and are_conflicting(class1, class2):
                G.add_edge(class1, class2)
    colors = custom_coloring(G, num_slots_per_day)
    return G, colors