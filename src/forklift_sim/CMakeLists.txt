cmake_minimum_required(VERSION 3.8)
project(forklift_sim)

find_package(ament_cmake REQUIRED)

# Install URDF/xacro, meshes and launch files into share/forklift_sim
install(
  DIRECTORY urdf meshes launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
