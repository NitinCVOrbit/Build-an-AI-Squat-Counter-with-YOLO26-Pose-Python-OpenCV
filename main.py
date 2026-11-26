
import cv2
from ultralytics import YOLO
from pose_utils import calculate_squat_angle
from counter import squat_counter
from visualizer import draw_angle, draw_info_panel


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading YOLO Pose model...")

    model = YOLO("yolo26n-pose.pt")

    # ========================================================
    # KEYPOINT MAPPING
    # ========================================================

    keypoints = {
        "LEFT_HIP": 11,
        "RIGHT_HIP": 12,
        "LEFT_KNEE": 13,
        "RIGHT_KNEE": 14,
        "LEFT_ANKLE": 15,
        "RIGHT_ANKLE": 16
    }

    # ========================================================
    # OPEN VIDEO
    # ========================================================

    cap = cv2.VideoCapture("input/01.mp4")

    if not cap.isOpened():
        print("ERROR: Could not open video.")
        return

    # ========================================================
    # COUNTER SETTINGS
    # ========================================================

    # Define the knee angle threshold for detecting the downward squat position
    down_angle = 140

    # Define the knee angle threshold for detecting the upward standing position
    up_angle = 165

    # Number of consecutive frames required to confirm a stable movement state
    stable_frames = 3

    # Initialize the initial squat state as standing (UP)
    state = "UP"

    # Initialize the counter for consecutive frames in the UP state
    up_frames = 0

    # Initialize the counter for consecutive frames in the DOWN state
    down_frames = 0

    # Initialize the total number of completed squats
    count = 0

    # ========================================================
    # PROCESS VIDEO
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280,720))

        # ====================================================
        # YOLO POSE
        # ====================================================

        # Run YOLO pose detection on the current video frame
        results = model(
            frame,              # Input frame on which pose detection will be performed
            conf=0.5,           # Set the minimum confidence threshold to 0.5 (50%)
            classes=[0],        # Detect only class 0, which represents a person
            verbose=False       # Disable detailed console output during inference
        )

        annotated_frame = frame.copy()

        # ====================================================
        # PERSON DETECTION
        # ====================================================

        if len(results) > 0:

            result = results[0]

            if result.keypoints is not None:

                keypoints_data = result.keypoints.data.cpu().numpy()

                if len(keypoints_data) > 0:

                    # ========================================
                    # FIRST PERSON
                    # ========================================

                    person = keypoints_data[0]

                    # ========================================
                    # CALCULATE SQUAT ANGLES
                    # ========================================

                    left_angle, right_angle, average_angle = calculate_squat_angle(
                        person,
                        keypoints
                    )

                    # ========================================
                    # UPDATE SQUAT COUNTER
                    # ========================================

                    count, state, up_frames, down_frames = squat_counter(
                        average_angle,
                        down_angle,
                        up_angle,
                        stable_frames,
                        state,
                        up_frames,
                        down_frames,
                        count
                    )

                    # ========================================
                    # YOLO POSE DRAWING
                    # ========================================

                    annotated_frame = result.plot()

                    # ========================================
                    # DRAW LEFT KNEE ANGLE
                    # ========================================

                    left_knee = person[13]

                    draw_angle(
                        annotated_frame,
                        left_knee,
                        left_angle
                    )

                    # ========================================
                    # DRAW RIGHT KNEE ANGLE
                    # ========================================

                    right_knee = person[14]

                    draw_angle(
                        annotated_frame,
                        right_knee,
                        right_angle
                    )

                    # ========================================
                    # INFORMATION PANEL
                    # ========================================

                    annotated_frame = draw_info_panel(
                        annotated_frame,
                        count,
                        state,
                        average_angle
                    )

        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "AI Squat Counter",
            annotated_frame
        )

        # ====================================================
        # QUIT
        # ====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ========================================================
    # RELEASE
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 50)
    print("PROCESSING COMPLETE")
    print("=" * 50)
    print(f"Total Squats: {count}")
    print("Output Video: output/squat_output.mp4")
    print("=" * 50)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()
