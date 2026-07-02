from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('simple_odometry')
    params_file = os.path.join(pkg_share, 'config', 'params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'params_file',
            default_value=params_file,
            description='Full path to the ROS2 parameters file'
        ),
        Node(
            package='simple_odometry',
            executable='odometry_node',
            name='odometry_node',
            output='screen',
            parameters=[LaunchConfiguration('params_file')]
        )
    ])
