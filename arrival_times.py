import numpy as np
import matplotlib.pyplot as plt


def generate_arrival_times(
    people_distribution, mean_time, std_dev, start_time, end_time
):  # generated using ChatGPT-4o
    """
    Generates arrival times paired with floor numbers for each person.

    Parameters:
    - people_distribution: A list where each index corresponds to a floor and the value is the number of people on that floor.
    - mean_time: Mean arrival time for the distribution.
    - std_dev: Standard deviation of the arrival times.
    - start_time: The earliest time an employee can arrive.
    - end_time: The latest time an employee can arrive.

    Returns:
    - A list of tuples where each tuple is (arrival_time, floor_number).
    """
    all_arrival_times = []

    for floor, num_people in enumerate(people_distribution, start=1):
        arrival_times = np.random.normal(loc=mean_time, scale=std_dev, size=num_people)
        arrival_times = np.clip(arrival_times, start_time, end_time)
        arrival_times.sort()

        # Pair each arrival time with the floor number
        paired_times = [(arrival_time, floor) for arrival_time in arrival_times]
        all_arrival_times.extend(paired_times)

    # Sort all arrival times across all floors
    all_arrival_times.sort(key=lambda x: x[0])

    return all_arrival_times


def plot_arrival_times(arrival_times, num_bins=50):  # generated using ChatGPT-4o
    """
    Plots the arrival times grouped by floor with different colors.

    Parameters:
    - arrival_times: A list of tuples (arrival_time, floor_number).
    - num_bins: Number of bins to use for the histogram.
    """
    # Separate arrival times by floor
    floors = list(set(floor for _, floor in arrival_times))
    floor_colors = plt.cm.viridis(np.linspace(0, 1, len(floors)))

    # Prepare the plot
    plt.figure(figsize=(12, 6))
    max_time = max(arrival_times, key=lambda x: x[0])[0]
    bins = np.linspace(0, max_time, num_bins)

    # Initialize the stacked histogram data
    hist_data = {floor: np.zeros(len(bins) - 1) for floor in floors}

    # Calculate the histogram for each floor
    for floor in floors:
        # Extract arrival times for this floor
        floor_times = [time for time, flr in arrival_times if flr == floor]

        # Compute histogram for this floor
        hist, _ = np.histogram(floor_times, bins=bins)
        hist_data[floor] = hist

    # Stack the histograms
    bottom = np.zeros(len(bins) - 1)
    for floor, color in zip(floors, floor_colors):
        plt.bar(
            bins[:-1],
            hist_data[floor],
            width=bins[1] - bins[0],
            bottom=bottom,
            color=color,
            edgecolor="black",
            alpha=0.7,
            label=f"Floor {floor}",
        )
        bottom += hist_data[floor]

    # Add labels and legend
    plt.xlabel("Arrival Time (seconds)")
    plt.ylabel("Number of Arrivals")
    plt.title("Employee Arrival Times by Floor")
    plt.legend(title="Floor")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    people_distribution = [100, 120, 60, 120, 80, 20]
    mean_arrival_time = 300
    std_dev_arrival_time = 100
    start_time = 0
    end_time = 600
    arrival_times = generate_arrival_times(
        people_distribution,
        mean_arrival_time,
        std_dev_arrival_time,
        start_time,
        end_time,
    )
    print("arrival_times:", arrival_times)
    print("len(arrival_times):", len(arrival_times))
    print("type(arrival_times):", type(arrival_times))
    plot_arrival_times(arrival_times, num_bins=50)
