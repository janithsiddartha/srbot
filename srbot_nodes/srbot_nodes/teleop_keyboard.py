import pygame
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, Int32MultiArray


class KeyboardPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer_ = self.create_timer(0.067, self.publish_twist)  # Publishing rate of 20Hz
        self.twist_msg_ = Twist()
        self.is_w_pressed = False
        self.is_a_pressed = False
        self.is_s_pressed = False
        self.is_d_pressed = False
        self.is_q_pressed = False
        self.is_e_pressed = False
        self.is_z_pressed = False
        self.is_c_pressed = False

    def publish_twist(self):
        if self.is_w_pressed or self.is_a_pressed or self.is_s_pressed or self.is_d_pressed or self.is_q_pressed or self.is_e_pressed or self.is_z_pressed or self.is_c_pressed:
            
            self.twist_msg_.linear.x = 0.2 if self.is_w_pressed or self.is_q_pressed or self.is_e_pressed else (-0.2 if self.is_s_pressed or self.is_z_pressed or self.is_c_pressed else 0.0)
            self.twist_msg_.linear.y = 0.2 if self.is_q_pressed or self.is_a_pressed or self.is_z_pressed else (-0.2 if self.is_e_pressed or self.is_d_pressed or self.is_c_pressed else 0.0)

            self.publisher_.publish(self.twist_msg_)

    def display_screen(self, screen):

        screen.fill((255, 255, 255))

        # Display the control message
        control_font = pygame.font.Font(None, 20)
        control_text = control_font.render("Control srbot!", True, (0, 0, 0))
        screen.blit(control_text, (50, 100))

        message = """
        -----------------------------
        Moving robot:

        w: Move Forward
        s: Move Backward
        a: Move Left
        d: Move Right

        q: Move Forward-Left
        e: Move Forward-Right
        z: Move Backward-Left
        c: Move Backward-Right
        
        -----------------------------
        """

        control_y = 100
        control_lines = message.split('\n')
        for line in control_lines:
            control_text = control_font.render(line.strip(), True, (0, 0, 0))
            screen.blit(control_text, (50, control_y))
            control_y += 20

    def run(self):
        pygame.init()
        screen_width = 250
        screen_height = 480
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Keyboard Publisher')
        clock = pygame.time.Clock()

        while rclpy.ok():
            # Check if any keys are pressed
            # keys_pressed = pygame.key.get_pressed()

            # # Set twist_msg_ to stop if no keys are pressed
            # self.twist_msg_.linear.x = 0.0
            # self.twist_msg_.linear.y = 0.0

            # if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_q] or keys_pressed[pygame.K_e]:
            #     self.twist_msg_.linear.x = 0.2
            # elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_z] or keys_pressed[pygame.K_c]:
            #     self.twist_msg_.linear.x = -0.2

            # if keys_pressed[pygame.K_q] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_z]:
            #     self.twist_msg_.linear.y = 0.2
            # elif keys_pressed[pygame.K_e] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_c]:
            #     self.twist_msg_.linear.y = -0.2

            # self.publisher_.publish(self.twist_msg_)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.is_w_pressed = True
                    elif event.key == pygame.K_a:
                        self.is_a_pressed = True
                    elif event.key == pygame.K_s:
                        self.is_s_pressed = True
                    elif event.key == pygame.K_d:
                        self.is_d_pressed = True
                    elif event.key == pygame.K_q:
                        self.is_q_pressed = True
                    elif event.key == pygame.K_e:
                        self.is_e_pressed = True
                    elif event.key == pygame.K_z:
                        self.is_z_pressed = True
                    elif event.key == pygame.K_c:
                        self.is_c_pressed = True
                    
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.is_w_pressed = False
                    elif event.key == pygame.K_a:
                        self.is_a_pressed = False
                    elif event.key == pygame.K_s:
                        self.is_s_pressed = False
                    elif event.key == pygame.K_d:
                        self.is_d_pressed = False
                    elif event.key == pygame.K_q:
                        self.is_q_pressed = False
                    elif event.key == pygame.K_e:
                        self.is_e_pressed = False
                    elif event.key == pygame.K_z:
                        self.is_z_pressed = False
                    elif event.key == pygame.K_c:
                        self.is_c_pressed = False

            rclpy.spin_once(self)

            self.display_screen(screen)
            pygame.display.update()

            clock.tick(60)  # Increase frame rate

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardPublisher()
    node.run()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
