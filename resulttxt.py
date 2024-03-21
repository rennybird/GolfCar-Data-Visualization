import numpy as np
import matplotlib.pyplot as plt

class LaneSteeringSimulation:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.raw_deviations = []
        self.filtered_deviations = []

    def load_deviations_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_deviations = [float(line.strip()) for line in file.readlines()]

    def moving_average_filter(self):
        for i in range(len(self.raw_deviations)):
            if i < self.window_size:
                filtered_deviation = np.mean(self.raw_deviations[:i+1])
            else:
                filtered_deviation = np.mean(self.raw_deviations[i-self.window_size+1:i+1])
            self.filtered_deviations.append(filtered_deviation)

    def determine_steering_direction(self, deviation):
        if deviation > -160:
            return "Steer Left"
        elif deviation < -200:
            return "Steer Right"
        else:
            return "Stay Straight"

    def run_simulation(self):
        self.moving_average_filter()
        steering_decisions = [self.determine_steering_direction(deviation) for deviation in self.filtered_deviations]
        return steering_decisions

    def visualize_simulation(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.raw_deviations, label='Raw Deviations', color='red')
        plt.plot(self.filtered_deviations, label='Filtered Deviations', color='blue')
        plt.axhline(y=-160, color='green', linestyle='--', label='Left Threshold')
        plt.axhline(y=-200, color='green', linestyle='--', label='Right Threshold')
        plt.title('Lane Steering Simulation')
        plt.xlabel('Frame')
        plt.ylabel('Deviation')
        plt.legend()
        plt.show()

# Initialize and run the simulation
simulation = LaneSteeringSimulation(window_size=5)
simulation.load_deviations_from_file('Result2.txt')
steering_decisions = simulation.run_simulation()
simulation.visualize_simulation()
