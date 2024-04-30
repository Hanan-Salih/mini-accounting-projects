import numpy as np
import matplotlib.pyplot as plt

frequency = [30, 31, 30, 31, 39, 39, 39, 32, 35, 35, 31, 31, 40, 40, 40, 41, 42, 45, 45, 42, 41, 42, 41, 43, 50, 50, 52,
             55, 55, 51, 55]

# اCalculate the average
average = sum(frequency) / len(frequency)

# Calculate the squared differences from the mean
squared_diff = [(x - average) ** 2 for x in frequency]

# Calculate the variance
variance = sum(squared_diff) / len(frequency)

# Calculate the standard deviation
stander_deviation = variance ** 0.5

# Plotting the histogram
plt.hist(frequency, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.title(f'standard deviation for time of delivery: {stander_deviation:.2f}')
plt.xlabel('standard deviation of the given time')
plt.ylabel('frequency of receiving time')

plt.axhline(np.max(plt.gca().get_ylim()) * 0.95, color='r', linestyle='dashed', linewidth=1.3,
            label="latest")  # horizontal max line
plt.axhline(np.mean(plt.gca().get_ylim()), color='b', linestyle='dashed', linewidth=1.3,
            label='average of time')  # horizontal average line
plt.axhline(np.min(plt.gca().get_ylim()) + 0.99, color='g', linestyle='dashed', linewidth=1.3,
            label="earliest")  # horizontal min line
plt.legend()
plt.show()
