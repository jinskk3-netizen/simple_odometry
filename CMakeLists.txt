cmake_minimum_required(VERSION 3.8)
project(simple_odometry)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Поиск зависимостей
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(robot_localisation REQUIRED)
find_package(rf2o_laser_odometry REQUIRED)

# 2. Создание исполняемого файла
add_executable(odometry_node src/odometry_node.cpp)

# 3. ПОДКЛЮЧЕНИЕ ЗАВИСИМОСТЕЙ (Это исправит ошибку rclcpp.hpp)
ament_target_dependencies(odometry_node
  rclcpp
  geometry_msgs
  nav_msgs
  tf2
  tf2_ros
  sensor_msgs
  std_msgs
  tf2_geometry_msgs
  robot_localization
  rf2o_laser_odometry
)

# 4. ПРАВИЛЬНАЯ УСТАНОВКА (Это исправит ошибку с отсутствием libexec/lib папки)
# Устанавливаем сам бинарник ноды в lib/simple_odometry
install(TARGETS odometry_node
  DESTINATION lib/${PROJECT_NAME}
)

# Копируем лаунчи и конфиги в share/simple_odometry
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
