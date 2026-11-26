
import cv2
import numpy as np


# ============================================================
# CALCULATE ANGLE ----- Dot Product Method (Vector Method)
# ============================================================

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    denominator = (
        np.linalg.norm(ba) *
        np.linalg.norm(bc)
        + 1e-7
    )

    cosine_angle = np.dot(ba, bc) / denominator

    cosine_angle = np.clip(
        cosine_angle,
        -1.0,
        1.0
    )

    angle = np.degrees(
        np.arccos(cosine_angle)
    )

    return angle


# ============================================================
# CALCULATE BOTH KNEE ANGLES
# ============================================================

def calculate_squat_angle(person, keypoints):

    lh = person[keypoints["LEFT_HIP"]]
    rh = person[keypoints["RIGHT_HIP"]]

    lk = person[keypoints["LEFT_KNEE"]]
    rk = person[keypoints["RIGHT_KNEE"]]

    la = person[keypoints["LEFT_ANKLE"]]
    ra = person[keypoints["RIGHT_ANKLE"]]

    # ========================================================
    # LEFT KNEE ANGLE
    # ========================================================

    left_angle = calculate_angle(
        lh,
        lk,
        la
    )

    # ========================================================
    # RIGHT KNEE ANGLE
    # ========================================================

    right_angle = calculate_angle(
        rh,
        rk,
        ra
    )

    # ========================================================
    # AVERAGE KNEE ANGLE
    # ========================================================

    average_angle = (
        left_angle + right_angle
    ) / 2

    return left_angle, right_angle, average_angle


# Calculate the average of both knee angles.
# During a squat, both knees bend together,
# so we use one angle to represent the squat movement.
#
# Example:
# Left  = 105 degrees
# Right = 110 degrees
# Average = (105 + 110) / 2 = 107.5 degrees
#
# The average reduces small differences caused
# by pose detection.
