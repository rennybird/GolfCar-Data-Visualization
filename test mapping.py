import ctypes
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32, String  # Import String for steering instructions
from camera_controller.yolop_inference2 import YolopTRT

class YolopInferenceNode(Node):
    def __init__(self, categories):
        super().__init__('yolop_inference_node')
        self.categories = categories
        
        # Assuming the plugin file and yolop model path are correct
        self.plugin_file = "/media/inc/64fdc28e-1c24-427f-bec3-0bf20738fe6b2/ros2_camera/src/camera_controller/camera_controller/libmyplugins.so"
        ctypes.CDLL(self.plugin_file)
        self.yolop = YolopTRT("/media/inc/64fdc28e-1c24-427f-bec3-0bf20738fe6b2/ros2_camera/src/camera_controller/camera_controller/yolop.trt", self.categories)
        
        self.bridge = CvBridge()
        
        # Publishers
        self.processed_image_publisher = self.create_publisher(Image, 'processed_image', 10)
        self.deviation_publisher = self.create_publisher(Float32, 'lane_deviation', 10)
        self.steering_instruction_publisher = self.create_publisher(String, 'steering_instruction', 10)
        self.control_action_publisher = self.create_publisher(Float32, 'control_action', 10)
        
        # Subscription
        self.subscription = self.create_subscription(Image, 'image_raw', self.image_callback, 10)
        
        self.last_time = None

    def map_deviation_to_steering(self, deviation, d_min=-200, d_max=-160, s_min=-40, s_max=40):
        return ((deviation - d_min) / (d_max - d_min)) * (s_max - s_min) + s_min

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            processed_images, _, deviations = self.yolop.infer([cv_image])
            processed_image = processed_images[0] if processed_images else None
            deviation = deviations[0] if deviations else None

            if processed_image is not None:
                processed_image_msg = self.bridge.cv2_to_imgmsg(processed_image, encoding="bgr8")
                processed_image_msg.header = msg.header
                self.processed_image_publisher.publish(processed_image_msg)

            if deviation is not None:
                steering_angle = self.map_deviation_to_steering(deviation)
                control_action_msg = Float32()
                control_action_msg.data = steering_angle
                self.control_action_publisher.publish(control_action_msg)
                self.get_logger().info(f"Published Control Action (Steering Angle): {steering_angle}")

                # Additionally, publish the deviation value if needed
                deviation_msg = Float32()
                deviation_msg.data = deviation
                self.deviation_publisher.publish(deviation_msg)
                self.get_logger().info(f"Published Deviation: {deviation}")

        except CvBridgeError as e:
            self.get_logger().error(f"CvBridge Error: {e}")
        except Exception as e:
            self.get_logger().error(f"YOLOP Inference Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    categories = ["car"]
    yolop_node = YolopInferenceNode(categories)
    rclpy.spin(yolop_node)
    yolop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
