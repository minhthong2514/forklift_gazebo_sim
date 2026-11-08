import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('forklift_sim')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_aws_world = get_package_share_directory('aws_robomaker_small_warehouse_world')

    # Path to the AWS small warehouse world file
    world_file = os.path.join(pkg_aws_world, 'worlds', 'small_warehouse.world')

    # Start Gazebo with the AWS warehouse world
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_file,
            'use_sim_time': 'true'
        }.items()
    )

    # Process the forklift URDF/Xacro file
    xacro_file = os.path.join(pkg_share, 'urdf', 'car_sim.urdf.xacro')
    robot_description = {'robot_description': xacro.process_file(xacro_file).toxml()}

    # Publish robot state (TF tree)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    # Spawn the forklift model into the Gazebo simulation
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'forklift_robot',
                   '-x', '0.0',
                   '-y', '0.0',
                   '-z', '0.1'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher,
        spawn_entity,
    ])