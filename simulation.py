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


def simulate(strategy):
    elevators = [Elevator(num_floors, max_capacity) for _ in range(num_elevators)]

    lobby = [0] * num_floors

    arrival_times = generate_arrival_times(
        people_distribution,
        mean_arrival_time,
        std_dev_arrival_time,
        start_time,
        end_time,
    )

    total_seconds = 4500

    for simulation_seconds in range(
        total_seconds
    ):  # simulate from 0 (9:45) to 4500 (9:00)

        ## Check if empolyees arrived
        i = 0
        while i < len(arrival_times):
            time, floor = arrival_times[i]
            if time <= simulation_seconds:
                lobby[floor - 1] += 1
                arrival_times.pop(i)
            else:
                i += 1

        ## Update time it takes for elevators to send their passengers to their floor and get back to the lobby
        for elevator in elevators:
            if math.floor(elevator.available_in) != 0:
                elevator.available_in -= 1
            else:
                elevator.available_in = 0

            if math.floor(elevator.passengers_arrive_in) != 0:
                elevator.passengers_arrive_in -= 1
            else:
                elevator.passengers_arrive_in = 0

        ## Apply the strategies and send people with available elevators
        if any(lobby):
            passengers = strategy(lobby, elevators)
            for i, elevator in enumerate(elevators):
                if any(passengers[i]):
                    if elevator.available_in != 0:
                        raise Exception(
                            f"gave elevator {elevator} passengers but it is not avaialable"
                        )
                    elevator.pick_up_passengers(passengers[i])
        else:
            if not arrival_times:
                return simulation_seconds + max(
                    [elevator.passengers_arrive_in for elevator in elevators]
                )


def evaluate_strategy(strategy, iterations):
    total = sum([simulate(strategy) for _ in range(iterations)])
    return total / iterations


if __name__ == "__main__":
    strategies = [
        random_passenger_assignment,
        max_passenger_assignment,
        match_check_passenger_assignment,
        no_match_check_proximity_passenger_assignment,
        proximity_passenger_assignment,
    ]

    num_iterations = 10000

    print("# iterations:", num_iterations)

    for strategy in strategies:
        print(
            f"avg total time for strategy {strategy.__name__}:",
            evaluate_strategy(strategy, num_iterations),
        )
