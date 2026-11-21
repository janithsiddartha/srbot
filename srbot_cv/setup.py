from setuptools import find_packages, setup

package_name = 'srbot_cv'

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
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yellow_detect = srbot_nodes.yellow_detect:main',
            'floor_segmentation_1 = srbot_nodes.floor_segmentation_1:main',
            'floor_segmentation_2 = srbot_nodes.floor_segmentation_2:main',
        ],
    },
)
