import json
from classes import Teacher, Group, Offices
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    teachers, groups, offices = [], [], []
    for entry in data:
        if entry['type'] == 'Teacher':
            teacher_data = entry['data']
            teachers.append(Teacher(teacher_data['name'], [(course[0], course[1]) for course in teacher_data['courses']], teacher_data['language']))
        elif entry['type'] == 'Group':
            group_data = entry['data']
            groups.append(Group(group_data['name'], [(course[0], course[1], course[2]) for course in group_data['courses'] if len(course) == 3], group_data['language']))
        elif entry['type'] == 'Office':
            office_data = entry['data']
            offices.append(Offices(office_data['name'], office_data['office_type']))
    return teachers, groups, offices

def Teach(teachers):
    n = 0;
    teach_list = []
    for teacher in teachers:
        n += 1
        teach_list.append(teacher)
    return n, teach_list

def Grup(groups):
    group_list = []
    n = 0
    for group in groups:
        n += 1
        group_list.append(group)
    return n,group_list

def Office(offices):
    office_list = []
    n = 0
    for office in offices:
        n += 1
        office_list.append(office)
    return n,office_list

  

if __name__ == "__main__":
    json_file = "file_1.json"
    file_path = "function.txt"
    teachers, groups, offices = load_data_from_json(json_file)
    number_of_teacher,teacher_list = Teach(teachers)
    number_of_groups, group_list = Grup(groups)
    number_of_offices, office_list = Office(offices)
    with open(file_path, 'w') as file:
        for i in range(number_of_teacher):
            file.write(f"\n{i+1}) {teacher_list[i]}")
        file.write("\n\n\n")
        for i in range(number_of_groups):
            file.write(f"\n{i+1}) {group_list[i]} \n")
        file.write("\n\n\n")
        for i in range(number_of_offices):
            file.write(f"\n{i+1}) {office_list[i]}")