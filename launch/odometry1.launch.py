import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('simple_odometry')
    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')

    return LaunchDescription([
        # 1. Ваш исходный узел колесной одометрии (переименуем топик для ясности)
        Node(
            package='simple_odometry',
            executable='simple_odometry_node',
            name='wheel_odometry',
            remappings=[('/odom', '/odom_wheel')]
        ),

        # 2. Лидарная одометрия rf2o (считает смещение по лазерным лучам)
        Node(
            package='rf2o_laser_odometry',
            executable='rf2o_laser_odometry_node',
            name='rf2o_laser_odometry',
            parameters=[{
                'laser_scan_topic': '/scan',
                'odom_topic': '/odom_lidar',
                'publish_tf': False, # TF будет публиковать сам EKF
                'base_frame_id': 'base_link',
                'odom_frame_id': 'odom',
                'freq': 10.0
            }]
        ),

        # 3. Узел Фильтра Калмана (EKF)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            parameters=[ekf_config_path],
            remappings=[('/odometry/filtered', '/odom')] # Фильтрованный топик становится основным
        )
    ])
