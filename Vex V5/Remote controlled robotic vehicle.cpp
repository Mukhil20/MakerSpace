#include "vex.h"
using namespace vex;

competition Competition;
brain Brain;
controller Controller1 = controller(primary);

motor LeftFront  = motor(PORT1, ratio18_1, false);
motor LeftBack   = motor(PORT2, ratio18_1, false);
motor RightFront = motor(PORT3, ratio18_1, true);
motor RightBack  = motor(PORT4, ratio18_1, true);

void usercontrol(void) {
    while (true) {
        int fwd  = Controller1.Axis3.position(); // left stick up/down
        int turn = Controller1.Axis1.position(); // left stick left/right

        int left  = fwd + turn;
        int right = fwd - turn;

        LeftFront.spin(forward, left, percent);
        LeftBack.spin(forward, left, percent);
        RightFront.spin(forward, right, percent);
        RightBack.spin(forward, right, percent);

        wait(20, msec);
    }
}

int main() {
    Competition.drivercontrol(usercontrol);
    while (true) wait(100, msec);
}
