# APK Decompiler
APK Decompiler is a web application that allows users to upload Android APK files and decompile them to extract important information such as package details, versioning, and permissions from the AndroidManifest.xml file. This tool provides an easy-to-use interface for developers and enthusiasts to analyze APK files without requiring additional tools.

Features
Upload APK files directly through the web interface.
Decompiles APK files to extract package information, version codes, and permissions.
Displays the results in a user-friendly format.
No additional tools required for decompilation.
Technologies Used
Flask: A lightweight web framework for Python.
HTML/CSS: For the front-end user interface.
XML Parsing: For processing the AndroidManifest.xml file.
Installation
To run this project locally, follow these steps

Clone the repository:

git clone https://github.com/SleepTheGod/APKDecompiler/

Navigate to the project directory

cd APKDecompiler

Create a virtual environment (optional but recommended)

python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate

Install the required packages

pip install -r requirements.txt

Run the application

python app.py

Open your browser and navigate to

http://127.0.0.1:5000/

Usage
Click on the "Choose File" button to select an APK file from your device.
Click on the "Decompile APK" button to upload and decompile the file.
The results will be displayed on a new page, showing package information, version codes, and permissions.
Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to create a pull request.
