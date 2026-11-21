import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np
from std_msgs.msg import Float32MultiArray

class ObstacleDetection(Node):
    def __init__(self):
        super().__init__('obstacle_detection')
        self.subscription = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        self.cv_bridge = CvBridge()
        self.publisher = self.create_publisher(
            Float32MultiArray,
            'obstacle_coordinates',
            10
        )

        # Define the region to exclude as the floor (adjust these values as needed)
        self.floor_region_height = 100  # Pixels from the bottom to consider as floor
        self.image_height = None  # Will be set in the image_callback

    def image_callback(self, msg):
        try:
            # Convert the compressed image message to a BGR image
            cv_image = self.cv_bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")
            self.image_height, image_width, _ = cv_image.shape

            # Exclude the lower part of the image as floor
            cv_image[self.image_height - self.floor_region_height :, :] = [0, 0, 0]

            # Convert BGR image to grayscale
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Perform obstacle segmentation (adjust threshold value as needed)
            _, obstacle_mask = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

            # Find contours of obstacles
            contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            obstacle_data = Float32MultiArray()
            obstacle_data.data = []

            for contour in contours:
                # Calculate the centroid (x, y) of the obstacle
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Calculate the depth (z) assuming a simple linear relationship (adjust as needed)
                    z = self.image_height - cy

                    # Calculate the area of the obstacle
                    area = cv2.contourArea(contour)

                    # Append obstacle data to the Float32MultiArray
                    obstacle_data.data.extend([float(cx), float(cy), float(z), float(area)])

            # Publish the obstacle data
            self.publisher.publish(obstacle_data)

        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    obstacle_detection = ObstacleDetection()
    rclpy.spin(obstacle_detection)
    obstacle_detection.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
