import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_forklift_sim = get_package_share_directory('forklift_sim')
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')
    pkg_explore_lite = get_package_share_directory('explore_lite')

    # Point to your latest navigation/mapping parameter file
    nav2_params_file = os.path.join(pkg_forklift_sim, 'config', 'nav2_params_sim.yaml')

    # 1. Include Gazebo simulation and forklift spawn launch file
    spawn_forklift_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_forklift_sim, 'launch', 'spawn_forklift.launch.py')
        )
    )

    # 2. Include SLAM Toolbox for online asynchronous mapping
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'slam_params_file': nav2_params_file
        }.items()
    )

    # 3. Include Explore Lite for autonomous frontier-based exploration
    explore_lite_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_explore_lite, 'launch', 'explore.launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([
        spawn_forklift_launch,
        slam_toolbox_launch,
        explore_lite_launch
    ])