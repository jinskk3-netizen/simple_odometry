#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <chrono>
#include <memory>

using namespace std::chrono_literals;

class SimpleOdometryNode : public rclcpp::Node {
public:
  SimpleOdometryNode() : Node("odometry_node") {
    // Declare parameters
    declare_parameter("update_rate", 50.0);
    declare_parameter("initial_x", 0.0);
    declare_parameter("initial_y", 0.0);
    declare_parameter("initial_yaw", 0.0);
    declare_parameter("frame_id", "odom");
    declare_parameter("child_frame_id", "base_footprint");
    declare_parameter("use_imu_yaw", true);

    // Get parameters
    update_rate_ = get_parameter("update_rate").as_double();
    x_ = get_parameter("initial_x").as_double();
    y_ = get_parameter("initial_y").as_double();
    yaw_ = get_parameter("initial_yaw").as_double();
    frame_id_ = get_parameter("frame_id").as_string();
    child_frame_id_ = get_parameter("child_frame_id").as_string();
    use_imu_yaw_ = get_parameter("use_imu_yaw").as_bool();

    // Subscribers
    cmd_vel_sub_ = create_subscription<geometry_msgs::msg::Twist>(
      "/cmd_vel", 10, std::bind(&SimpleOdometryNode::cmdVelCallback, this, std::placeholders::_1));

    imu_sub_ = create_subscription<sensor_msgs::msg::Imu>(
      "/imu/data", 10, std::bind(&SimpleOdometryNode::imuCallback, this, std::placeholders::_1));

    // Publisher
    odom_pub_ = create_publisher<nav_msgs::msg::Odometry>("/odometry", 10);

    // TF broadcaster
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(this);

    // Timer
    timer_ = create_wall_timer(
      std::chrono::duration<double>(1.0 / update_rate_), 
      std::bind(&SimpleOdometryNode::updateOdometry, this));

    last_time_ = now();
    RCLCPP_INFO(get_logger(), "Simple Odometry Node started with rate %.1f Hz", update_rate_);
  }

private:
  void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    vx_ = msg->linear.x;
    vy_ = msg->linear.y;
  }

  void imuCallback(const sensor_msgs::msg::Imu::SharedPtr msg) {
    tf2::Quaternion q(msg->orientation.x, msg->orientation.y, msg->orientation.z, msg->orientation.w);
    tf2::Matrix3x3 m(q);
    double roll, pitch, yaw;
    m.getRPY(roll, pitch, yaw);
    yaw_ = yaw;
  }

  void updateOdometry() {
    auto current_time = now();
    double dt = (current_time - last_time_).seconds();
    if (dt <= 0.0) return;

    // Integrate position (body to world)
    x_ += (vx_ * cos(yaw_) - vy_ * sin(yaw_)) * dt;
    y_ += (vx_ * sin(yaw_) + vy_ * cos(yaw_)) * dt;

    last_time_ = current_time;

    // Odometry message
    nav_msgs::msg::Odometry odom_msg;
    odom_msg.header.stamp = current_time;
    odom_msg.header.frame_id = frame_id_;
    odom_msg.child_frame_id = child_frame_id_;

    odom_msg.pose.pose.position.x = x_;
    odom_msg.pose.pose.position.y = y_;
    odom_msg.pose.pose.position.z = 0.0;

    tf2::Quaternion q;
    q.setRPY(0.0, 0.0, yaw_);
    odom_msg.pose.pose.orientation = tf2::toMsg(q);

    // Twist
    odom_msg.twist.twist.linear.x = vx_;
    odom_msg.twist.twist.linear.y = vy_;
    odom_msg.twist.twist.angular.z = 0.0;

    odom_pub_->publish(odom_msg);

    // TF transform
    geometry_msgs::msg::TransformStamped transform;
    transform.header.stamp = current_time;
    transform.header.frame_id = frame_id_;
    transform.child_frame_id = child_frame_id_;
    transform.transform.translation.x = x_;
    transform.transform.translation.y = y_;
    transform.transform.translation.z = 0.0;
    transform.transform.rotation = tf2::toMsg(q);

    tf_broadcaster_->sendTransform(transform);
  }

  // Subscriptions and publishers
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::TimerBase::SharedPtr timer_;

  // State
  double vx_ = 0.0, vy_ = 0.0;
  double x_ = 0.0, y_ = 0.0, yaw_ = 0.0;
  rclcpp::Time last_time_;

  // Parameters
  double update_rate_;
  std::string frame_id_, child_frame_id_;
  bool use_imu_yaw_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SimpleOdometryNode>());
  rclcpp::shutdown();
  return 0;
}
