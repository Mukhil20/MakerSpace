from xarm.wrapper import XArmAPI
import time

# ===== CONNECT =====
arm = XArmAPI("192.168.1.169")
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

print("Connected to Lite 6")

# ===== POSITIONS (edit these for your workspace) =====
PICK_X, PICK_Y, PICK_Z = 200, 0, 95  # Where the object is
PLACE_X, PLACE_Y, PLACE_Z = 300, 150, 95  # Where to drop it
SAFE_Z = 300  # Safe travel height


try:
    # Step 1 🟦 Move to safe height above pick position
    print("Moving above pick position...")
    arm.set_position(PICK_X, PICK_Y, SAFE_Z, wait=True)

    # Step 2 🟦 Move down to pick height
    print("Moving down to pick...")
    arm.set_position(PICK_X, PICK_Y, PICK_Z, wait=True)

    # Step 3 🟦 Turn on suction
    print("Picking object...")
    arm.set_vacuum_gripper(on=False)  # False = suction ON for Lite 6
    time.sleep(1)

    # Step 4 🟦 Lift back up to safe height
    print("Lifting...")
    arm.set_position(PICK_X, PICK_Y, SAFE_Z, wait=True)

    # Step 5 🟦 Move across to place position
    print("Moving to place position...")
    arm.set_position(PLACE_X, PLACE_Y, SAFE_Z, wait=True)

    # Step 6 🟦 Move down to place height
    print("Moving down to place height...")
    arm.set_position(PLACE_X, PLACE_Y, PLACE_Z, wait=True)

    # Step 7 🟦 Release
    print("Releasing object...")
    arm.set_vacuum_gripper(on=True)  # True = suction OFF for Lite 6
    time.sleep(1)

    # Step 8 🟦 Lift back up
    arm.set_position(PLACE_X, PLACE_Y, SAFE_Z, wait=True)

    print("Pick and place complete!")

except Exception as e:
    print(f"Error: {e}")

finally:
    arm.disconnect()
    print("Disconnected")
