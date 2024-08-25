import json
import time
import argparse
import os

def generate_dataset(periods, rooms, unscheduled_courses_count):
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

    return dataset

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
    room_types = ["Small", "Medium", "Large"]  # Definir room_types dentro da função
    schedule = []
    unscheduled = []

    available_rooms = {room_type: [] for room_type in room_types}
    for room in rooms:
        available_rooms[room["Type"]].append(room)

    room_availability = {period: {room_type: [] for room_type in room_types} for period in range(periods)}
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

def main():
    parser = argparse.ArgumentParser(description="Course scheduling with given number of rooms.")
    parser.add_argument('rooms', type=int, default=10, help='Number of rooms')
    parser.add_argument('--periods', type=int, default=20, help='Number of periods (default: 20)')
    parser.add_argument('--unscheduled_courses_count', type=int, default=10, help='Number of unscheduled courses (default: 10)')
    parser.add_argument('--output_dir', type=str, default='output', help='Directory to save the output files (default: output)')

    args = parser.parse_args()
    
    rooms = args.rooms
    periods = args.periods
    unscheduled_courses_count = args.unscheduled_courses_count
    output_dir = args.output_dir

    # Garantir que o diretório de saída exista
    os.makedirs(output_dir, exist_ok=True)

    dataset = generate_dataset(rooms, periods, unscheduled_courses_count)

    start_time = time.time()

    exact_schedule, unscheduled_courses = iterative_backtracking_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
    exact_schedule_json = schedule_to_json(exact_schedule, unscheduled_courses)

    elapsed_time = time.time() - start_time

    filename = os.path.join(output_dir, f"exact_schedule_{rooms}_{periods}_{unscheduled_courses_count}_{elapsed_time:.2f}_seconds.json")
    with open(filename, "w") as json_file:
        json.dump(exact_schedule_json, json_file, indent=2)

    print(f"Arquivo exato salvo em {filename}. Tempo de execução: {elapsed_time:.2f} (s)")

    start_time = time.time()

    approximate_schedule, unscheduled_courses_approx = greedy_approximate_scheduler(dataset["Courses"], dataset["Rooms"], dataset["Periods"])
    approximate_schedule_json = schedule_to_json(approximate_schedule, unscheduled_courses_approx)

    elapsed_time = time.time() - start_time
    approximate_filename = os.path.join(output_dir, f"approximate_schedule_{rooms}_{periods}_{unscheduled_courses_count}_{elapsed_time:.2f}_seconds.json")
    with open(approximate_filename, "w") as json_file:
        json.dump(approximate_schedule_json, json_file, indent=2)

    print(f"Arquivo aproximado salvo em {approximate_filename}. Tempo de execução: {elapsed_time:.2f} (s)")

if __name__ == "__main__":
    main()