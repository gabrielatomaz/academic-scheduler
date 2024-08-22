import json
import time

dataset = {
    "Courses": [
        {"Course": f"100{i}", "RoomsRequested": {"Type": "Small" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Large"}, "Teacher": f"T{i}"}
        for i in range(1, 380)
    ],
    "Periods": 20,
    "Rooms": [
        {"Room": f"R{i}", "Type": "Small" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Large"}
        for i in range(1, 21)
    ],
    "Teachers": [f"T{i}" for i in range(1, 380)]
}

def is_valid_assignment(schedule, course, room, period):
    if course["RoomsRequested"]["Type"] != room["Type"]:
        return False
    for assigned_course, assigned_room, assigned_period in schedule:
        if assigned_period == period and assigned_room["Room"] == room["Room"]:
            return False
    
    return True

def backtracking_scheduler(courses, rooms, periods, schedule=[], depth=0, counter={"attempts": 0}):
    if len(schedule) == len(courses):
        return schedule
    
    course = courses[len(schedule)]

    for period in range(periods):
        for room in rooms:
            if is_valid_assignment(schedule, course, room, period):                
                counter["attempts"] += 1
                
                schedule.append((course, room, period))
                
                result = backtracking_scheduler(courses, rooms, periods, schedule, depth+1, counter)
                if result:
                    return result
                
                schedule.pop()
    return None

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

start_time = time.time()

exact_schedule = backtracking_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
exact_schedule_json = schedule_to_json(exact_schedule) if exact_schedule else {"Assignments": []}

elapsed_time = time.time() - start_time

filename = f"exact_schedule_{elapsed_time:.2f}_seconds.json"
with open(filename, "w") as json_file:
    json.dump(exact_schedule_json, json_file, indent=2)

print(f"Arquivo salvo em {filename}. Tempo de execução: {elapsed_time:.2f} (s)")

#approximate_schedule = greedy_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
#approximate_schedule_json = schedule_to_json(approximate_schedule)

#print("Aproximativo:", json.dumps(approximate_schedule_json, indent=2))