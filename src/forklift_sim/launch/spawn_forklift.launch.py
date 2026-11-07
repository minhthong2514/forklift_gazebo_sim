import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('forklift_sim')

    # Expand the xacro into a plain URDF string
    xacro_file = os.path.join(pkg_share, 'urdf', 'car_sim.urdf.xacro')
    robot_description = {'robot_description': xacro.process_file(xacro_file).toxml()}

    # Start Gazebo Classic with the ROS 2 init + factory plugins
    start_gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose',
             '-s', 'libgazebo_ros_init.so',
             '-s', 'libgazebo_ros_factory.so'],
        # Avoid Gazebo hanging while trying to reach the online model database
        additional_env={'GAZEBO_MODEL_DATABASE_URI': ''},
        output='screen'
    )

    # Publishes the static TF of all fixed joints and the wheel joints
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    # Spawn the robot slightly above the ground (base_footprint is at ground level)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'forklift_robot',
                   '-z', '0.05'],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo,
        robot_state_publisher,
        spawn_entity,
    ])
