import numpy as np

import matplotlib.pyplot as plt

class LaneSteeringSimulation:
    def __init__(self):
        self.raw_deviations = []

    def load_deviations_from_files(self, file_paths):
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                self.raw_deviations.append([float(line.strip()) for line in file.readlines()])

    def determine_steering_direction(self, deviation):
        if deviation > -160:
            return "Steer Left"
        elif deviation < -200:
            return "Steer Right"
        else:
            return "Stay Straight"

    def run_simulation(self):
        steering_decisions = []
        for deviations in self.raw_deviations:
            steering_decisions.append([self.determine_steering_direction(deviation) for deviation in deviations])
        return steering_decisions

    def visualize_simulation(self):
        plt.figure(figsize=(10, 6))
        colors = ['blue', 'green', 'red', 'grey', 'magenta']
        for i, deviations in enumerate(self.raw_deviations):
            plt.plot(deviations, label=f'Raw Deviations {i+1}', color=colors[i])
        plt.axhline(y=-160, color='red', linestyle='--', label='Left Threshold')
        plt.axhline(y=-200, color='green', linestyle='--', label='Right Threshold')
        plt.title('Lane Deviation Data')
        plt.xlabel('Frame')
        plt.ylabel('Deviation(pixel)')
        plt.legend()
        plt.show()

# Initialize and run the simulation
simulation = LaneSteeringSimulation()
simulation.load_deviations_from_files(['Result1.txt', 'Result2.txt', 'Result3.txt', 'Result4.txt', 'Result5.txt'])
steering_decisions = simulation.run_simulation()
simulation.visualize_simulation()