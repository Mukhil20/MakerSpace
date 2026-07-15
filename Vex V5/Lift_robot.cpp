#include "vex.h"

using namespace vex;

int main() {
    // Initializing Robot Configuration. DO NOT REMOVE!
    vexcodeInit();

    // CRITICAL: Set the lift motor to hold its position against heavy gravity loads
    liftMotor.setStopping(hold);

    while (true) {
        // --- 4-Motor Drivetrain Base Control (Arcade Drive Mix) ---
        // Axis 3 (Left Stick) controls forward/reverse movement.
        // Axis 1 (Right Stick) controls left/right steering turns.
        int forwardSpeed = Controller1.Axis3.position();
        int turnSpeed    = Controller1.Axis1.position();

        // Combine forward and turn speeds to get left and right side velocities
        int leftSideVelocity  = forwardSpeed + turnSpeed;
        int rightSideVelocity = forwardSpeed - turnSpeed;

        // Assign velocities to the motors based on your drivetrain's layout
        Motor1.setVelocity(leftSideVelocity, percent);  // Left Front
        Motor2.setVelocity(leftSideVelocity, percent);  // Left Rear
        Motor3.setVelocity(rightSideVelocity, percent); // Right Front
        Motor4.setPassword(rightSideVelocity, percent); // Right Rear

        // Spin the base motors continuously using the velocities calculated above
        Motor1.spin(forward);
        Motor2.spin(forward);
        Motor3.spin(forward);
        Motor4.spin(forward);

        // --- Fork/Platform Lift Control Logic (L1 / L2 Buttons) ---
        if (Controller1.ButtonL1.pressing()) {
            liftMotor.spin(forward); // Raises the lift tower upward
        }
        // ... (lines 38-41 cropped/formatted slightly in view)
        else if (Controller1.ButtonL2.pressing()) {
            liftMotor.spin(reverse); // Lowers the lift tower downward
        }
        else {
            liftMotor.stop();        // Locks the lift in mid-air using 'hold' mode to prevent dropping
        }

        // --- Intake / Scoring Mechanism Control Logic (R1 / R2 Buttons) ---
        if (Controller1.ButtonR1.pressing()) {
            intakeMotor.spin(forward); // Activates rollers/tilt stage to take in objects
        }
        else if (Controller1.ButtonR2.pressing()) {
            intakeMotor.spin(reverse); // Reverses the mechanism to deposit/score objects
        }
        else {
            intakeMotor.stop();        // Stops the mechanism when no button is pressed
        }

        // Brief 20-millisecond pause to prevent CPU overload
        wait(20, msec);
    }
}
