import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class FloorSegmentation(Node):
    def __init__(self):
        super().__init__('floor_segmentation')
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
            'flr_segt_vid',
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

            # Create a mask for the floor region (entirely black)
            floor_mask = np.zeros_like(cv_image)

            # Convert the remaining image to grayscale
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Perform floor segmentation
            _, obstacle_mask = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

            # Set the floor region in the obstacle mask to black
            obstacle_mask[self.image_height - self.floor_region_height :, :] = 0

            # Convert the segmented obstacle mask to BGR format
            obstacle_mask_bgr = cv2.cvtColor(obstacle_mask, cv2.COLOR_GRAY2BGR)

            # Create the segmented image where the floor is black and obstacles are white
            segmented_image = obstacle_mask_bgr

            # Publish the segmented image
            segmented_msg = self.cv_bridge.cv2_to_compressed_imgmsg(segmented_image)
            self.publisher.publish(segmented_msg)

        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    floor_segmentation = FloorSegmentation()
    rclpy.spin(floor_segmentation)
    floor_segmentation.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
