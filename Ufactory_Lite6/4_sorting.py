import cv2
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO
from xarm.wrapper import XArmAPI
from simple_pid import PID
import time

# ===== CONFIG =====
YOLO_MODEL = "C:/Users/mukhi/Documents/ufactory_arm/best.pt"
FIXED_Z = 250
ROBOT_IP = "192.168.1.169"
DETECT_XYZ = [200, 0, 300]

FRAME_W, FRAME_H = 640, 480
CX, CY = FRAME_W // 2, FRAME_H // 2
THRESH = 8

# ===== INITIALIZATION =====
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

model = YOLO(YOLO_MODEL)
model.to("cpu")

arm = XArmAPI(ROBOT_IP)
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

# ===== PID =====
pid_x = PID(0.2, 0.0, 0.0, setpoint=0)
pid_y = PID(0.2, 0.0, 0.0, setpoint=0)
pid_x.output_limits = (-200, 200)
pid_y.output_limits = (-200, 200)

# ===== HELPER =====
def find_closest_box(detections, prev_u, prev_v, target_class):
    min_dist = float("inf")
    best_box = None

    for box in detections:
        cls = int(box.cls.item())
        cls_name = model.names[cls]

        if cls_name != target_class:
            continue

        xyxy = box.xyxy[0].cpu().numpy()
        u = int((xyxy[0] + xyxy[2]) / 2)
        v = int((xyxy[1] + xyxy[3]) / 2)

        dist = (u - prev_u)**2 + (v - prev_v)**2

        if dist < min_dist:
            min_dist = dist
            best_box = box

    return best_box

# ===== MAIN =====
def sort_all_objects():
    picked_count = 0
    class_counts = {}

    current_class = None
    current_u, current_v = None, None

    drop_zones = {
        "yellow": (70.2, 216.6),
        "orange": (160.8, 338.5),
        "green": (232, 279.3),
        "purple": (8, 338.5),
    }

    timeout_no_detections = 5
    last_seen_time = time.time()

    try:
        while True:
            arm.set_position(*DETECT_XYZ, wait=True)
            arm.set_vacuum_gripper(on=True)

            task_active = True
            found = False

            while task_active:
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())

                results = model(color_image, verbose=False)

                if results[0].boxes is None:
                    detections = []
                else:
                    detections = results[0].boxes

                # No detections
                if len(detections) == 0:
                    if time.time() - last_seen_time > timeout_no_detections:
                        print("[INFO] No objects left")
                        task_active = False
                        break
                    continue
                else:
                    last_seen_time = time.time()

                # ===== LOCK TARGET =====
                if current_class is None:
                    box = detections[0]

                    current_class = model.names[int(box.cls.item())]

                    xyxy = box.xyxy[0].cpu().numpy()
                    current_u = int((xyxy[0] + xyxy[2]) / 2)
                    current_v = int((xyxy[1] + xyxy[3]) / 2)

                    print(f"[INFO] Locked: {current_class}")

                # ===== TRACK TARGET =====
                box = find_closest_box(detections, current_u, current_v, current_class)

                if box is None:
                    print("[INFO] Lost target, relocking...")
                    current_class = None
                    continue

                xyxy = box.xyxy[0].cpu().numpy()

                u = int((xyxy[0] + xyxy[2]) / 2)
                v = int((xyxy[1] + xyxy[3]) / 2)

                current_u, current_v = u, v

                err_x = u - CX
                err_y = v - CY

                # ===== PICK =====
                if abs(err_x) < THRESH and abs(err_y) < THRESH:
                    print(f"[INFO] Picking {current_class}")

                    _, pose = arm.get_position(is_radian=False)
                    base_x, base_y, base_z = pose[:3]

                    target_x = base_x + 63
                    target_y = base_y + 35

                    arm.set_position(target_x, target_y, base_z, wait=True)
                    arm.set_position(target_x, target_y, 95, wait=True)

                    arm.set_vacuum_gripper(on=False)
                    time.sleep(2)

                    arm.set_position(target_x, target_y, 250, wait=True)

                    drop_x, drop_y = drop_zones.get(current_class, (150, 150))

                    arm.set_position(drop_x, drop_y, 250, wait=True)
                    arm.set_position(drop_x, drop_y, 130, wait=True)

                    arm.set_vacuum_gripper(on=True)
                    time.sleep(1)

                    arm.set_position(*DETECT_XYZ, wait=True)

                    picked_count += 1
                    class_counts[current_class] = class_counts.get(current_class, 0) + 1

                    print(f"[SUCCESS] Picked {current_class} (Total {picked_count})")

                    found = True
                    task_active = False
                    current_class = None

                else:
                    # ===== PID MOVE =====
                    delta_y = pid_x(err_x)
                    delta_x = pid_y(err_y)

                    _, pose = arm.get_position(is_radian=False)
                    base_x, base_y, _ = pose[:3]

                    arm.set_position(
                        base_x + delta_x,
                        base_y + delta_y,
                        FIXED_Z,
                        wait=False
                    )

                # Display
                cv2.circle(color_image, (u, v), 5, (0, 255, 0), -1)
                cv2.circle(color_image, (CX, CY), 5, (0, 0, 255), -1)
                cv2.imshow("Detect", color_image)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    task_active = False
                    break

            if not found:
                break

    except KeyboardInterrupt:
        print("[INFO] Interrupted")
    finally:
        cv2.destroyAllWindows()
        print(f"\n[FINAL] Sorted {picked_count} objects: {class_counts}")
        return picked_count, class_counts


if __name__ == "__main__":
    print("=" * 50)
    print("ROBOT SORTING PROGRAM")
    print("=" * 50)

    try:
        count, classes = sort_all_objects()
        print(f"\nDone. Picked {count} objects")
        print(classes)
    finally:
        pipeline.stop()
        arm.disconnect()
        print("[INFO] Cleanup done")