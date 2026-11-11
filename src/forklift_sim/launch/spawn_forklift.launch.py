import os
import subprocess
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def gazebo_env():
    out = subprocess.run(
        ['bash', '-c', 'source /usr/share/gazebo/setup.sh >/dev/null 2>&1; env'],
        capture_output=True, text=True).stdout
    pairs = (line.partition('=') for line in out.splitlines())
    return {k: v for k, _, v in pairs if k.startswith(('GAZEBO_', 'OGRE_'))}

def generate_launch_description():
    pkg_share = get_package_share_directory('forklift_sim')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_world = get_package_share_directory('aws_robomaker_small_warehouse_world')

    world_file = os.path.join(pkg_world, 'worlds', 'small_warehouse', 'small_warehouse.world')

    # Gazebo environment + models of the warehouse world
    env = gazebo_env()
    env['GAZEBO_MODEL_DATABASE_URI'] = ''  # do not try to reach the online database
    env['GAZEBO_MODEL_PATH'] = (os.path.join(pkg_world, 'models') + os.pathsep
                                + env.get('GAZEBO_MODEL_PATH', ''))
    env_actions = [SetEnvironmentVariable(k, v) for k, v in env.items()]

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': world_file}.items()
    )

    xacro_file = os.path.join(pkg_share, 'urdf', 'robot_model_sim.urdf.xacro')
    robot_description = {'robot_description': xacro.process_file(xacro_file).toxml()}

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'forklift_robot',
                   '-x', '0.0', '-y', '0.0', '-z', '0.05', '-Y', '0.0',
                   '-timeout', '120'],
        output='screen'
    )

    return LaunchDescription(env_actions + [gazebo, robot_state_publisher, spawn_entity])