import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory('tugbot_navigation2')

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    rviz_config_file = LaunchConfiguration('rviz_config')

    nav2_launch_file_dir = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'launch'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=os.path.join(package_share, 'map', 'map.yaml'),
            description='Full path to map file to load'
        ),

        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(
                package_share,
                'config',
                'navigation2.yaml'
            ),
            description='Full path to param file to load'
        ),

        DeclareLaunchArgument(
            'rviz_config',
            default_value=os.path.join(package_share, 'rviz', 'nav2.rviz'),
            description='Full path to RViz config file'
        ),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),

        # bringup_launch.py starts map_server, AMCL, both costmaps and their
        # lifecycle managers. Do not start a second AMCL node in this file.
        GroupAction(
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(nav2_launch_file_dir, 'bringup_launch.py')
                    ),
                    launch_arguments={
                        'map': map_file,
                        'use_sim_time': use_sim_time,
                        'params_file': params_file,
                        'autostart': 'true'
                    }.items(),
                ),
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        ),
    ])
