#include "vex.h"

using namespace vex;

int main() {
    // Initializing Robot Configuration. DO NOT REMOVE!
    vexcodeInit();

    // Set the arm motor to hold its position when stopped
    armMotor.setStopping(hold);

    while (true) {
        // --- 4-Motor Drivetrain Logic (Arcade Drive Mix) ---
        // Motor1 and Motor2 share the same direction calculation
        int velocity1_2 = Controller1.Axis3.position() + Controller1.Axis1.position();
        // Motor3 and Motor4 share the same direction calculation
        int velocity3_4 = Controller1.Axis3.position() - Controller1.Axis1.position();

        Motor1.setVelocity(velocity1_2, percent);
        Motor2.setVelocity(velocity1_2, percent);
        Motor3.setVelocity(velocity3_4, percent);
        Motor4.setVelocity(velocity3_4, percent);

        Motor1.spin(forward);
        Motor2.spin(forward);
        Motor3.spin(forward);
        Motor4.spin(forward);

        // --- Arm Control Logic (L1 / L2) ---
        if (Controller1.ButtonL1.pressing()) {
            armMotor.spin(forward);
        }
        else if (Controller1.ButtonL2.pressing()) {
            armMotor.spin(reverse);
        }
        else {
            armMotor.stop();
        }

        // --- Claw Control Logic (R1 / R2) ---
        if (Controller1.ButtonR1.pressing()) {
            clawMotor.spin(forward);
        }
        else if (Controller1.ButtonR2.pressing()) {
            clawMotor.spin(reverse);
        }
        else {
            clawMotor.stop();
        }

        // Brief pause to prevent CPU hogging
        wait(20, msec);
    }
}
