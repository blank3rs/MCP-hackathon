"""
Purpose of the File:
This script continuously monitors the mouse cursor's position on the screen
and prints its pixel coordinates (x, y) and the color at that position
to the terminal every 3 seconds. It can also capture screenshots of specified regions.

Key Functionality:
- Uses the 'pynput' library to get mouse cursor coordinates.
- Uses the 'PIL' (Pillow) library to capture screen and get pixel colors.
- Uses the macOS built-in screencapture command with special flags for reliable foreground captures.
- Uses the 'time' library to introduce a delay between updates.
- Can capture and save screenshots of specific regions.
- Runs in an infinite loop until manually stopped (e.g., by Ctrl+C).

Important Notes & Context:
- The 'pynput' and 'Pillow' libraries must be installed for this script to run 
  (e.g., pip install pynput pillow).
- On some operating systems (like macOS), you may need to grant accessibility
  permissions to the terminal or IDE running this script for it to correctly
  read mouse coordinates and capture screens. If you see (0,0) or no output, check permissions.
- For macOS, ensure Terminal has Screen Recording permissions in System Settings > Privacy & Security.
"""
import time
import os
import subprocess
from datetime import datetime
from pynput import mouse
from PIL import ImageGrab, Image

def get_mouse_position():
    """Gets the current mouse cursor position."""
    mouse_controller = mouse.Controller()
    return mouse_controller.position

def get_pixel_color(x, y):
    """Gets the color of the pixel at the specified coordinates."""
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color

def capture_region(x1, y1, x2, y2, filename=None, app_name=None):
    """
    Captures a screenshot of the region defined by two points (x1,y1) and (x2,y2)
    using macOS native screencapture command with special flags for foreground capture.
    
    Args:
        x1, y1: Coordinates of the first point (top-left)
        x2, y2: Coordinates of the second point (bottom-right)
        filename: Optional filename to save the screenshot. If None, a timestamp-based name will be used.
        app_name: Optional name of the app to bring to the foreground before capturing
        
    Returns:
        The path to the saved screenshot file.
    """
    # Ensure correct ordering of coordinates
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    # Calculate width and height
    width = right - left
    height = bottom - top
    
    # Create filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    # Make sure we're getting the absolute path
    abs_filepath = os.path.abspath(filename)
    
    # Use macOS built-in screencapture for reliable captures
    try:
        # Bring the specific app to the foreground if specified
        if app_name:
            subprocess.run([
                "osascript",
                "-e",
                f'tell application "{app_name}" to activate'
            ])
            time.sleep(0.5)  # Allow time for app to come to foreground
        
        # Focus all applications to ensure proper foreground rendering
        subprocess.run([
            "osascript", 
            "-e", 
            'tell application "System Events" to set frontmost of every process whose frontmost is true to true'
        ])
        time.sleep(0.5)  # Allow system time to render the foreground properly
        
        # Take the screenshot of the specified region with compositing flag
        subprocess.run([
            "screencapture",
            "-x",  # Silent mode (no sound)
            "-C",  # Include window compositing (fixes black/empty screen issues)
            "-R", f"{left},{top},{width},{height}",  # Exact region to capture
            abs_filepath
        ])
        
        print(f"Screenshot saved as: {abs_filepath}")
        return abs_filepath
    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        return None

def interactive_capture_region(filename=None):
    """
    Prompts the user to select a region of the screen interactively
    using macOS native screencapture.
    
    Args:
        filename: Optional filename to save the screenshot. If None, a timestamp-based name will be used.
        
    Returns:
        The path to the saved screenshot file.
    """
    # Create filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    # Make sure we're getting the absolute path
    abs_filepath = os.path.abspath(filename)
    
    try:
        print("Please select an area of the screen when the selection tool appears...")
        # Using the interactive mode of screencapture with compositing flag
        subprocess.run([
            "screencapture",
            "-i",  # Interactive mode (user selects region)
            "-C",  # Include window compositing 
            abs_filepath
        ])
        
        print(f"Screenshot saved as: {abs_filepath}")
        return abs_filepath
    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        return None

def check_screen_permissions():
    """
    Prints instructions for ensuring proper screen recording permissions.
    """
    print("\nIMPORTANT: For proper foreground app capture, ensure:")
    print("1. Terminal has Screen Recording permissions in System Settings > Privacy & Security > Screen Recording")
    print("2. If issues persist, run in Terminal: tccutil reset ScreenCapture")
    print("   This will reset permissions and prompt you to grant them again.\n")

if __name__ == "__main__":
    print("Starting mouse position and color tracker... Press Ctrl+C to stop.")
    try:
        while True:
            x, y = get_mouse_position()
            color = get_pixel_color(x, y)
            print(f"Cursor position: X={x}, Y={y} | Color (RGB): {color}")
            time.sleep(1)  # Reduced from 3 seconds to 1 second for more responsive updates
    except KeyboardInterrupt:
        print("\nMouse position and color tracker stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure 'pynput' and 'pillow' are installed and accessibility permissions are granted if needed.")

