# WINAPP-SN-Generator

WINAPP-SN-Generator is a Windows-based Serial Number Generator application that features a modern, dark-themed GUI built with CustomTkinter. The application allows users to generate a serial number in the following format:

`SN-DDMMYY-XXXX`

Where:
- **DDMMYY** is a date string (which can be manually entered or automatically set to the current date).
- **XXXX** is a 4-digit hash generated from the concatenation of the project name and revision.

In addition to generating the serial number, the application also creates a QR code representing that serial number. It provides a “Save All” function that stores the serial number in a text file and the corresponding QR code as a PNG file in a user-specified directory.

## Features
- Modern GUI with a dark theme using CustomTkinter.
- Side-by-side input fields for Project Name and Revision.
- Finish Date input field (accepting date in DDMMYY format) with an option ("Use current date") to auto-fill the field with today’s date and disable manual editing.
- Save Location input to specify where the generated files will be stored.
- Serial number generation that combines the finish date with a 4-digit hash (derived from the project name and revision).
- QR code generation from the serial number, displayed in a fixed 150×150 pixel area with a transparent placeholder.
- Capability to build a standalone executable (SN-Gen.exe) using PyInstaller without any console window appearing.

## Requirements
- Python 3.x
- CustomTkinter
- qrcode
- Pillow

To install the required packages, run:
```sh
pip install -r requirements.txt
```

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/DvidMakesThings/WINAPP-SN-Generator.git
    cd WINAPP-SN-Generator
    ```
2. (Optional) Create and activate a virtual environment.
3. Install the dependencies as mentioned above.

## Usage
1. Run the application by executing:
    ```sh
    python main.py
    ```
2. Enter the required details:
    - Project Name and Revision (side by side).
    - Finish Date in DDMMYY format or check "Use current date" to auto-fill with today’s date.
    - Save Location for the output files.
3. Click the "Generate SN" button to generate the serial number and display the QR code.
4. Click the "Save All" button to save the serial number (in a text file) and the QR code (as a PNG image) in the specified directory.

### Building a Standalone Executable

To create a standalone executable named `SN-Gen.exe` without a console window, follow these steps:

1. **Install PyInstaller**: 
    ```sh
    pip install pyinstaller
    ```
2. **Run PyInstaller** in the project directory:
    ```sh
    pyinstaller --onefile --windowed --name SN-Gen main.py
    ```
3. Once the build process is complete, the executable (`SN-Gen.exe`) will be located in the `dist` folder.

### License

This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

### Contact

For questions or feedback, please contact:
- **Email**: s.dvid@hotmail.com
- **GitHub**: [DvidMakesThings](https://github.com/DvidMakesThings)