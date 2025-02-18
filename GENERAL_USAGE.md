# SoftwareGasControl: Sistema de Control y Automatización de Entorno en Python

Este documento proporciona una explicación detallada sobre el funcionamiento del programa *SoftwareGasControl*, incluyendo los datos requeridos en cada campo, el flujo principal del programa y el manejo de excepciones. Su objetivo es facilitar el uso del software y minimizar cualquier posible ambigüedad para usuarios de distintos niveles.

## Descripción General

El archivo principal, `GasMain.py`, es el punto de entrada del sistema. Su ejecución permite la gestión integral del flujo de la aplicación, con funciones orientadas tanto a la ejecución del programa como a la configuración automática de un entorno Python llamado `SoftwareGasControl`. Este entorno asegura que todas las dependencias necesarias se instalen y actualicen conforme a las exigencias del software, eliminando así la necesidad de verificaciones manuales.

### Creación y Gestión del Entorno Virtual

Al ejecutarse, el sistema detecta la presencia del entorno virtual. Si este no existe, `SoftwareGasControl` lo genera automáticamente y procede a instalar las dependencias requeridas. Este procedimiento asegura una configuración óptima, evitando la duplicación de paquetes en el sistema. Las dependencias solo se descargarán en el caso de que no estén presentes en el entorno, garantizando un proceso eficiente y controlado.

### Configuración Automática en Visual Studio Code

Para facilitar la interacción del usuario con el entorno, el programa asigna automáticamente el intérprete de Python en *Visual Studio Code* al entorno `SoftwareGasControl`, evitando la necesidad de seleccionar versiones específicas de Python o paquetes individuales. De esta forma, el usuario puede concentrarse en el uso del software sin requerir conocimientos previos de configuración en entornos de desarrollo integrados.


## Selección del Modo de Ejecución: Terminal o Interfaz Gráfica

Una vez completada la instalación y configuración del entorno `SoftwareGasControl`, el programa solicita al usuario que elija el modo de ejecución. A través de una entrada por teclado, se presentan dos opciones: 
- **1** para la ejecución en modo terminal (*TerminalView*).
- **2** para la ejecución mediante la interfaz gráfica de usuario (GUI).

Según la selección del usuario, el sistema iniciará el flujo principal del programa en el modo correspondiente, permitiendo flexibilidad para adaptarse a las preferencias y necesidades del usuario.
