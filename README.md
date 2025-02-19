# WINAPP-SN-Generator

## Description

WINAPP-SN-Generator is a Windows-based Serial Number Generator application with a modern dark-themed GUI built using CustomTkinter. The program allows users to input a **Project Name**, **Revision**, and **Finish Date** (in `DDMMYY` format) and optionally use today’s date via a checkbox. The serial number is generated by adding a random number (0–9999) to a hash computed from the concatenation of the Project Name and Revision. The final serial number is displayed in the format:

```
SN-XXXXXXDDMMYY
```

where `XXXXXX` is the final hash (formatted as at least 6 digits) and `DDMMYY` is the finish date. The generated serial number is shown in a copyable text field.

In addition, a QR code is generated from the serial number and displayed (resized to 150×150 pixels). Users can specify a save location for the output files. The layout includes:
- A dark-green **Generate SN** button (with a darker green hover effect) for generating the serial number.
- A **Save Location** input field (the path input) that spans the full width.
- Directly below the Save Location input, a row with two buttons: a **Browse** button on the left and a **Save All** button on the right.
- The **Save All** button is green (with a darker green hover effect).
- When saving, the filenames include the project name as a prefix.

## Features

- **Modern Dark-Themed GUI:** Built using CustomTkinter.
- **Input Fields:** For Project Name, Revision, and Finish Date. Includes a "Use current date" checkbox to auto-fill the finish date.
- **Serial Number Generation:** The serial number is computed by adding a random number to a hash of the Project Name and Revision, then appending the finish date. It is displayed in a copyable text field.
- **QR Code Generation:** A QR code (150×150 pixels) is generated from the serial number.
- **File Saving:** The Save All function saves three files (a text file, a PNG file, and a BMP file of the QR code) in the chosen directory. Each filename includes the project name as a prefix.
- **Responsive Buttons:** The **Generate SN** and **Save All** buttons use a darker green color that matches the dark theme and change to an even darker green when hovered over.
- **Save Location Management:** The Save Location input is accompanied by a **Browse** button for easy directory selection.

## Requirements

- Python 3.x
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/Pillow/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DvidMakesThings/WINAPP-SN-Generator.git
   cd WINAPP-SN-Generator
   ```
2. (Optional) Create and activate a virtual environment.
3. Install the required packages:
   ```bash
   pip install customtkinter qrcode pillow
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. In the GUI:
   - Enter the **Project Name**, **Revision**, and **Finish Date** (or check "Use current date" to auto-fill).
   - Click the **Generate SN** button to generate the serial number.
   - The generated serial number appears in a copyable text field.
   - A QR code based on the serial number is displayed.
   - The **Save Location** input field shows the current path by default.
   - Below the path input, use the **Browse** button to select a different directory if desired.
   - Click the **Save All** button to save three files (a text file, a PNG file, and a BMP file) with filenames that include the project name and serial number.
   
## Building a Standalone Executable

To build a standalone executable (without a console window) using PyInstaller and to include an icon (converted to ICO format), run:
```bash
pyinstaller --onefile --windowed --name SN-Gen --icon=ico.ico main.py
```

## License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback:
- **Email:** [s.dvid@hotmail.com](mailto:s.dvid@hotmail.com)
- **GitHub:** [DvidMakesThings](https://github.com/DvidMakesThings)
