import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_forklift = get_package_share_directory('forklift_sim')
    pkg_slam = get_package_share_directory('slam_toolbox')
    pkg_nav2 = get_package_share_directory('nav2_bringup')
    pkg_explore = get_package_share_directory('explore_lite')
    config = os.path.join(pkg_forklift, 'config')
    explore_config = os.path.join(pkg_explore, 'config')
    rviz_config = os.path.join(pkg_forklift, 'rviz', 'rviz_default.rviz')

    # 1. Gazebo 
    spawn_forklift = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_forklift, 'launch', 'spawn_forklift.launch.py')))

    # 2. RViz 
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen')

    # 3. SLAM Toolbox
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam, 'launch', 'online_async_launch.py')),
        launch_arguments={
            'use_sim_time': 'true',
            'slam_params_file': os.path.join(config, 'slam_params_sim.yaml'),
        }.items())

    # 4. Nav2 navigation
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': 'true',
            'params_file': os.path.join(config, 'nav2_params_sim.yaml'),
            'autostart': 'true',
        }.items())

    # 5. Frontier exploration 
    explore = Node(
        package='explore_lite',
        executable='explore',
        name='explore_node',
        parameters=[os.path.join(explore_config, 'params.yaml'), {'use_sim_time': True}],
        output='screen')

    return LaunchDescription([
        spawn_forklift,
        rviz,
        slam_toolbox,
        nav2,
        # explore,
    ])