import numpy as np

import matplotlib.pyplot as plt

class LaneSteeringSimulation:
    def __init__(self):
        self.raw_deviations = []

    def load_deviations_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_deviations = [float(line.strip()) for line in file.readlines()]

    def determine_steering_direction(self, deviation):
        if deviation > -160:
            return "Steer Left"
        elif deviation < -200:
            return "Steer Right"
        else:
            return "Stay Straight"

    def run_simulation(self):
        steering_decisions = [self.determine_steering_direction(deviation) for deviation in self.raw_deviations]
        return steering_decisions

    def visualize_simulation(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.raw_deviations, label='Raw Deviations', color='blue')
        plt.axhline(y=-160, color='red', linestyle='--', label='Left Threshold')
        plt.axhline(y=-200, color='green', linestyle='--', label='Right Threshold')
        plt.title('Lane Steering Simulation')
        plt.xlabel('Frame')
        plt.ylabel('Deviation')
        plt.legend()
        plt.show()

# Initialize and run the simulation
simulation = LaneSteeringSimulation()
simulation.load_deviations_from_file('Result5.txt')
steering_decisions = simulation.run_simulation()
simulation.visualize_simulation()
