import cv2
import numpy as np
import pyrealsense2 as rs

# ===== CAMERA SETUP =====
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# ===== HSV COLOR RANGES =====
# Tune these if needed (lighting matters!)
color_ranges = {
    "yellow": ((20, 100, 100), (35, 255, 255)),
    "orange": ((10, 100, 100), (20, 255, 255)),
    "green": ((40, 70, 70), (80, 255, 255)),
    "purple": ((125, 70, 70), (155, 255, 255)),
}

# Colors for drawing (BGR)
draw_colors = {
    "yellow": (0, 255, 255),
    "orange": (0, 165, 255),
    "green": (0, 255, 0),
    "purple": (255, 0, 255),
}

def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    output = frame.copy()
    
    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        
        mask = cv2.inRange(hsv, lower, upper)
        
        # Remove noise
        mask = cv2.medianBlur(mask, 5)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            if area > 500: # filter small noise
                x, y, w, h = cv2.boundingRect(cnt)
                
                cx = x + w // 2
                cy = y + h // 2
                
                # Draw box
                cv2.rectangle(output, (x, y), (x+w, y+h), draw_colors[color_name], 2)
                
                # Label
                cv2.putText(output, color_name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            draw_colors[color_name], 2)
                
                # Center point
                cv2.circle(output, (cx, cy), 5, (255, 255, 255), -1)
                
    return output

# ===== MAIN LOOP =====
try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        if not color_frame:
            continue
            
        frame = np.asanyarray(color_frame.get_data())
        
        result = detect_colors(frame)
        
        cv2.imshow("Color Detection", result)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
