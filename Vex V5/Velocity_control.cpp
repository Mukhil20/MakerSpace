#include "vex.h"

using namespace vex;

brain Brain;
motor Motor10(PORT10);

int main() {
  // Spin motor forward at 50% speed for 3 seconds
  Motor10.spin(forward, 50, percent);
  wait(3, seconds);
  Motor10.stop();
}
