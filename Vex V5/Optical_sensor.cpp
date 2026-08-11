#include "vex.h"
using namespace vex;

brain Brain;
optical Optical1(PORT1);

int main() {
  Optical1.setLight(ledState::on);

  while(true) {
    double hue = Optical1.hue();
    int proximity = Optical1.proximity();

    printf("Hue: %.1f  Proximity: %d\n", hue, proximity);
    wait(100, msec);
  }
}
