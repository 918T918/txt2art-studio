# Txt2Art Studio

A simple cross-platform GUI application to generate ASCII art from text using various fonts, powered by `pyfiglet`.

## Features

* Generate ASCII art from text input.
* Choose from a wide variety of available `pyfiglet` fonts.
* Adjust the output width.
* Real-time preview updates as you type or change settings.
* Copy generated art to the clipboard (with code formatting options).
* Save generated art to a text file.
* Clear input/output areas easily.
* Light/Dark theme toggle.
* Cross-platform (tested on Linux, should work on Windows and macOS).

## Installation

1.  **Python 3:** Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/) if needed. Most Linux distributions and recent macOS versions come with Python 3. Check by opening your terminal or command prompt and typing:
    ```bash
    python3 --version
    # or on some systems (like Windows)
    python --version
    ```

2.  **Dependencies:** This tool requires the `pyfiglet` library. Install it using pip:
    ```bash
    # Linux/macOS/WSL
    pip3 install pyfiglet

    # Windows (native)
    pip install pyfiglet
    ```

3.  **Get the Code:** Clone this repository to download the main application script (`txt2art.py`) and the optional setup script (`txt2art_setup.sh`):
    ```bash
    git clone [https://github.com/918T918/txt2art-studio.git](https://github.com/918T918/txt2art-studio.git)
    # Replace 918T918/txt2art-studio if your repo name is different
    cd txt2art-studio
    ```

## Usage (Running the GUI)

<<<<<<< HEAD
Navigate to the directory where you cloned the repository in your terminal or command prompt and run the main script using Python 3:

```bash
# Linux/macOS/WSL
python3 txt2art.py

# Windows (native)
python txt2art.py
# or sometimes just:
# py txt2art.py
This will launch the graphical user interface. Enter text, select a font, adjust the width, and the ASCII art will appear in the result area. Use the buttons to copy, save, or clear the output. Use the theme button at the bottom to toggle light/dark mode. Use the "Copy Format" dropdown to select how the art should be formatted when copied to the clipboard.

Notes for WSL (Windows Subsystem for Linux) Users
Running GUI applications like Txt2Art Studio from within WSL requires some setup to display the window on your Windows desktop.

WSL2 on Windows 11: This typically works out-of-the-box thanks to WSLg, which automatically handles GUI applications. You usually don't need any extra configuration.
WSL1 or WSL2 on Windows 10: You will likely need to install and run an X Server application on your Windows host (like VcXsrv or X410) and configure the DISPLAY environment variable within your WSL terminal before running the Python script. A common setting is:

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
# Run this in your WSL terminal *before* running the python script
(Refer to documentation for your specific X Server and WSL version for detailed setup).
Once the display is configured (or if using WSLg), the installation (pip3 install pyfiglet) and running (python3 txt2art.py) commands within WSL are the same as for standard Linux.

Optional: System-Wide Command (Linux/macOS/WSL)
If you want to run the GUI from anywhere in your terminal just by typing txt2art, you can use the provided setup script:

Navigate to the script's directory: Open your terminal and cd into the folder where you cloned the repository (the one containing txt2art.py and txt2art_setup.sh).


# Example: if you cloned into your home directory
cd ~/txt2art-studio
Make the setup script executable:


chmod +x txt2art_setup.sh
Run the setup script with sudo: This script will make txt2art.py executable and create the necessary symbolic link in /usr/local/bin.


sudo ./txt2art_setup.sh
Run: Now you should be able to open a new terminal window (or type rehash or hash -r in some shells) and simply type:


txt2art
to launch the application from anywhere.

<<<<<<< HEAD
