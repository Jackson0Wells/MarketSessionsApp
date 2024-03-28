### Market Sessions App

This application, **Market_sessions.py**, is a Python script that utilizes the Tkinter library to create a graphical user interface (GUI) for displaying information about different market sessions in the financial markets.

![image3](https://github.com/Jackson0Wells/MarketSessionsApp/assets/165251968/2891b806-0b0e-4f4e-8b76-594588f1e439)
![image2](https://github.com/Jackson0Wells/MarketSessionsApp/assets/165251968/caadb44d-0401-4c61-919d-3e13b7016cd8)
![image1](https://github.com/Jackson0Wells/MarketSessionsApp/assets/165251968/b80b0012-dda2-48f2-a2d1-5a2158178da5)


### Installation Guide

1. **Clone the Repository:**
   Clone or download the repository containing the Market Sessions App script.

2. **Install Python:**
   If you haven't already, ensure that Python is installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

3. **Install Dependencies:**
   Open a terminal or command prompt. Then, run the following command to install the required dependencies:
   ```sh
   pip install pillow
   ```

   - **Pillow:** This library is required for image processing tasks within the application. It allows the application to handle image files efficiently.

4. **Run the Script:**
   After installing the dependencies, you can run the Market Sessions App script by executing the following command in the terminal or command prompt:
   ```sh
   python Market_sessions.py
   ```

   This command will execute the script and launch the Market Sessions App GUI.

### Building the Market Sessions App without Terminal

If you prefer not to use the terminal to build the app, you can build it using PyInstaller directly.

1. **Install PyInstaller (if not already installed):**
   PyInstaller is a tool used to convert Python scripts into standalone executables. If you haven't installed PyInstaller yet, you can do so using pip:
   ```sh
   pip install pyinstaller
   ```

2. **Run PyInstaller to Build the App:**
   Once PyInstaller is installed, navigate to the directory containing the **Market_sessions.py** script using your file explorer. Then, follow these steps:

   - **Step 1:** Hold down the `Shift` key on your keyboard and right-click in the folder containing the script.
   - **Step 2:** From the context menu that appears, select "Open PowerShell window here" or "Open command window here," depending on your system.
   - **Step 3:** In the PowerShell or command window, run the following command to build the Market Sessions App without opening a terminal/console window:
     ```sh
     pyinstaller --onefile --noconsole Market_sessions.py
     ```

     - **--onefile:** This flag tells PyInstaller to bundle the Python script and its dependencies into a single executable file.
     - **--noconsole:** This flag ensures that the built executable does not open a terminal/console window when launched.

   This command will bundle the Python script and its dependencies into a standalone executable file without opening a terminal window when the app is launched.

3. **Find the Executable:**
   After PyInstaller has finished building the app, you can find the executable file in the `dist` directory within the project directory. The executable file will have the same name as your Python script with an added extension (e.g., `Market_sessions.exe` on Windows).

4. **Run the Executable:**
   You can run the executable file directly from your file explorer by double-clicking on it. This will launch the Market Sessions App without the need for Python or any additional dependencies.

### Additional Notes:

- PyInstaller may generate additional files and folders during the build process. These are necessary for the executable to run correctly and can usually be ignored.

- If you encounter any errors during the build process, make sure to check the PyInstaller documentation and troubleshoot accordingly.

- Remember to distribute the executable file along with any required assets (such as image files) when sharing or deploying the Market Sessions App.

### Showcase


https://github.com/Jackson0Wells/MarketSessionsApp/assets/165251968/42751ba9-a52f-49d9-91c8-dc86ca14b34c
https://www.youtube.com/watch?v=5B19-6fUQoE

## Support Development

If you find this project useful and would like to support further development, you can donate Bitcoin to the following address:

Bitcoin Address: `17Uv9ZgoKFXdi18PNf5UighASk53KMjzxp`

Your contributions will be greatly appreciated and will help in maintaining and improving this project. Thank you for your support!

