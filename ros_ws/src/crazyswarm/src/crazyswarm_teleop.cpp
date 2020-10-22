#include <fstream>
#include <sstream>

#include <ros/ros.h>
#include <tf/transform_listener.h>

#include <sensor_msgs/Joy.h>
#include <std_srvs/Empty.h>

#include <crazyflie_driver/Takeoff.h>
#include <crazyflie_driver/Land.h>

namespace SaitekButtons {

    enum {
        Pink1,
        Pink2,
        Pink3,
        Orange4,
        Orange5,
        Pink6,
        Pink7,
        Pink8,
        Orange9,
        Orange10,
        Yellow11,
        Yellow12,
        Yellow13,
        Yellow14,
        Yellow15,
        Yellow16,
        Blue17,
        Blue18,
        Green19,
        Green20,
        Gray21,
        Black22,
        Black23,
        Black24,
        Scroll,
        ScrollUp,
        ScrollDn,
        Red,
        COUNT,
    };

}

class Manager
{
public:

    Manager()
        : m_subscribeJoy()
        , m_serviceEmergency()
        , m_serviceTakeoff()
        , m_serviceLand()
    {
        ros::NodeHandle nh;
        m_subscribeJoy = nh.subscribe("/joy", 1, &Manager::joyChanged, this);

        ROS_INFO("Wait for services...");

        ros::service::waitForService("/emergency");
        m_serviceEmergency = nh.serviceClient<std_srvs::Empty>("/emergency");
        ros::service::waitForService("/takeoff");
        m_serviceTakeoff = nh.serviceClient<crazyflie_driver::Takeoff>("/takeoff");
        ros::service::waitForService("/land");
        m_serviceLand = nh.serviceClient<crazyflie_driver::Land>("/land");

        ROS_INFO("Manager ready.");
    }

    ~Manager()
    {
    }

private:
    void joyChanged(
        const sensor_msgs::Joy::ConstPtr& msg)
    {
        static std::vector<int> lastButtonState(SaitekButtons::COUNT);

        if (msg->buttons.size() >= SaitekButtons::COUNT
            && lastButtonState.size() >= SaitekButtons::COUNT)
        {
            if (msg->buttons[SaitekButtons::Red] == 1 && lastButtonState[SaitekButtons::Red] == 0) {
                emergency();
            }
            if (msg->buttons[SaitekButtons::Black22] == 1 && lastButtonState[SaitekButtons::Black22] == 0) {
                takeoff();
            }
            if (msg->buttons[SaitekButtons::Black23] == 1 && lastButtonState[SaitekButtons::Black23] == 0) {
                land();
            }
        }

        lastButtonState = msg->buttons;
    }

    void emergency()
    {
        ROS_INFO("emergency requested...");
        std_srvs::Empty srv;
        m_serviceEmergency.call(srv);
        ROS_INFO("Done.");
    }

    void takeoff()
    {
        crazyflie_driver::Takeoff srv;
        srv.request.groupMask = 0;
        srv.request.height = 1.0;
        srv.request.duration = ros::Duration(2.0);
        m_serviceTakeoff.call(srv);
    }

    void land()
    {
        crazyflie_driver::Land srv;
        srv.request.groupMask = 0;
        srv.request.height = 0.05;
        srv.request.duration = ros::Duration(3.5);
        m_serviceLand.call(srv);
    }

private:
    ros::Subscriber m_subscribeJoy;

    ros::ServiceClient m_serviceEmergency;
    ros::ServiceClient m_serviceTakeoff;
    ros::ServiceClient m_serviceLand;
};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "manager");

  Manager manager;
  ros::spin();

  return 0;
}
