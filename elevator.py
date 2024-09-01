from constants import fill_time_per_person, floor_travel_time, door_open_time


def time_to_return_to_lobby(passengers):
    floors = set(sorted(passengers))

    return (
        len(passengers) * fill_time_per_person
        + 2 * max(floors) * floor_travel_time
        + len(floors) * door_open_time
    )


def time_to_send_all_passengers(passengers):
    floors = set(sorted(passengers))

    return (
        len(passengers) * fill_time_per_person
        + max(floors) * floor_travel_time
        + len(floors) * door_open_time
    )


class Elevator:
    def __init__(self, num_floors, max_capacity):
        self.passengers = [
            0
        ] * num_floors  # indicies are the floor number shifted by -1
        self.available_in = 0
        self.passengers_arrive_in = 0
        self.max_capacity = max_capacity

    def pick_up_passengers(self, passengers):
        self.passengers = passengers
        self.available_in = time_to_return_to_lobby(passengers)
        self.passengers_arrive_in = time_to_send_all_passengers(passengers)

    def __str__(self):
        return f"<Elevator object; passengers: {self.passengers}; available_in: {self.available_in}>"
