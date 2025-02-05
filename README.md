Automatically logging in Wi-Fi
======================

This project automates the process of connecting to a Wi-Fi network that requires authentication via a login page (e.g., captive portal). The script logs in to the portal using user-provided credentials, simplifying the connection process for networks that require frequent authentication.

Features
--------

-   **Wi-Fi Network Connection**: Automatically connects to a specified Wi-Fi network.
-   **Web Portal Login**: Logs into a web portal (e.g., captive portal) using the provided credentials.
-   **Internet Availability Check**: Checks the availability of an internet connection before attempting to log in.
-   **Status URL Check**: Optionally checks a status URL to see if the user is already logged in before proceeding with the login process.
-   **Debug Mode**: Enables or disables browser headless mode for debugging purposes.
-   **Configuration File Creation**: The configuration file is created when the script is run if it does not already exist.

Requirements
------------

-   Python 3.7 or higher
-   Dependencies:
    -   `asyncio`
    -   `playwright` (for automating web browser actions)
    -   `subprocess` (for executing system commands)
    -   `socket` (for checking internet connectivity)
    -   `json` (for handling configuration files)

To install required Python dependencies, run:

`pip install playwright`

For Playwright to work, you must also install the necessary browser binaries:

`python -m playwright install`

Configuration
-------------

### Config File Creation

The script will automatically check if the configuration file (`wifi_config.json`) exists. If the file is missing, it will prompt the user to fill in the necessary information, and a new configuration file will be created.

Upon running the script for the first time, the following fields will be prompted for input:

1.  **Wi-Fi Network Name (SSID)**: The name of the Wi-Fi network you want to connect to (e.g., `Example_WIFI`).
2.  **Login Page URL**: The URL of the login page you need to access to authenticate (e.g., `http://192.168.1.1/login`).
3.  **Username**: The username for the login form (e.g., `user123`).
4.  **Password**: The password for the login form (e.g., `password123`).
5.  **Status URL (Optional)**: A URL that can be checked after login to verify if the login was successful (e.g., `http://192.168.1.1/status`). If not provided, the script will check if the internet connection is available instead.
6.  **Debug Mode**: A boolean flag to enable or disable browser debug mode. If enabled (`true`), the browser will run in non-headless mode (visible). If disabled (`false`), the browser will run in headless mode (background, invisible).

### Configuration File Example

If the configuration file is successfully created, it will be saved in the project directory as `wifi_config.json`. The content will look like this:

`{
  "target_ssid": "Example_WIFI",
  "login_page_url": "http://192.168.1.1/login",
  "username": "user123",
  "password": "password123",
  "status_url": "http://192.168.1.1/status",
  "debug_mode": true
}`

### Description of Each Configuration Field:

1.  **target_ssid** (Required): The name of the Wi-Fi network (SSID) that the script will connect to. Example: `Example_WIFI`.

2.  **login_page_url** (Required): The URL of the login page (usually a captive portal page) that requires the user to authenticate. Example: `http://192.168.1.1/login`.

3.  **username** (Required): The username for logging into the login page. Example: `user123`.

4.  **password** (Required): The password for logging into the login page. Example: `password123`.

5.  **status_url** (Optional): A URL that the script can check to verify whether the user is already logged in. If not provided, the script will instead check the internet connection. Example: `http://192.168.1.1/status`.

6.  **debug_mode** (Optional): A boolean flag indicating whether the browser should run in debug mode (visible).

    -   `true`: Browser runs in non-headless mode (you can see the browser window).
    -   `false`: Browser runs in headless mode (invisible, runs in the background).

Usage
-----

1.  **Run the Script**: After configuring your `wifi_config.json` file (or letting the script create it for you), you can run the script using the following command:

    `python wifi_login.py`

2.  **User Input**: If the configuration file is missing or incomplete, the script will prompt the user to fill in the required information (SSID, login URL, username, password, and optionally the status URL and debug mode).

3.  **Internet Check**: The script will first check if the internet is already available. If so, it will skip the login process.

4.  **Wi-Fi Connection**: If the device is not already connected to the specified Wi-Fi network, the script will attempt to connect to it.

5.  **Login Process**:

    -   The script will open a browser (with or without a UI, depending on `debug_mode`).
    -   It will navigate to the login page, where it will fill in the **username** and **password** fields and submit the form:

        `await page.fill('input[name="username"]', username)`
        `await page.fill('input[name="password"]', password)`
        `await page.click('button[type="submit"]')`

    -   After submitting, it checks whether the login was successful by either checking the `status_url` or verifying the internet connection.

6.  **Debug Mode**: If `debug_mode` is set to `true` in the configuration file, the browser will run in non-headless mode (i.e., you will see the browser window). If set to `false`, the browser will run in headless mode, meaning it will run in the background without a visible window.

Building an Executable with PyInstaller
---------------------------------------

You can build an executable of the script using **PyInstaller**, so you can run it without needing to have Python installed on the machine. This is particularly useful for distribution or running on machines without Python.

### Steps to Build the Executable:

1.  **Install PyInstaller**: First, you need to install **PyInstaller** if you haven't already. Run the following command:

    `pip install pyinstaller`

2.  **Create the Executable**: Once PyInstaller is installed, navigate to the directory containing `wifi_script.py` and run the following command to create a standalone executable:

    `pyinstaller --onefile --name WiFIAutoConnect --icon="favicon.ico" .\wifi_script.py`

    This will generate a `dist` directory containing the `WiFIAutoConnect` executable. The options used in this command are:

    -   `--onefile`: Creates a single executable file.
    -   `--name WiFIAutoConnect`: Specifies the name of the executable.
    -   `--icon="favicon.ico"`: Sets the icon for the executable (ensure you have a valid `.ico` file).
    -   `.\wifi_script.py`: The Python script to package.
3.  **Running the Executable**: After the build process is complete, you can find the executable in the `dist` directory. Run the following command to execute the program:

    `./dist/WiFIAutoConnect`

    This executable will behave the same way as the Python script but can be run on a machine that does not have Python installed.

Troubleshooting
---------------

-   **Wi-Fi Connection Issues**: If the script fails to connect to the Wi-Fi network, ensure that the SSID is correct and that the Wi-Fi network is available.
-   **Login Failures**: If the login process does not work as expected, make sure the login URL, username, and password are correct. You can also enable `debug_mode` to see the browser's actions.
-   **Internet Connection Problems**: If the script cannot detect the internet connection, ensure that the device has internet access and that the Wi-Fi network is connected properly.

License
-------

This project is licensed under the MIT License - see the <LICENSE> file for details.
# Auto-Login-Public-WIFI
