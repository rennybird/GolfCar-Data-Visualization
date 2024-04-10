import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, kp, ki, kd, set_point=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.set_point = set_point
        self.previous_error = 0
        self.integral = 0

    def compute(self, current_value, delta_time):
        error = self.set_point - current_value
        self.integral += error * delta_time
        derivative = (error - self.previous_error) / delta_time if delta_time > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        return output

class LaneSteeringSimulation:
    def __init__(self):
        self.raw_deviations = []
        self.pid_controller = PIDController(kp=0.1, ki=0.0, kd=0.05)

    def load_deviations_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.raw_deviations = [float(line.strip()) for line in file.readlines()]

    def run_simulation(self):
        delta_time = 1  # Assuming 1 second between frames for simplicity
        steering_angles = []
        for deviation in self.raw_deviations:
            steering_angle = self.pid_controller.compute(deviation, delta_time)
            steering_angles.append(steering_angle)
        return steering_angles

    def visualize_simulation(self):
        steering_angles = self.run_simulation()
        plt.figure(figsize=(10, 6))
        plt.plot(steering_angles, label='PID Steering Angles', color='blue')
        plt.axhline(y=-40, color='red', linestyle='--', label='Left Threshold (-40)')
        plt.axhline(y=40, color='green', linestyle='--', label='Right Threshold (40)')
        plt.title('Lane Steering Simulation with PID Control')
        plt.xlabel('Frame')
        plt.ylabel('Steering Angle')
        plt.legend()
        plt.show()
        
simulation = LaneSteeringSimulation()
simulation.load_deviations_from_file('Result5.txt')
simulation.visualize_simulation()