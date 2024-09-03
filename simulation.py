import math
from arrival_times import generate_arrival_times
from constants import *
from elevator import Elevator
from strategies import (
    random_passenger_assignment,
    max_passenger_assignment,
    match_check_passenger_assignment,
    no_match_check_proximity_passenger_assignment,
    proximity_passenger_assignment,
)
from arrival_times import plot_times


def simulate(strategy, std_dev=std_dev):
    elevators = [Elevator(num_floors, max_capacity)
                 for _ in range(num_elevators)]

    lobby = [0] * num_floors
    completed_employees = [0] * num_floors
    employee_completion_times = []

    arrival_times = generate_arrival_times(
        employee_floor_distribution,
        mean_arrival_time,
        std_dev,
        start_time,
        end_time,
    )

    total_seconds = 3000

    for simulation_seconds in range(
        total_seconds
    ):
        if simulation_seconds == end_time:
            completed_by_9 = completed_employees.copy()

        # Check if empolyees arrived
        i = 0
        while i < len(arrival_times):
            floor, time = arrival_times[i]
            if time <= simulation_seconds:
                lobby[floor - 1] += 1
                arrival_times.pop(i)
            else:
                i += 1

        # Update time it takes for elevators to send their passengers to their floor and get back to the lobby
        for elevator in elevators:
            if math.floor(elevator.available_in) == 0:
                elevator.reset()
            else:
                elevator.available_in -= 1

            j = 0
            while j < len(elevator.passenger_complete_times):
                floor, amount, time = elevator.passenger_complete_times[j]
                if math.floor(time) == 0:
                    completed_employees[floor - 1] += amount
                    employee_completion_times += [(floor, simulation_seconds)] * amount
                    elevator.passenger_complete_times.pop(j)
                else:
                    elevator.passenger_complete_times[j][2] -= 1
                    j += 1

        # Apply the strategies and send people with available elevators
        if any(lobby):
            passengers = strategy(lobby, elevators)
            for k, elevator in enumerate(elevators):
                if any(passengers[k]):
                    if elevator.available_in != 0:
                        raise Exception(
                            f"gave elevator {
                                elevator} passengers but it is not avaialable"
                        )
                    elevator.pick_up_passengers(passengers[k])
        else:
            if not arrival_times:

                for elevator in elevators:
                    for floor, amount, time in elevator.passenger_complete_times:
                        employee_completion_times += [(floor, simulation_seconds + time)] * amount 
                return {
                    "time": simulation_seconds
                    + max([max([time for _, _, time in elevator.passenger_complete_times]) if len(
                        elevator.passenger_complete_times) != 0 else 0 for elevator in elevators]),
                    "num_completed_by_9": 500 if simulation_seconds < end_time else sum(completed_by_9),
                    "employee_completion_times": employee_completion_times
                }


def evaluate_strategy(strategy, iterations, std_dev=std_dev):
    times = []
    num_completed_by_9s = []
    employee_completion_times = []

    for _ in range(iterations):
        result = simulate(strategy, std_dev=std_dev)
        times.append(result["time"])
        num_completed_by_9s.append(result["num_completed_by_9"])
        employee_completion_times += result["employee_completion_times"]

    return {
        "times": times,
        "avg_time": sum(times) / iterations,
        "num_completed_by_9s": num_completed_by_9s,
        "avg_num_completed_by_9": sum(num_completed_by_9s) / iterations,
        "employee_completion_times": employee_completion_times
    }


def analyze_strategies_time_and_completion():
    strategies = [
        random_passenger_assignment,
        max_passenger_assignment,
        match_check_passenger_assignment,
        no_match_check_proximity_passenger_assignment,
        proximity_passenger_assignment,
    ]

    num_iterations = 1000

    print("# iterations:", num_iterations)

    for strategy in strategies:
        result = evaluate_strategy(strategy, num_iterations)
        print(
            f"{strategy.__name__}: avg_time: {result["avg_time"]}, avg_late_by_9: {
                sum(employee_floor_distribution) - result["avg_num_completed_by_9"]}",
        )


def calibrate_model():
    num_iterations = 1000

    print("# iterations:", num_iterations)

    print(f"start: {start_time}; end: {end_time}; mean {mean_arrival_time}")

    new_std_devs = list(range(50, 325, 25))

    for new_std_dev in new_std_devs:
        result = evaluate_strategy(
            random_passenger_assignment, num_iterations, std_dev=new_std_dev)
        print(f"with std_dev {new_std_dev} avg_time: {result['avg_time']} avg_late_by_9: {sum(employee_floor_distribution) - result['avg_num_completed_by_9']}")

def plot_arrived_times():
    num_iterations = 1000
    total_completion_times = []
    for _ in range(num_iterations):
        total_completion_times += simulate(max_passenger_assignment)["employee_completion_times"]


    plot_times(total_completion_times, scale=1 / num_iterations, bin_width=50, left_bound=None, right_bound=None)

if __name__ == "__main__":
    analyze_strategies_time_and_completion()
