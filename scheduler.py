import json

dataset = {
    "Courses": [
        {"Course": f"100{i}", "RoomsRequested": {"Type": "Small" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Large"}, "Teacher": f"T{i}"}
        for i in range(1, 400)
    ],
    "Periods": 20,
    "Rooms": [
        {"Room": f"R{i}", "Type": "Small" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Large"}
        for i in range(1, 21)
    ],
    "Teachers": [f"T{i}" for i in range(1, 400)]
}

def is_valid_assignment(schedule, course, room, period):
    if course["RoomsRequested"]["Type"] != room["Type"]:
        return False
    for assigned_course, assigned_room, assigned_period in schedule:
        if assigned_period == period and assigned_room["Room"] == room["Room"]:
            print(f"Invalid Assignment: Room {room['Room']} is already occupied at period {period}.")
            return False
    
    return True

def backtracking_scheduler(courses, rooms, periods, schedule=[], depth=0, counter={"attempts": 0}):
    if len(schedule) == len(courses):
        print("Valid schedule found:", schedule)
        print(f"Total attempts: {counter['attempts']}")
        return schedule
    
    course = courses[len(schedule)]

    for period in range(periods):
        for room in rooms:
            if is_valid_assignment(schedule, course, room, period):
                print(f"Depth {depth}: Trying course {course} in room {room} at period {period}")
                
                counter["attempts"] += 1
                
                schedule.append((course, room, period))
                
                result = backtracking_scheduler(courses, rooms, periods, schedule, depth+1, counter)
                if result:
                    return result
                
                print(f"Depth {depth}: Backtracking from course {course} in room {room} at period {period}")
                schedule.pop()
    
    print(f"Depth {depth}: Dead end reached, no valid assignments for course {course}")
    print(f"Total attempts: {counter['attempts']}")
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
