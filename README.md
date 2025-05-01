# Txt2Art Studio

A simple cross-platform GUI application to generate ASCII art from text using various fonts, powered by `pyfiglet`.




## Features

* Generate ASCII art from text input.
* Choose from a wide variety of available `pyfiglet` fonts.
* Adjust the output width.
* Real-time preview updates as you type or change settings.
* Copy generated art to the clipboard.
* Save generated art to a text file.
* Clear input/output areas easily.
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

3.  **Get the Code:** Clone or download the `txt2art_studio.py` script from this repository.
    ```bash
    git clone [https://github.com/918T918/txt2art-studio.git](https://github.com/918T918/txt2art-studio.git)
    
    cd txt2art-studio
    ```

## Usage (Running the GUI)

Navigate to the directory where you saved `txt2art_studio.py` in your terminal or command prompt and run the script using Python 3:

```bash
# Linux/macOS/WSL
python3 txt2art_studio.py

# Windows (native)
python txt2art_studio.py
# or sometimes just:
# py txt2art_studio.py
This will launch the graphical user interface. Enter text, select a font, adjust the width, and the ASCII art will appear in the result area. Use the buttons to copy, save, or clear the output.

**Notes for WSL (Windows Subsystem for Linux) Users**
Running GUI applications like Txt2Art Studio from within WSL requires some setup to display the window on your Windows desktop.

WSL2 on Windows 11: This typically works out-of-the-box thanks to WSLg, which automatically handles GUI applications. You usually don't need any extra configuration.
WSL1 or WSL2 on Windows 10: You will likely need to install and run an X Server application on your Windows host (like VcXsrv or X410) and configure the DISPLAY environment variable within your WSL terminal before running the Python script. A common setting is:
Bash

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
# Run this in your WSL terminal *before* running the python script
(Refer to documentation for your specific X Server and WSL version for detailed setup).
Once the display is configured (or if using WSLg), the installation (pip3 install pyfiglet) and running (python3 txt2art_studio.py) commands within WSL are the same as for standard Linux.

Optional: System-Wide Command (Linux/macOS/WSL)
If you want to run the GUI from anywhere in your terminal just by typing txt2art, follow these steps:

Navigate to the script's directory: Open your terminal and cd into the folder containing txt2art_studio.py.

Bash

# Example: if the script is in the cloned repo directory
cd path/to/txt2art-studio
Make the script executable:

Bash

chmod +x txt2art_studio.py
(Make sure the very first line of the script is #!/usr/bin/env python3)

Create a symbolic link: Link the script (using its current path) to a directory in your system's PATH, like /usr/local/bin. This usually requires administrator privileges (sudo). Run this command from the directory containing the script:

Bash

sudo ln -s "$(pwd)/txt2art_studio.py" /usr/local/bin/txt2art
"$(pwd)/txt2art_studio.py" automatically gets the full path to the script in the current directory.
Run: Now you should be able to open a new terminal window (or type rehash or hash -r in some shells) and simply type:

Bash

txt2art
to launch the application from anywhere.

One-Liner (Run this from the directory containing the script after making it executable):

Bash

sudo ln -s "$(pwd)/txt2art_studio.py" /usr/local/bin/txt2art
(Note for Native Windows Users: Creating system-wide commands works differently on Windows. The easiest way is usually to add the script's directory to your system's PATH environment variable or create a shortcut.)
