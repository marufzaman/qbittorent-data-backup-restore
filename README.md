# qBittorrent Data Backup and Restore (Windows Only)

---

## Overview

This tool offers a straightforward GUI for backing up and restoring qBittorrent data on Windows systems. Built with Python and `tkinter`, it provides an intuitive interface for managing your qBittorrent data, complete with detailed logging to track progress and errors.

---

## Features

- **Backup**: Easily create zip backups of both local and roaming qBittorrent data.
- **Restore**: Restore your qBittorrent data from previously created backups.
- **GUI**: User-friendly graphical interface for effortless operation.
- **Logging**: Comprehensive logs to monitor the backup and restore processes.

---

## Requirements

- Python 3.12.6 or later
- `Pillow` for image handling
- `tkinter` for the graphical interface

---

## Installation

1. **Clone the Repository**:
    ```powershell
    git clone https://github.com/marufzaman/qbittorent-data-backup-restore.git
    ```

2. **Navigate to the Project Directory**:
    ```powershell
    cd qbittorent-data-backup-restore
    ```

3. **Create and Activate a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

4. **Install Required Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

---

## Usage

1. **Run the Script**:
    ```powershell
    python qbittorent_Backup_and_Restore.py
    ```

2. **Interact with the GUI** to perform backup and restore operations.

---

## Creating an Executable

To generate a standalone executable from this script, follow these steps:

1. **Install PyInstaller**:
    ```powershell
    pip install pyinstaller
    ```

2. **Prepare UPX (Optional)**:
    UPX (Ultimate Packer for eXecutables) compresses the executable to reduce its size. Download UPX from [here](https://upx.github.io/), extract the archive, and note the directory path.

3. **Create the Executable**:
    Use one of the following commands based on your needs:

    - **Basic Command**: Creates a simple executable without compression or custom icon.
      ```powershell
      pyinstaller --onefile qbittorent_Backup_and_Restore.py
      ```

    - **With Icon**: Adds a custom icon to the executable.
      ```powershell
      pyinstaller --onefile --icon="backup_logo.png" qbittorent_Backup_and_Restore.py
      ```

    - **No Console**: For GUI applications, suppresses the console window.
      ```powershell
      pyinstaller --onefile --noconsole --icon="backup_logo.png" qbittorent_Backup_and_Restore.py
      ```

    - **With UPX Compression**: Compresses the executable using UPX. Replace `"path-to-upx-win64"` with your UPX directory.
      ```powershell
      pyinstaller --onefile --noconsole --icon="backup_logo.png" --upx-dir "path-to-upx-win64" qbittorent_Backup_and_Restore.py
      ```

    - **With Debugging**: Includes debugging information if you encounter issues.
      ```powershell
      pyinstaller --onefile --noconsole --icon="backup_logo.png" --debug all qbittorent_Backup_and_Restore.py
      ```

4. **Locate the Executable**:
    The executable will be found in the `dist` folder within your project directory.

5. **Troubleshooting**:
    Ensure all required files are in their correct locations and review the PyInstaller logs for any errors if the executable does not function as expected.

### Explanation of PyInstaller Commands

- `--onefile`: Packages everything into a single executable file.
- `--icon="backup_logo.png"`: Sets a custom icon for the executable.
- `--noconsole`: Hides the console window (useful for GUI applications).
- `--upx-dir "path-to-upx-win64"`: Specifies the path to UPX for compression.
- `--debug all`: Adds debugging information for troubleshooting.

---

## GUI Controls

- **Backup qBittorrent**: Initiates backup of local and roaming qBittorrent data.
- **Restore qBittorrent**: Restores qBittorrent data from backups.
- **Log Area**: Displays logs for operations and errors.

---

## Future Plans

An OS-independent version of this tool is in development. Contributions to help create this version or support other operating systems are warmly welcomed!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Your contributions are encouraged! If you have suggestions, bug reports, or wish to assist with the OS-independent version, please submit issues or pull requests.

---

## Contact

For any inquiries or feedback, please reach out to [A. M. Almarufuzzaman](mailto:marufzaman05@gmail.com).

---