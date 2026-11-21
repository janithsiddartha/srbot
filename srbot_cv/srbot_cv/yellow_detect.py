import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class YellowObjectDetection(Node):
    def __init__(self):
        super().__init__('yellow_object_detection')
        self.subscription = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',
            self.image_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        self.cv_bridge = CvBridge()
        self.publisher = self.create_publisher(
            CompressedImage,
            'opencv_vid',
            10
        )

    def image_callback(self, msg):
        try:
            # Convert the compressed image message to a BGR image
            cv_image = self.cv_bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # Convert BGR image to HSV color space
            hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # Define the lower and upper bounds for yellow color in HSV
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            # Threshold the image to detect yellow objects
            yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

            # Find contours of yellow objects
            contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw bounding boxes around yellow objects with an area > 50
            for contour in contours:
                if cv2.contourArea(contour) > 50:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Publish the processed image
            self.publisher.publish(self.cv_bridge.cv2_to_compressed_imgmsg(cv_image))

        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    yellow_object_detection = YellowObjectDetection()
    rclpy.spin(yellow_object_detection)
    yellow_object_detection.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
