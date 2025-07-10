"""
stepping_mode.py

Defines constants for stepper motor microstepping modes.
Each mode is represented as a tuple of (MS1, MS2, MS3) pin states.
These are used to configure the stepper driver for different resolutions.
"""

# Full step mode: lowest resolution, highest torque
FULL_STEP = (0, 0, 0)
# Half step mode: double the resolution
HALF_STEP = (1, 0, 0)
# Quarter step mode: 4x the resolution
QUARTER_STEP = (0, 1, 0)
# Eighth step mode: 8x the resolution
EIGHTH_STEP = (1, 1, 0)
# Sixteenth step mode: 16x the resolution, smoothest movement
SIXTEENTH_STEP = (1, 1, 1)
