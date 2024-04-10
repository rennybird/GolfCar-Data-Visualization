import numpy as np
import matplotlib.pyplot as plt

class LaneSteeringSimulation:
    def __init__(self):
        self.raw_deviations = []

    def load_deviations_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_deviations = [float(line.strip()) for line in file.readlines()]

    def map_deviation_to_steering(self, deviation, d_min=-200, d_max=-160, s_min=-1, s_max=1):
        steering_angle = ((deviation - d_min) / (d_max - d_min)) * (s_max - s_min) + s_min
        print(f"Deviation: {deviation} -> Steering Angle: {steering_angle:.2f}")
        return steering_angle

    def determine_steering_direction(self, deviation):
        steering_angle = self.map_deviation_to_steering(deviation)
        if steering_angle > 0:
            return "Steer Right"
        elif steering_angle < 0:
            return "Steer Left"
        else:
            return "Stay Straight"

    def run_simulation(self):
        steering_angles = [self.map_deviation_to_steering(deviation) for deviation in self.raw_deviations]
        return steering_angles

    def visualize_simulation(self):
        steering_angles = self.run_simulation()
        plt.figure(figsize=(10, 6))
        plt.plot(steering_angles, label='Mapped Steering Angles', color='blue')
        plt.axhline(y=-1, color='red', linestyle='--', label='Left Threshold')
        plt.axhline(y=1, color='green', linestyle='--', label='Right Threshold')
        plt.title('Lane Steering Simulation')
        plt.xlabel('Frame')
        plt.ylabel('Steering Angle')
        plt.legend()
        plt.show()

# Initialize and run the simulation
simulation = LaneSteeringSimulation()
simulation.load_deviations_from_file('Result5.txt')
simulation.visualize_simulation()
