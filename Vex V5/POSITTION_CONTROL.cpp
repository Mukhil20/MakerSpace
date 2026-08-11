#include "vex.h"
using namespace vex;

brain Brain;
motor Motor10(PORT10);

int main() {
  // Spin to 90 degrees and wait
  Motor10.spinToPosition(90, degrees, true);
  wait(1, seconds);

  // Spin to 180 degrees
  Motor10.spinToPosition(180, degrees, true);
  wait(1, seconds);

  // Return back to 0
  Motor10.spinToPosition(0, degrees, true);
}
