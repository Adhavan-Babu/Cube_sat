import matplotlib.pyplot as plt
import time
import random

# Simulated battery parameters
battery_percent = 100

# Data storage
times = []
battery_levels = []

start_time = time.time()

plt.ion()  # interactive mode

while battery_percent > 0:
    print(f"Battery: {battery_percent:.2f}%")
    current_time = time.time() - start_time

    # 🔋 Simulate battery drain + slight randomness
    battery_percent -= random.uniform(0.2, 0.8)
    battery_percent = max(battery_percent, 0)

    # Store values
    times.append(current_time)
    battery_levels.append(battery_percent)

    # Plot
    plt.clf()
    plt.plot(times, battery_levels)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Battery (%)")
    plt.title("Simulated Battery Drain")
    plt.ylim(0, 100)

    plt.pause(0.1)

plt.ioff()
print("graphing complete!")
plt.savefig("battery_graph.png")

