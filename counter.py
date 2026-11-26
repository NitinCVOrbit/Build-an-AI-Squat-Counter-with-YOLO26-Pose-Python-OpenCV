
# ============================================================
# SQUAT COUNTER
# ============================================================

def squat_counter(
    angle,
    down_angle,
    up_angle,
    stable_frames,
    state,
    up_frames,
    down_frames,
    count
):

    # Check whether the knee angle is below the DOWN threshold
    if angle < down_angle:

        # Increase the consecutive DOWN frame counter
        down_frames += 1

        # Reset the UP frame counter
        up_frames = 0

        # Example:
        # If stable_frames = 3:
        # Frame 1: Angle = 130 -> DOWN frames = 1
        # Frame 2: Angle = 125 -> DOWN frames = 2
        # Frame 3: Angle = 120 -> DOWN frames = 3
        # Now the DOWN position is confirmed.

        # Confirm DOWN position after consecutive stable frames
        if down_frames >= stable_frames:

            # Update the current state to DOWN
            state = "DOWN"

    # ========================================================
    # UP STATE DETECTION
    # ========================================================

    # Check whether the knee angle is above the UP threshold
    elif angle > up_angle:

        # Increase the consecutive UP frame counter
        up_frames += 1

        # Reset the DOWN frame counter
        down_frames = 0

        # Example:
        # If stable_frames = 3:
        # Frame 1: Angle = 170 -> UP frames = 1
        # Frame 2: Angle = 172 -> UP frames = 2
        # Frame 3: Angle = 175 -> UP frames = 3
        # Now the UP position is confirmed.

        # Confirm UP position after consecutive stable frames
        if up_frames >= stable_frames:

            # Count a squat only if the previous state was DOWN
            if state == "DOWN":

                # Increase the squat count by one
                count += 1

            # Update the current state to UP
            state = "UP"

    # ========================================================
    # INTERMEDIATE ANGLE
    # ========================================================

    # Execute when the angle is between DOWN and UP thresholds
    else:

        # Reset the consecutive UP frame counter
        up_frames = 0

        # Reset the consecutive DOWN frame counter
        down_frames = 0

        # Example:
        # If angle = 150:
        # It is neither DOWN (< 140) nor UP (> 165).
        # Therefore, both frame counters are reset.

    # ========================================================
    # RETURN VALUES
    # ========================================================

    # Return updated squat count, state, and frame counters
    return count, state, up_frames, down_frames



# In the simple method, we change the squat state immediately
# based on the detected knee angle.
#
# Example:#
# down_angle = 140
# up_angle = 165
#
# Frame 1: Angle = 130 -> State = DOWN -> Count = 0
# Frame 2: Angle = 135 -> State = DOWN -> Count = 0
# Frame 3: Angle = 168 -> State = UP   -> Count = 1
# Frame 4: Angle = 138 -> State = DOWN -> Count = 1
# Frame 5: Angle = 170 -> State = UP   -> Count = 2
# Frame 6: Angle = 132 -> State = DOWN -> Count = 2
# Frame 7: Angle = 175 -> State = UP   -> Count = 3
#
# Problem:
# The person has actually performed only ONE squat.
# However, the counter counts THREE squats.
#
# This happens because small fluctuations in YOLO keypoint
# detection cause the knee angle to change unexpectedly.


# ------------------------------------------------------------
# 2. IMPROVED METHOD (WITH STABLE_FRAMES)
# ------------------------------------------------------------

# To prevent false counting, we introduce stable_frames.
#
# stable_frames = 3
#
# Now, the knee angle must satisfy the threshold condition
# for THREE consecutive frames before changing the state.
#
# Example:
#
# Frame 1: Angle = 130 -> DOWN frames = 1 -> State = UP
# Frame 2: Angle = 125 -> DOWN frames = 2 -> State = UP
# Frame 3: Angle = 168 -> UP frames   = 1 -> State = UP
# Frame 4: Angle = 138 -> DOWN frames = 1 -> State = UP
# Frame 5: Angle = 170 -> UP frames   = 1 -> State = UP
# Frame 6: Angle = 132 -> DOWN frames = 1 -> State = UP
# Frame 7: Angle = 175 -> UP frames   = 1 -> State = UP
#
# Result:
# The DOWN or UP condition was never satisfied for three
# consecutive frames.
#
# Therefore, the squat state does not change and no false
# squat is counted.