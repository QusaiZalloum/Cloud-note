import os
import sys
import subprocess

# Check if required packages are installed
required_packages = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-bcrypt', 'psycopg2-binary', 'pytz']

def install_requirements():
    print("Installing required packages...")
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            return False
    return True

# Install requirements if needed
if not all(subprocess.call([sys.executable, '-m', 'pip', 'show', package], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL) == 0 
          for package in required_packages):
    if not install_requirements():
        print("Failed to install all required packages. Please install them manually.")
        sys.exit(1)

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from website import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Note Cloud application...")
    print("Access the application at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
