from setuptools import find_packages, setup

package_name = 'srbot_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sumukh',
    maintainer_email='sumukh.porwal@gmail.com',
    description='Contains all the python programs required to run srbot',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'speed_convertor = srbot_nodes.speed_convertor:main',
            'teleop_keyboard = srbot_nodes.teleop_keyboard:main',
            'encoder_ticks_to_odom = srbot_nodes.encoder_ticks_to_odom:main',
            'inverse_kinematics = srbot_nodes.inverse_kinematics:main',
            'forward_kinematics = srbot_nodes.forward_kinematics:main',
            'imu_data_transformer = srbot_nodes.imu_data_transformer:main',
            'plotjuggler = srbot_nodes.plotjuggler:main',
            'test_odom = srbot_nodes.test_odom:main',
            'robot_navigator = srbot_nodes.robot_navigator:main',
            'waypoint = srbot_nodes.waypoint:main',
        ],
    },
)
