"""
File: coder_setup.py
Purpose: This script defines functions for GUI automation on macOS using the pyautogui library.
         It includes a function to simulate key combinations (Cmd+I then Cmd+R), click,
         type, and press Enter, typically for interacting with an inspector tool.
         It also includes a function to type a formatted string at the current cursor position.
Key Functionality:
  - Defines `start_inspector_and_refresh()`: Simulates Cmd+I, Cmd+R, clicks,
    types "coder.mdc", and interacts with UI elements on macOS.
  - Defines `paste_formatted_string(text_to_paste: str)`: Formats the input string,
    copies it to the clipboard, and then pastes it at the current cursor position on macOS.
  - If not running on macOS, functions will print a message and not attempt
    to simulate key presses or mouse actions.
  - Includes basic examples of how to call these functions.
Important Notes & Context:
  - Requires the `pyautogui` and `pyperclip` libraries to be installed.
    You can install them by running: pip install pyautogui pyperclip
  - These scripts are intended for macOS only.
  - Ensure that the application you intend to interact with is in focus
    when these scripts/functions are run for the key presses and mouse actions to take effect.
"""
import pyautogui
import platform
import time
import pyperclip

def start_inspector_and_refresh():
    """
    Simulates pressing Cmd+I then Cmd+R on macOS.
    If not on macOS, it prints a message and does nothing.
    This is often used to open an inspector or a similar tool and then refresh it.
    Short delays are added before and after the hotkeys to ensure
    the commands have time to be processed by the OS.
    """
    if platform.system() != "Darwin":
        print("This script is intended for macOS only. No key presses will be simulated.")
        return

    try:
        time.sleep(5)  # Small delay to ensure focus or ireadiness

        pyautogui.keyDown('command')
        pyautogui.press('i')
        pyautogui.keyUp('command')
        time.sleep(0.5) # Delay for the first action to register

        pyautogui.keyDown('command')
        pyautogui.press('r')
        pyautogui.keyUp('command')

        time.sleep(0.5) # Small delay for the second action to register
        pyautogui.click(x=54, y=121) # Click at the specified coordinates
        time.sleep(0.2) # Small delay for the click to register
        pyautogui.click(x=31, y=120) # Click at the new specified coordinates
        time.sleep(0.2) # Small delay for the new click to register
        pyautogui.typewrite("tool_creator_server.py")
        time.sleep(0.5) # Small delay after typing
        pyautogui.click(x=121, y=168) # Click at specified coordinates instead of pressing Enter
        time.sleep(0.2) # Small delay after clicking
        pyautogui.click(x=270, y=169)
        pyautogui.click(x=31, y=120) # Click at the new specified coordinates
        time.sleep(0.2) # Small delay for the new click to register
        pyautogui.typewrite("coder.mdc")
        time.sleep(0.5) # Small delay after typing
        pyautogui.click(x=121, y=168) # Click at specified coordinates instead of pressing Enter
        pyautogui.click(x=270, y=169)
        pyautogui.keyDown('command')
        pyautogui.press('a')
        pyautogui.keyUp('command')
        pyautogui.press('delete')
    except Exception as e:
        print(f"An error occurred during key press simulation: {e}")
        print("Please ensure pyautogui is installed and configured correctly.")
        print("For some OS configurations, additional setup might be needed for pyautogui to control keyboard/mouse.")

def paste_formatted_string(text_to_paste: str):
    """
    Formats a given string and types it out at the current cursor position on macOS.
    A small delay is added before typing to allow for focus.

    Args:
        text_to_paste: The string to be formatted and typed.
    """
    if platform.system() != "Darwin":
        print("This script is intended for macOS only. No text will be typed.")
        return

    formatted_string = f"""
    You are an AI assistant tasked with creating and organizing tools within the server/tools directory.
    Your goal is to:
    1. Create new directories and tools as needed within server/tools
    2. Ensure proper imports and integration with tool_creator_server.py
    3. Verify all tools work correctly as part of the server

    Please follow these guidelines:
    - Only work within the server/tools directory structure
    - Import new tools into tool_creator_server.py
    - Test all tools to ensure they work as expected
    - DONT WORRY ABOUT TESTING THE TOOL, JUST BUILD IT AND MAKE SURE IT WORKS WITH THE SERVER dont about testing it
    - read me or anuthing else, just build the tool and make sure it works with the server
    - IMPORTANT: make sure to do all uv add for packages you wanna add make sure you do uv add (package name)
    - IMPORTANT: Do not run the file or tool just build it and make sure it works with the server
    - IMPORTANT: DO NOT MAKE TEST FILES OR TEST CODE, JUST BUILD THE TOOL AND MAKE SURE IT WORKS WITH THE SERVER
    Remember to:
    - Check for existing similar tools before creating new ones
    - Follow the established coding patterns and conventions
    - Ensure proper error handling and logging
    - Update documentation as needed
    - REMEMBER WHEN YOU ARE DONE USE THE RESTART SERVER MCP TO RESTART AFTER YOU ARE DONE CODING and if you start coding call the start coding tiool
    - whenever you start coding edit it to True, and when done edit it to False using the restart server mcp tool
    here is what you need to build:
    {text_to_paste}
    """
    
    try:
        time.sleep(0.5)  # Small delay to ensure focus or readiness
        pyperclip.copy(formatted_string) # Copy to clipboard
        pyautogui.hotkey('command', 'v') # Paste
        print(f"Successfully pasted string after copying to clipboard.")
        pyautogui.press('enter')
        
        # Move to the specified position
        target_position = (238, 940)  # User-specified position
        pyautogui.moveTo(target_position[0], target_position[1])
        print(f"Moved to position X={target_position[0]}, Y={target_position[1]}")
        
        # Click at the target position
        pyautogui.click()
        print(f"Clicked at position {pyautogui.position()}")
        
        # Press command+enter based on keep_going.txt content
        print("Starting to press Command+Enter every 2 seconds while keep_going.txt contains 'true'...")
        
        while True:
            try:
                with open('/Users/akshaym/Documents/hackathons/tests/dl/servers/keep_going.txt', 'r') as file:
                    content = file.read().strip().lower()
                    if content != 'true':
                        print(f"keep_going.txt contains '{content}', stopping Command+Enter sequence")
                        break
            except FileNotFoundError:
                print("keep_going.txt not found, creating with default 'true' value")
                with open('/Users/akshaym/Documents/hackathons/tests/dl/servers/keep_going.txt', 'w') as file:
                    file.write('true')
                # Initialize content since we just created the file
                content = 'true'
                    
            time.sleep(2)  # Wait for 2 seconds
            pyautogui.keyDown('command')
            pyautogui.press('enter')
            pyautogui.keyUp('command')
            print(f"Pressed Command+Enter, keep_going.txt = '{content}'")
        
        print("Completed Command+Enter sequence based on keep_going.txt")
        
        # After Command+Enter sequence stops, click at the specified coordinates
        time.sleep(1.0)  # Wait a second before additional clicks
        pyautogui.click(x=1288.0, y=810.3046875)
        print("Clicked at position X=1288.0, Y=810.3046875")
        
        time.sleep(2)  # Small delay between clicks
        pyautogui.click(x=1138.6953125, y=765.90625)
        print("Clicked at position X=1138.6953125, Y=765.90625")
        
        # Type the command and press enter
        time.sleep(0.5)  # Small delay before typing
        pyautogui.typewrite("uv run servers/tools_creator_server.py")
        print("Typed: uv run servers/tools_creator_server.py")
        pyautogui.press('enter')
        print("Pressed Enter to execute the command")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure pyautogui and pyperclip are installed and configured correctly.")

if __name__ == "__main__":
    start_inspector_and_refresh()
    paste_formatted_string("build a tool that creates a csv file if it doesnt exist and we can do crud operations on it")
