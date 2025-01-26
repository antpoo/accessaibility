from screeninfo import get_monitors

# Get display resolution dynamically
monitor = get_monitors()[0]  # Use the primary monitor
DISPLAY_WIDTH = monitor.width
DISPLAY_HEIGHT = monitor.height

# Set a keybind to close the program
EXIT_KEY = 'esc'

SMOOTHING_FACTOR = 0.5  # The closer to 1, the smoother the movement
smoothed_x, smoothed_y = None, None
