# Forklift Gazebo Simulation

This is a ROS 2 Humble workspace for simulating a custom Mecanum-drive forklift model in Gazebo, featuring omni-directional mobility, optimized physics, LiDAR scanning, and a ZED2 stereo camera simulation (designed to run without requiring CUDA or the ZED SDK in simulation).

## Simulation Preview
![Forklift Model in Gazebo Simulation](images/forklift_model_sim.png)

## Key Features
- **Omni-Directional Movement:** Full 3DOF planar mobility (linear X, linear Y, and angular Z) powered by the `planar_move` plugin.
- **Optimized Physics & Tuned Collisions:** Adjusted ground friction coefficients and chassis collision boxes to prevent sliding friction conflicts.
- **LiDAR Integration:** Equipped with a 360-degree LiDAR sensor for environment scanning and mapping.
- **ZED2 Stereo Camera Integration:** Accurate mechanical positioning of the ZED2 camera model mounted on a custom bracket (50-degree pitch alignment), providing RGB and Depth simulation topics via standard Gazebo plugins without needing hardware CUDA dependencies.

## Main Packages & Submodules in the Workspace
- **`forklift_sim`**: The core custom package containing the Mecanum forklift URDF/Xacro models, 3D meshes, sensor definitions, and Gazebo launch configurations.
- **`zed_description` (Submodule)**: Official Stereolabs package providing URDF descriptions and 3D visual/collision meshes for the ZED camera family (Apache 2.0 License).
- **`explore_lite` (Submodule)**: Provides autonomous frontier-based exploration algorithms (BSD License).
- **`slam_toolbox`**: Handles Simultaneous Localization and Mapping (SLAM) to generate real-time 2D occupancy grid maps.
- **`teleop_twist_keyboard`**: Enables manual keyboard teleoperation to test and control multi-directional movement via `/cmd_vel` topics.

---

## Getting Started
First, you must install all required dependencies for the workspace packages using `rosdep`:
```bash
sudo rosdep init # Only run if rosdep is not initialized yet
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### Clone the Repository (with Submodules)
If you are cloning this repository for the first time, make sure to initialize submodules:
```bash
git clone --recursive https://github.com/minhthong2514/forklift_gazebo_sim.git
```

### Build the Workspace 
Navigate to your workspace root directory and build using `colcon`:
```bash
cd forklift_gazebo_sim
colcon build --symlink-install
source install/setup.bash
```

### Running the Simulation
**Option 1: Autonomous Exploration**

Launch the core autonomous exploration and SLAM mapping pipeline:
```bash
ros2 launch forklift_sim bringup_mapping_sim.launch.py
```

**Option 2: Manual control and debugging**

Use this mode to manually test movement, inspect sensor topics, or debug physics using keyboard teleoperation:

1. Launch the base simulation environment:
```bash
ros2 launch forklift_sim spawn_forklift.launch.py
```
2. Open a new terminal and run teleop:
```bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
