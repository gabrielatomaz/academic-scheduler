import json
import time

periods = 20
rooms = 10000
unscheduled_courses_count = 10

room_types = ["Small", "Medium", "Large"]

room_list = [
    {"Room": f"R{i+1}", "Type": room_types[i % len(room_types)]}
    for i in range(rooms)
]

room_count_by_type = {room_type: 0 for room_type in room_types}
for room in room_list:
    room_count_by_type[room["Type"]] += 1

course_list = []
course_id = 1

for room_type in room_types:
    for _ in range(room_count_by_type[room_type] * periods):
        course_list.append({
            "Course": f"100{course_id}",
            "RoomsRequested": {"Type": room_type},
            "Teacher": f"T{course_id}"
        })
        course_id += 1

for _ in range(unscheduled_courses_count):
    course_list.append({
        "Course": f"100{course_id}",
        "RoomsRequested": {"Type": "Medium"},  
        "Teacher": f"T{course_id}"
    })
    course_id += 1

dataset = {
    "Courses": course_list,
    "Periods": periods,
    "Rooms": room_list,
    "Teachers": [f"T{i+1}" for i in range(len(course_list))]
}

def is_valid_assignment(schedule, course, room, period):
    if course["RoomsRequested"]["Type"] != room["Type"]:
        return False
    for assigned_course, assigned_room, assigned_period in schedule:
        if assigned_period == period and assigned_room["Room"] == room["Room"]:
            return False
    return True

def iterative_backtracking_scheduler(courses, rooms, periods):
    schedule = []
    unscheduled = []
    course_index = 0  

    while course_index < len(courses):
        course = courses[course_index]
        found_valid_assignment = False

        for period in range(periods):
            for room in rooms:
                if is_valid_assignment(schedule, course, room, period):
                    schedule.append((course, room, period))
                    found_valid_assignment = True
                    break  
            if found_valid_assignment:
                break 

        if not found_valid_assignment:
            unscheduled.append(course)
        
        course_index += 1

    return schedule, unscheduled

def greedy_approximate_scheduler(courses, rooms, periods):
    schedule = []
    unscheduled = []

    available_rooms = {room_type: [] for room_type in room_types}
    for room in rooms:
        available_rooms[room["Type"]].append(room)

    room_availability = {period: {room["Type"]: [] for room in rooms} for period in range(periods)}
    for period in room_availability:
        for room in rooms:
            room_availability[period][room["Type"]].append(room)

    for course in courses:
        assigned = False
        room_type = course["RoomsRequested"]["Type"]
        
        for period in range(periods):
            if room_availability[period][room_type]:
                room = room_availability[period][room_type].pop(0)
                schedule.append((course, room, period))
                assigned = True
                break 

        if not assigned:
            unscheduled.append(course)

    return schedule, unscheduled

def schedule_to_json(schedule, unscheduled):
    result = {
        "Assignments": [],
        "TotalCoursesBooked": len(schedule),
        "TotalCoursesUnscheduled": len(unscheduled)
    }
    for (course, room, period) in schedule:
        result["Assignments"].append({
            "Course": course["Course"],
            "Period": period,
            "Room": room["Room"],
            "RequestedRoomSize": course["RoomsRequested"]["Type"],
            "AssignedRoomSize": room["Type"],
            "Teacher": course["Teacher"],
            "Status": "Booked"
        })
    
    for course in unscheduled:
        result["Assignments"].append({
            "Course": course["Course"],
            "Period": "N/A",
            "Room": "N/A",
            "RequestedRoomSize": course["RoomsRequested"]["Type"],
            "AssignedRoomSize": "N/A",
            "Teacher": course["Teacher"],
            "Status": "Not available room"
        })
    
    return result

print("Escolha o algoritmo para execução:")
print("1. Exato: Backtracking")
print("2. Algoritmo Aproximado: Greedy")

choice = input("Digite o número da sua escolha (1 ou 2): ")

if choice == "1":
    start_time = time.time()

    exact_schedule, unscheduled_courses = iterative_backtracking_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
    exact_schedule_json = schedule_to_json(exact_schedule, unscheduled_courses)

    elapsed_time = time.time() - start_time

    filename = f"exact_schedule_{elapsed_time:.2f}_seconds.json"
    with open(filename, "w") as json_file:
        json.dump(exact_schedule_json, json_file, indent=2)

    print(f"Arquivo exato salvo em {filename}. Tempo de execução: {elapsed_time:.2f} (s)")

elif choice == "2":
    start_time = time.time()

    approximate_schedule, unscheduled_courses_approx = greedy_approximate_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
    approximate_schedule_json = schedule_to_json(approximate_schedule, unscheduled_courses_approx)

    elapsed_time = time.time() - start_time
    approximate_filename = f"approximate_schedule_{elapsed_time:.2f}_seconds.json"
    with open(approximate_filename, "w") as json_file:
        json.dump(approximate_schedule_json, json_file, indent=2)

    print(f"Arquivo aproximado salvo em {approximate_filename}. Tempo de execução: {elapsed_time:.2f} (s)")

else:
    print("Escolha inválida. Por favor, execute o programa novamente e escolha 1 ou 2.")
