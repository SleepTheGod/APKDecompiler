from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import zipfile
import xml.etree.ElementTree as ET
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

# Ensure the upload and results directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

class APKDecompiler:
    def __init__(self, apk_path, output_dir):
        self.apk_path = apk_path
        self.output_dir = output_dir

    def extract_apk(self):
        """Extract the APK file into the output directory."""
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
                zip_ref.extractall(self.output_dir)
                print("Extraction complete. Files extracted:")
                print(zip_ref.namelist())  # Print the names of the files extracted
        except zipfile.BadZipFile:
            return "The uploaded file is not a valid APK."
        except Exception as e:
            return f"An error occurred during extraction: {e}"

    def parse_manifest(self):
        """Parse the AndroidManifest.xml file for application details."""
        manifest_path = os.path.join(self.output_dir, "AndroidManifest.xml")
        
        if not os.path.exists(manifest_path):
            return "AndroidManifest.xml not found in the extracted APK."
        
        if os.path.getsize(manifest_path) == 0:  # Check if the file is empty
            return "AndroidManifest.xml is empty."

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            # Extract basic application information
            package = root.get('package', 'N/A')
            version_code = root.get('android:versionCode', 'N/A')
            version_name = root.get('android:versionName', 'N/A')

            result = f"<h3>Package Information:</h3>"
            result += f"<p><strong>Package Name:</strong> {package}</p>"
            result += f"<p><strong>Version Code:</strong> {version_code}</p>"
            result += f"<p><strong>Version Name:</strong> {version_name}</p>"

            # Extract permissions
            permissions = root.findall("uses-permission")
            result += "<h3>Permissions:</h3><ul>"
            for perm in permissions:
                result += f"<li>{perm.get('{http://schemas.android.com/apk/res/android}name', 'N/A')}</li>"
            result += "</ul>"

            # Extract application components
            app = root.find("application")
            if app is not None:
                activities = app.findall("activity")
                result += "<h3>Activities:</h3><ul>"
                for activity in activities:
                    result += f"<li>{activity.get('{http://schemas.android.com/apk/res/android}name', 'N/A')}</li>"
                result += "</ul>"
            else:
                result += "<h3>No application components found.</h3>"

            return result

        except ET.ParseError as e:
            return f"Error parsing AndroidManifest.xml: {e}"
        except Exception as e:
            return f"An unexpected error occurred while parsing the manifest: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'apk_file' not in request.files:
            return redirect(request.url)
        file = request.files['apk_file']
        if file.filename == '':
            return redirect(request.url)

        apk_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(apk_path)

        # Decompile the APK
        output_dir = os.path.join(RESULT_FOLDER, file.filename.replace('.apk', ''))
        os.makedirs(output_dir, exist_ok=True)
        
        decompiler = APKDecompiler(apk_path, output_dir)
        extraction_result = decompiler.extract_apk()
        
        if extraction_result is not None:
            return render_template('result.html', manifest_info=extraction_result)

        manifest_info = decompiler.parse_manifest()

        return render_template('result.html', manifest_info=manifest_info)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
