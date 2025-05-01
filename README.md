

# Txt2Art Studio

A simple cross-platform GUI application to generate ASCII art from text using various fonts, powered by `pyfiglet`.

![Screenshot Placeholder](https://placehold.co/600x400/EEE/333?text=App+Screenshot+Here)
*(Suggestion: Replace the placeholder URL above with an actual screenshot of your application after uploading it somewhere, like in your GitHub repo itself)*

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
    # Linux/macOS
    pip3 install pyfiglet

    # Windows
    pip install pyfiglet
    ```

3.  **Get the Code:** Clone or download the `txt2art_studio.py` script from this repository.
    ```bash
    git clone [https://github.com/YourUsername/txt2art-studio.git](https://github.com/YourUsername/txt2art-studio.git)
    # Replace YourUsername/txt2art-studio with your actual repo URL
    cd txt2art-studio
    ```

## Usage (Running the GUI)

Navigate to the directory where you saved `txt2art_studio.py` in your terminal or command prompt and run the script using Python 3:

```bash
# Linux/macOS
python3 txt2art_studio.py

# Windows
python txt2art_studio.py
# or sometimes just:
# py txt2art_studio.py
