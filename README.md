# elevator-problem

A simulation of the classic elevator queueing math modeling problem.  

## Simulation Description

The model is implemented in the Python programming language and is based on time steps. It takes an input of a strategy function, and uses that strategy function to calculate the amount of time it would take to send all employees to their respective floors (more about the model in the description of `simulation.py`).  

## Usage

1. download the repo (either by downloading zip or doing `git clone https://github.com/Moonflower2022/elevator-problem`)
2. cd to the directory
3. run `python simulation.py`
4. extra: if you want to see the graph in `arrival_times.py` you need to download `matplotlib` using `python -m pip install matplotlib`, and then run `python arrival_times.py`

(`python` could be replaced by `py`, `python3`, or `python3.x` where x is your python version)

## Files

There are five python files, and each of them do a part in the simulation.

* `arrival_times.py`: Generates arrival times of the employees according to a normal distribution, draws graph of the distribution.
* `elevator.py`: Implements the elevator class, which is what keeps track of the elevators, their passengers, and their return times (how long it would take for them to get back to the lobby).
* `strategies.py`: Implements five strategies:
  * `random_passenger_assignment`: Elevators just take anyone who is in the lobby in a random order.
  * `max_passenger_assignment`: Repeatedly load the maximum amount of people going to the same floor until we hit maximum capacity.
  * `match_check_passenger_assignment`: Same as `max_passenger_assignment`, but if adding another group going to the same floor would fill the elevator to max capacity without leaving anyone behind, take them.
  * `proximity_passenger_assignment`: Same as `match_check_passenger_assignment`, but after the check, taking people from floors below, then above the first group’s floor.
  * `no_match_check_proximity_passenger_assignment`: Same as `proximity_passenger_assignment`, but there is no match check.
* `constants.py`: Stores the constants for the simulation in a file for the sake of importing to other files.
* `simulation.py`: Implements the actual simulation. Every second, the model runs an update step which includes checking if employees arrived (if they do, add them to the lobby), updating the time that unavailable elevators need to get back to the lobby, and using the strategy function, determine which passengers would go in which available elevators.  
