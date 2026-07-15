#include "vex_iq.h"
using namespace vex;

int main() {
    // Initializing Robot Configuration. DO NOT REMOVE!
    vexcodeInit();

    // Configure the Optical Sensor light to 50% to help see colors clearly
    OpticalSensor.setLight(open, 50, percent);

    while (true) {
        // --- TRAFFIC SIGNAL DETECTION ---
        // If the sensor sees RED, force the robot to stop (Red Light)
        if (OpticalSensor.color() == color::red) {
            // Stop the drivetrain immediately
            Drivetrain.stop(brake);

            // Optional: Print a warning to the IQ Brain screen
            Brain.Screen.clearScreen();
            Brain.Screen.setCursor(1, 1);
            Brain.Screen.print("RED LIGHT: STOP!");
        }
        // If the sensor sees GREEN (or anything safe), follow Controller commands
        else {
            // --- STANDARD DRIVE CONTROL ---
            // Axis A (Left Joystick) controls forward/reverse speed
            // Axis C (Right Joystick) controls left/right steering turn speed
            int forwardSpeed = Controller.AxisA.position();
            int turnSpeed    = Controller.AxisC.position();

            // Drive the smart chassis based on the joystick positions
            Drivetrain.drive(forward, forwardSpeed, percent);
            Drivetrain.turn(right, turnSpeed, percent);

            // Clear the brain screen when driving normally
            Brain.Screen.clearScreen();
            Brain.Screen.setCursor(1, 1);
            Brain.Screen.print("GREEN LIGHT: GO");
        }

        // Brief 20-millisecond pause to prevent CPU overload
        wait(20, msec);
    }
}
