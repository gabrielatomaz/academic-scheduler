import json

dataset = {
    "Courses": [
        {"Course": "1001", "RoomsRequested": {"Type": "Small"}, "Teacher": "T1"},
        {"Course": "1002", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T2"},
        {"Course": "1003", "RoomsRequested": {"Type": "Large"}, "Teacher": "T3"},
        {"Course": "1004", "RoomsRequested": {"Type": "Small"}, "Teacher": "T4"},
        {"Course": "1005", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T5"},
        {"Course": "1006", "RoomsRequested": {"Type": "Large"}, "Teacher": "T6"},
        {"Course": "1007", "RoomsRequested": {"Type": "Small"}, "Teacher": "T7"},
        {"Course": "1008", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T8"},
        {"Course": "1009", "RoomsRequested": {"Type": "Large"}, "Teacher": "T9"},
        {"Course": "1010", "RoomsRequested": {"Type": "Small"}, "Teacher": "T10"},
        {"Course": "1011", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T11"},
        {"Course": "1012", "RoomsRequested": {"Type": "Large"}, "Teacher": "T12"},
        {"Course": "1013", "RoomsRequested": {"Type": "Small"}, "Teacher": "T13"},
        {"Course": "1014", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T14"},
        {"Course": "1015", "RoomsRequested": {"Type": "Large"}, "Teacher": "T15"},
        {"Course": "1016", "RoomsRequested": {"Type": "Small"}, "Teacher": "T16"},
        {"Course": "1017", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T17"},
        {"Course": "1018", "RoomsRequested": {"Type": "Large"}, "Teacher": "T18"},
        {"Course": "1019", "RoomsRequested": {"Type": "Small"}, "Teacher": "T19"},
        {"Course": "1020", "RoomsRequested": {"Type": "Medium"}, "Teacher": "T20"}
    ],
    "Periods": 20,
    "Rooms": [
        {"Room": "R1", "Type": "Small"},
        {"Room": "R2", "Type": "Medium"},
        {"Room": "R3", "Type": "Large"},
        {"Room": "R4", "Type": "Small"},
        {"Room": "R5", "Type": "Medium"},
        {"Room": "R6", "Type": "Large"},
        {"Room": "R7", "Type": "Small"},
        {"Room": "R8", "Type": "Medium"},
        {"Room": "R9", "Type": "Large"},
        {"Room": "R10", "Type": "Small"}
    ],
    "Teachers": [
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
        "T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T20"
    ]
}

def is_valid_assignment(schedule, course, room, period):
    if course["RoomsRequested"]["Type"] != room["Type"]:
        return False
    for assigned_course, assigned_room, assigned_period in schedule:
        if assigned_period == period and assigned_room["Room"] == room["Room"]:
            print(f"Invalid Assignment: Room {room['Room']} is already occupied at period {period}.")
            return False
    
    return True

def backtracking_scheduler(courses, rooms, periods, schedule=[]):
    if len(schedule) == len(courses):
        return schedule
    
    course = courses[len(schedule)]
    
    for period in range(periods):
        for room in rooms:
            if is_valid_assignment(schedule, course, room, period):
                schedule.append((course, room, period))
                result = backtracking_scheduler(courses, rooms, periods, schedule)
                if result:
                    return result
                schedule.pop()
    
    return None

def greedy_scheduler(courses, rooms, periods):
    schedule = []
    course_assignments = {course["Course"]: False for course in courses}
    
    for period in range(periods):
        for room in rooms:
            available_courses = [course for course in courses if not course_assignments[course["Course"]]]
            for course in available_courses:
                if is_valid_assignment(schedule, course, room, period):
                    schedule.append((course, room, period))
                    course_assignments[course["Course"]] = True
                    break
            else:
                continue
            break
    return schedule

def schedule_to_json(schedule):
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
    return result

exact_schedule = backtracking_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
exact_schedule_json = schedule_to_json(exact_schedule) if exact_schedule else {"Assignments": []}

print("Exato:", json.dumps(exact_schedule_json, indent=2))

approximate_schedule = greedy_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
approximate_schedule_json = schedule_to_json(approximate_schedule)

print("Aproximativo:", json.dumps(approximate_schedule_json, indent=2))
