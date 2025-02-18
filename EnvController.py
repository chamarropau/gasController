import os
import subprocess
import sys
import venv
import json
from colorama import Fore, Style
from pkg_resources import get_distribution, parse_version
from termcolor import colored

class EnvironmentController:
    def __init__(self, env_name="SoftwareGasControl"):
        self.env_name = env_name
        self.env_path = os.path.join(os.getcwd(), self.env_name)
        self.dependencies = [
            "numpy", "pandas", "pyqtgraph", "pint", "setuptools_scm",
            "propar", "PyQt5", "PyQt5_sip", "pyserial", "PyVISA", "termcolor", "colorama",
            "tqdm", "pymeasure", "openpyxl", "pyvisa-py"
        ]

    def upgrade_pip(self, pip_path):        
        print(f"{colored('[INFO]', 'yellow')} UPGRADING PIP...")

        try:
            subprocess.check_call([pip_path, 'install', '--upgrade', 'pip'])
            print(f"{colored('[STATUS]', 'green')} PIP upgraded successfully.")
        except subprocess.CalledProcessError:
            print(f"{colored('[ERROR]', 'red')} Error upgrading pip.")
        finally:
            os.system("cls" if os.name == "nt" else "clear")

    def upgrade_setuptools(self, pip_path):
        try:
            curr_version = subprocess.check_output([pip_path, 'show', 'setuptools']).decode().split('\n')
            for line in curr_version:
                if 'Version:' in line:
                    curr_version = line.split(' ')[-1]
                    break
            required_version = "61.0.0"
            if parse_version(curr_version) < parse_version(required_version):
                print(f"{colored('[INFO]', 'yellow')} UPGRADING SETUPTOOLS...")
                subprocess.check_call([pip_path, 'install', '--upgrade', 'setuptools'])
        except Exception as e:
            print(f"{colored('[ERROR]', 'red')} ERROR UPGRADING SETUPTOOLS...")

        os.system("cls" if os.name == "nt" else "clear")

    def download_bronkhorst_library(self, pip_path):
        print(f"{colored('[INFO]', 'yellow')} DOWNLOADING BRONKHORST LIBRARY...")

        try:
            # Intentamos instalar bronkhorst-propar
            subprocess.check_call(['pip', 'install', 'bronkhorst-propar==1.1.1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{colored('[STATUS]', 'green')} bronkhorst-propar INSTALLED SUCCESSFULLY.")
            print()
            
            # Comprobamos si 'instrument' está en 'propar'
            try:
                import propar
                if hasattr(propar, 'instrument'):
                    print(f"{colored('[STATUS]', 'green')} 'instrument' class found in 'propar'. Installation successful.")
                else:
                    raise ImportError("instrument class not found in propar")
            
            except ImportError:
                print(f"{colored('[WARNING]', 'yellow')} 'instrument' class not found in 'propar'. Attempting reinstall...")
                # Purga la caché de pip
                subprocess.check_call([pip_path, 'cache', 'purge'])
                # Desinstala bronkhorst-propar
                subprocess.check_call([pip_path, 'uninstall', '-y', 'bronkhorst-propar'])
                # Reinstala bronkhorst-propar
                subprocess.check_call([pip_path, 'install', 'bronkhorst-propar==1.1.1'])
                
                # Verificación final
                try:
                    import propar
                    if hasattr(propar, 'instrument'):
                        print(f"{colored('[STATUS]', 'green')} Reinstallation successful. 'instrument' class is now available.")
                    else:
                        print(f"{colored('[ERROR]', 'red')} 'instrument' class still not found in 'propar' after reinstall.")
                except ImportError:
                    print(f"{colored('[ERROR]', 'red')} Failed to import 'propar' after reinstall.")

        except subprocess.CalledProcessError:
            print(f"{colored('[ERROR]', 'red')} ERROR INSTALLING bronkhorst-propar.")

    def check_and_install_required_packages(self, pip_path):
        for package in ["tqdm", "colorama", "pkg_resources"]:
            try:
                __import__(package)
            except ImportError:
                print(f"{colored('[INFO]', 'yellow')} INSTALLING {package}...")
                subprocess.check_call([pip_path, 'install', package])

    def create_environment(self):
        if not os.path.exists(self.env_path):
            print(f"{colored('[INFO]', 'yellow')} CREATING VIRTUAL ENVIRONMENT... {self.env_name}...")
            venv.create(self.env_path, with_pip=True)
            print(f"{colored('[STATUS]', 'green')} VIRTUAL ENVIRONMENT CREATED SUCCESSFULLY {self.env_name}...")

        os.system("cls" if os.name == "nt" else "clear")

    def install_dependencies(self, pip_path):
        print(f"{colored('[INFO]', 'yellow')} INSTALLING DEPENDENCIES... {self.env_name}...")
        print()

        for dependency in self.dependencies:
            print(f"{colored('[INFO]', 'yellow')} INSTALLING {dependency}...")
            try:
                subprocess.check_call([pip_path, 'install', dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{colored('[STATUS]', 'green')} {dependency} INSTALLED SUCCESSFULLY.")
                print()
            except subprocess.CalledProcessError:
                print(f"{colored('[ERROR]', 'red')} ERROR INSTALLING {dependency}")

        os.system("cls" if os.name == "nt" else "clear")

    def set_vscode_interpreter(self):
        settings_path = os.path.join(os.getcwd(), '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                f.write('{}')
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        settings["python.pythonPath"] = os.path.join(self.env_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'python')
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

        os.system("cls" if os.name == "nt" else "clear")

    def run_gas_main(self):
        """Run GasMain.py using the Python interpreter from the virtual environment."""
        print(f"{colored('[STATUS]', 'green')} RUNNING THE MAIN APPLICATION...")
        python_executable = os.path.join(self.env_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'python')
        gas_main_path = os.path.join(os.getcwd(), 'GasMain.py')
        try:
            subprocess.check_call([python_executable, gas_main_path])
        except subprocess.CalledProcessError as e:
            print(f"{colored('[ERROR]', 'red')} ERROR RUNNING THE MAIN APPLICATION...")

    def setup(self):
        pip_path = os.path.join(self.env_path, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(self.env_path, 'bin', 'pip')
        self.create_environment()
        self.upgrade_pip(pip_path)
        self.upgrade_setuptools(pip_path)
        self.download_bronkhorst_library(pip_path)
        self.check_and_install_required_packages(pip_path)
        self.install_dependencies(pip_path)
        self.set_vscode_interpreter()
        self.run_gas_main()
