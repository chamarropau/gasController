## Interfaz Gráfica de Usuario (GUI) en PyQt5

Al seleccionar el modo de ejecución **GUI**, se despliega una aplicación desarrollada en PyQt5 que permite una gestión visual e interactiva del sistema. La interfaz está organizada en varias secciones funcionales, cada una dedicada a configurar diferentes aspectos del sistema de control y automatización.

![image](https://github.com/user-attachments/assets/ec81dc08-c547-48ed-ab08-5b888ba6e488)



#### Área de Visualización

La sección superior de la ventana presenta el **Área de Visualización**, donde se muestran los resultados y datos en tiempo real generados por el sistema. Este espacio central permite al usuario monitorear el estado del software y cualquier información relevante en el proceso de análisis de gases.

#### Modo Manual

En la parte inferior izquierda se encuentra la sección **Manual Mode**, destinada a la configuración y control manual de los dispositivos y parámetros del sistema. Incluye las siguientes opciones:

- **Enable Manual Mode**: Activando esta casilla, el usuario habilita el modo manual, lo que permite personalizar cada uno de los parámetros de forma independiente.
- **Measurement Time, Acquisition Time, Saving Time**: Estas entradas permiten configurar los tiempos de medición, adquisición y almacenamiento, expresados en minutos, para controlar la duración de cada operación.
- **MFCs (Mass Flow Controllers)**: Cada controlador de flujo de masa (MFC3, MFC6, MFC9, MFC12, MFC16, MFC20) tiene un campo de entrada para ajustar manualmente su flujo específico. Esta configuración es útil para personalizar las tasas de flujo en experimentos que requieren valores precisos.
- **Electrical Type**: Al hacer clic en este botón, se despliega un cuadro de diálogo (*QtDialog*) que permite al usuario especificar el tipo de configuración eléctrica para los experimentos, proporcionando una capa adicional de personalización. La funcionalidad exacta de este diálogo se describirá en secciones posteriores.

<div align="center">
    <img src="https://github.com/user-attachments/assets/cf9f3ce4-f378-4d7c-8411-dcdee51eca1b" alt="image">
</div>

<br>
Al hacer clic en el botón **Electrical Type** en el **Modo Manual**, se despliega un cuadro de diálogo (*QtDialog*) que permite seleccionar el tipo de medición eléctrica que se utilizará en el sistema. Este diálogo presenta seis opciones de medición, cada una con sus propios campos configurables para adaptarse a diferentes tipos de análisis. A continuación se describe cada opción en detalle:

- **ManualIV**: Configuración manual para mediciones de corriente en función del voltaje (I-V). Al seleccionar esta opción, el usuario puede ingresar el **voltaje** deseado y elegir la **unidad** adecuada (mV, µV, o V) según los requerimientos de precisión del experimento.

<div align="center">
    <img src="https://github.com/user-attachments/assets/481dec47-7934-4c57-8443-820be1da1b4e" alt="image">
</div>
<br>

- **ManualVI**: Configuración manual para mediciones de voltaje en función de la corriente (V-I). En esta modalidad, el usuario introduce la **intensidad** deseada y selecciona la **unidad** correspondiente (mA, µA, o A).
<div align="center">
    <img src="https://github.com/user-attachments/assets/cbfc396b-17c5-43ca-aaa2-b0906fd7d617" alt="image">
</div>
<br>

- **AutomaticIV**: Configuración automática para mediciones de corriente en función del voltaje (I-V) en un rango específico. Esta opción permite especificar un **voltaje inicial** y un **voltaje final**, así como la **unidad** (mV, µV, o V). Además, el usuario puede definir el número de **steps** (pasos) en los que se dividirá el rango, permitiendo una medición continua y precisa.
<div align="center">
    <img src="https://github.com/user-attachments/assets/b02667af-7e7e-44cf-8118-0d8d2cfe01d1" alt="image">
</div>
<br>

- **AutomaticVI**: Configuración automática para mediciones de voltaje en función de la corriente (V-I) en un rango determinado. Similar a *AutomaticIV*, esta opción requiere ingresar una **intensidad inicial** y una **intensidad final**, junto con la **unidad** (mA, µA, o A) y el número de **steps** para realizar las mediciones en intervalos específicos.
<div align="center">
    <img src="https://github.com/user-attachments/assets/de62543f-0d0e-422b-be15-d661c4a5dc6c" alt="image">
</div>
<br>

- **AutomaticIT**: Configuración automática para mediciones de corriente en función del tiempo (I-T). Al elegir esta opción, el usuario introduce un **voltaje** y selecciona la **unidad** correspondiente. Este tipo de medición es útil para estudios donde la corriente varía con el tiempo bajo un voltaje constante.
<div align="center">
    <img src="https://github.com/user-attachments/assets/568daeec-4ed3-42ab-8cc3-6df7720fee66" alt="image">
</div>
<br>

- **AutomaticVT**: Configuración automática para mediciones de voltaje en función del tiempo (V-T). En esta modalidad, el usuario puede ingresar la **intensidad** y seleccionar la **unidad** (mA, µA, o A), permitiendo analizar el comportamiento del voltaje a lo largo del tiempo bajo una corriente constante.
<div align="center">
    <img src="https://github.com/user-attachments/assets/43f784ec-688e-44cd-ae11-4699cdec1f4f" alt="image">
</div>
<br>

Este cuadro de diálogo es dinámico y ajusta sus campos de entrada según la opción seleccionada, proporcionando una interfaz intuitiva y eficiente para los distintos tipos de medición eléctrica.



#### Modo Automático

A la derecha del Modo Manual, se encuentra la sección **Automatic Mode**, diseñada para configuraciones automáticas mediante la importación de datos externos. Las opciones en esta sección incluyen:

- **Enable Automatic Mode**: Esta casilla habilita el modo automático, permitiendo que el sistema configure y ejecute automáticamente según los datos especificados.
- **Import Excel**: Un botón que permite cargar un archivo Excel con los parámetros de control y medición previamente definidos. Este método es ideal para realizar experimentos o procesos repetitivos sin necesidad de ingresar manualmente cada valor.
- **Sheet Name**: Un campo de entrada donde el usuario debe especificar el nombre de la hoja dentro del archivo Excel que contiene los datos a importar.

#### Selección de Keithley

En la parte inferior central, el usuario puede seleccionar entre **One Keithley** o **Two Keithley**. Esta opción define si se usará uno o dos dispositivos Keithley para la medición, lo cual puede influir en la precisión y el tipo de datos recopilados durante la ejecución del programa.

#### Botón de Ejecución

Finalmente, en la parte inferior de la ventana se encuentra el botón **RUN**. Al presionarlo, se inicia el flujo principal del programa con los parámetros seleccionados, ya sea en modo manual o automático, y con una o dos Keithleys según la configuración.
