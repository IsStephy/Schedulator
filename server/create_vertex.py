import json
import networkx as nx
import matplotlib.pyplot as plt
from classes import Teacher, Course, Group, Offices
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    teachers, courses, groups, offices = [], [], [], []
    for entry in data:
        if entry['type'] == 'Teacher':
            teacher_data = entry['data']
            teachers.append(Teacher(teacher_data['name'], [(course[0], course[1]) for course in teacher_data['courses']], teacher_data['language']))
        elif entry['type'] == 'Course':
            course_data = entry['data']
            courses.append(Course(course_data['name'], course_data['course_type']))
        elif entry['type'] == 'Group':
            group_data = entry['data']
            groups.append(Group(group_data['name'], [(course[0], course[1], course[2]) for course in group_data['courses'] if len(course) == 3], group_data['language']))
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
    group_course_assignments = {}
    group_office_assignments = {}
    teacher_office_group_assignments = {}
    for group in groups:
        group_prefix = ''.join(filter(str.isalpha, group.name))
        for course_name, course_type, frequency in group.courses:
            eligible_teachers = teacher_course_lang.get((course_name, course_type, group.language), [])
            eligible_offices = office_course_type.get(course_type, [])
            if not eligible_teachers or not eligible_offices:
                continue
            assignment_key = (group_prefix, course_name, course_type, group.language)
            if assignment_key in teacher_office_group_assignments:
                assigned_teacher, assigned_office = teacher_office_group_assignments[assignment_key]
            else:
                teacher_index = group_course_assignments.get(assignment_key, 0)
                office_index = group_office_assignments.get(course_type, 0)
                assigned_teacher = eligible_teachers[teacher_index % len(eligible_teachers)]
                assigned_office = eligible_offices[office_index % len(eligible_offices)]
                teacher_office_group_assignments[assignment_key] = (assigned_teacher, assigned_office)
                group_course_assignments[assignment_key] = teacher_index + 1
                group_office_assignments[course_type] = office_index + 1
            result.append((group.name, course_name, course_type, assigned_teacher.name, assigned_office.name, frequency, group.language))
    return result

def are_conflicting(class1, class2):
    if (class1[1] == class2[1] and class1[2] == "Curs" and class2[2] == "Curs" and
            class1[3] == class2[3] and class1[4] == class2[4] and class1[6] == class2[6]):
        return False
    return class1[3] == class2[3] or class1[4] == class2[4] or class1[0] == class2[0]
def greedy_coloring(G):
    colors = {node: -1 for node in G.nodes()}
    available = [False] * G.number_of_nodes()
    nodes = list(G.nodes())
    colors[nodes[0]] = 0
    for node in nodes[1:]:
        available = [True] * len(colors)
        for neighbor in G.neighbors(node):
            if colors[neighbor] != -1:
                available[colors[neighbor]] = False
        clr = 0
        while clr < len(available):
            if available[clr]:
                break
            clr += 1
        colors[node] = clr
    return colors
def create_graph_and_apply_coloring(json_file):
    teachers, courses, groups, offices = load_data_from_json(json_file)
    tuples_list = create_list_of_tuples(teachers, courses, groups, offices)
    G = nx.Graph()
    for class1 in tuples_list:
        for class2 in tuples_list:
            if class1 != class2 and are_conflicting(class1, class2):
                G.add_edge(class1, class2)
    colors = greedy_coloring(G)
    return G, colors
if __name__ == "__main__":
    json_file = "file_1.json"
    teachers, courses, groups, offices = load_data_from_json(json_file)
    tuples_list = create_list_of_tuples(teachers, courses, groups, offices)
    for tuples in tuples_list:
        print(tuples)
    graph = {class_session: [] for class_session in tuples_list}
    G = nx.Graph()
    for class1 in tuples_list:
        for class2 in tuples_list:
            if class1 != class2 and are_conflicting(class1, class2):
                G.add_edge(class1, class2)
    colors = greedy_coloring(G)
    plt.figure(figsize=(300, 160))
    pos = nx.spring_layout(G, seed=100)
    color_map = [colors[node] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, labels={node: f"{node[1][:3]}.. ({node[0]})" for node in G.nodes()}, node_size=1000, node_color=color_map, font_size=5, edge_color="gray", cmap=plt.cm.Paired)
    plt.title("Graphical Representation of Class Sessions and Conflicts with Coloring")
    plt.show()