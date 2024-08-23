import json
import time

periods = 20
rooms = 100
unscheduled_courses_count = 0
max_courses = periods * rooms

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
    for _ in range((room_count_by_type[room_type] * periods) + unscheduled_courses_count):
        course_list.append({
            "Course": f"100{course_id}",
            "RoomsRequested": {"Type": room_type},
            "Teacher": f"T{course_id}"
        })
        course_id += 1

dataset = {
    "Courses": course_list,
    "Periods": periods,
    "Rooms": room_list,
    "Teachers": [f"T{i+1}" for i in range(max_courses)]
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

def schedule_to_json(schedule, unscheduled):
    result = {"Assignments": []}
    for (course, room, period) in schedule:
        result["Assignments"].append({
            "Course": course["Course"],
            "Period": period,
            "Room": room["Room"],
            "RequestedRoomSize": course["RoomsRequested"]["Type"],
            "AssignedRoomSize": room["Type"],
            "Teacher": course["Teacher"]
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

start_time = time.time()

exact_schedule, unscheduled_courses = iterative_backtracking_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
exact_schedule_json = schedule_to_json(exact_schedule, unscheduled_courses)

elapsed_time = time.time() - start_time

filename = f"exact_schedule_{elapsed_time:.2f}_seconds.json"
with open(filename, "w") as json_file:
    json.dump(exact_schedule_json, json_file, indent=2)

print(f"Arquivo salvo em {filename}. Tempo de execução: {elapsed_time:.2f} (s)")
