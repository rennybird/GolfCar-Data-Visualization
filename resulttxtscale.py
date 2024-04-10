import numpy as np
import matplotlib.pyplot as plt

class LaneSteeringSimulation:
    def __init__(self):
        self.raw_deviations = []
        self.scaled_deviations = []

    def load_deviations_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_deviations = [float(line.strip()) for line in file.readlines()]
        self.scale_deviations()

    def scale_deviations(self):
        original_min, original_max = -200, -160
        target_min, target_max = -1, 1
        self.scaled_deviations = [(deviation - original_min) / (original_max - original_min) * (target_max - target_min) + target_min for deviation in self.raw_deviations]

    def determine_steering_direction(self, scaled_deviation):
        if scaled_deviation > 0:
            return "Steer Left"
        elif scaled_deviation < 0:
            return "Steer Right"
        else:
            return "Stay Straight"

    def run_simulation(self):
        steering_decisions = [self.determine_steering_direction(scaled_deviation) for scaled_deviation in self.scaled_deviations]
        return steering_decisions

    def visualize_simulation(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.scaled_deviations, label='Scaled Deviations', color='blue')
        plt.axhline(y=1, color='red', linestyle='--', label='Left Threshold (1)')
        plt.axhline(y=-1, color='green', linestyle='--', label='Right Threshold (-1)')
        plt.title('Lane Steering Simulation')
        plt.xlabel('Frame')
        plt.ylabel('Scaled Deviation')
        plt.legend()
        plt.show()

simulation = LaneSteeringSimulation()
simulation.load_deviations_from_file('Result5.txt')  # Adjust path as necessary
steering_decisions = simulation.run_simulation()
simulation.visualize_simulation()
