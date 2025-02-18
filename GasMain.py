from EnvController import EnvironmentController
import sys
import os
from termcolor import colored

# Configurar el entorno virtual si no está ya configurado
env_path = os.path.join(os.getcwd(), "SoftwareGasControl")
if not os.path.exists(env_path):
    print("Setting up the environment for the first time...")
    env = EnvironmentController()
    env.setup()
os.system("cls" if os.name == "nt" else "clear")   
print(f"{colored('[STATUS]', 'green')} RUNNING THE MAIN APPLICATION...")
from controller.Controller import Controller
from view.TerminalView import TerminalView
from PyQt5.QtWidgets import QApplication 
from view.App import App

def main():

    # Crear el controlador de la aplicación
    controller = None
    controller = Controller()

    # Preguntar al usuario por el modo de ejecución
    try:
        running_mode = int(input("Select the running mode (1: Terminal View, 2: GUI): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        sys.exit(1)

    # Ejecutar el modo seleccionado por el usuario
    try:
        if running_mode == 1:
            # Modo terminal
            terminal = TerminalView(controller)
            terminal.start()
        elif running_mode == 2:
            # Modo GUI
            app = QApplication(sys.argv)
            window = App(controller)
            window.showMaximized()
            try:
                sys.exit(app.exec_())
            finally:
                controller.shutdown()
                print("Exiting...")
                sys.exit(0)

        else:
            print("Invalid option. Exiting.")
            sys.exit(1)
            

        # Apagar los dispositivos y cerrar la aplicación correctamente
        controller.shutdown()
        print("Exiting...")
        sys.exit(0)
        
    except (KeyboardInterrupt, Exception):
        controller.shutdown()
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
