# srbot_simulation

Go to terminal and run:
1. `sudo apt install git -y`
2. `mkdir -p ~/ros2_ws/src` (if directory ros2_ws doesn't exist)
3. `cd ~/ros2_ws/src`
4. `git clone git@github.com:Sumukh18/srbot_simulation.git`
5. `cd srbot_simulation/`
6. `chmod +x install.sh`
7. `./install.sh`

**Important:**

Now follow these steps:
1. Open a new terminal and run `gazebo`.
2. Go to the "Insert" tab at the top of left bar.
3. From the drop-down menu of your "GAZEBO_MODEL_PATH" directory, add `srbot` and `srbot_house` to the gazebo environment.
4. After this, you can close Gazebo.

**Gazebo Simulations:**

1. Run `ros2 launch srbot_description simulation.launch.py` to launch Gazebo and RViz.
2. Run `ros2 run srbot_teleop keyboard` to control srbot using your keyboard.

**SLAM:** 

1. Run `ros2 launch srbot_description nav2.launch.py slam:=True`.
2. For keyboard control, run `ros2 run srbot_teleop teleop_keyboard`.
3. To save your map, run to `cd ros2_ws/src/srbot_simulation_ros2/srbot_description/maps/` and then to save map run `ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/srbot_simulation/srbot_description/maps/{name_of_your_map}`

**Navigation:**

**If you are using your own map**, follow these steps before starting the Navigation Stack:

1. Change `static_map_path = os.path.join(pkg_share, 'maps', 'house.yaml')` to `static_map_path = os.path.join(pkg_share, 'maps', '{name_of_your_map}.yaml')` in **/srbot_description/launch/nav2.launch.py**.
2. Change `default_value=os.path.join(map_dir, 'maps', 'house.yaml')` to `default_value=os.path.join(map_dir, 'maps', '{name_of_your_map}.yaml')` in **/srbot_navigation/launch/localization.launch.py**.
3. Change `yaml_filename: "house.yaml"` to `yaml_filename: "{name_of_your_map}.yaml"` in **/srbot_navigation/params/srbot_nav2_params.yaml**.

To launch the navigation stack:

1. Run `ros2 launch srbot_description nav2.launch.py`.
2. Click the **2D Pose Estimate button** in the RViz2 menu. (Position of the robot will be near outside wall and below main gate of the house).
3. Click on the map where the robot is located in gazebo and drag the large green arrow toward the direction where the robot is facing.
4. After this, click the **Navigation2 Goal** button in the RViz2 menu.
5. Click on the map to set the destination of the robot and drag the green arrow toward the direction where the robot will be facing.

Waypoint Navigation:

1. Run `ros2 launch srbot_description nav2.launch.py`.
2. Click the **2D Pose Estimate** button in the RViz2 menu. (Position of the robot will be near outside wall and below main gate of the house).
3. Now click the **Waypoint mode** button in the bottom left corner of RViz. Clicking this button puts the system in waypoint follower mode.
4. Click **Navigation2 Goal** button, and click on areas of the map where you would like your robot to go (i.e. select your waypoints). Select as many waypoints as you want.
5. When you’re ready for the robot to follow the waypoints, click the **Start Navigation** button in the bottom left corner of RViz.

**Note:** 
* This green arrow is a marker that can specify the destination of the robot.
* The root of the arrow is x, y coordinate of the destination, and the angle θ is determined by the orientation of the arrow.
* As soon as x, y, θ are set, srbot will start moving to the destination immediately.