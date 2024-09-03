from constants import fill_time_per_person, floor_travel_time, door_open_time


def time_to_return_to_lobby(passengers):
    floors = list(set(passengers))

    return (
        len(passengers) * fill_time_per_person
        + 2 * max(floors) * floor_travel_time
        + len(floors) * door_open_time
    )


def time_to_send_all_passengers(passengers):
    floors = list(set(passengers))

    return (
        len(passengers) * fill_time_per_person
        + max(floors) * floor_travel_time
        + (len(floors) - 1) * door_open_time
    )


def generate_complete_times(passengers):
    floors = sorted(set(passengers))

    return [
        [
            floor,
            passengers.count(floor),
            len(passengers) * fill_time_per_person
            + floor * floor_travel_time
            + i * door_open_time,  # they clock in as soon as they leave the elevator
        ]
        for i, floor in enumerate(floors)
    ]


class Elevator:
    def __init__(self, num_floors, max_capacity):
        self.num_floors = num_floors
        self.max_capacity = max_capacity
        self.reset()

    def pick_up_passengers(self, passengers):
        self.passengers = passengers
        self.available_in = time_to_return_to_lobby(passengers)
        self.passenger_complete_times = generate_complete_times(passengers)

    def reset(self):
        self.passengers = [
            0
        ] * self.num_floors  # indicies are the floor number shifted by -1
        self.available_in = 0
        self.passenger_complete_times = []  # tuples of (floor, arrival time)

    def __str__(self):
        return f"<Elevator object; passengers: {self.passengers}; available_in: {self.available_in}>"


if __name__ == "__main__":
    import random
    from constants import max_capacity

    iterations = 10000

    print(
        sum(
            time_to_return_to_lobby([random.randint(1, 6) for _ in range(max_capacity)])
            for _ in range(iterations)
        )
        / iterations
    )
