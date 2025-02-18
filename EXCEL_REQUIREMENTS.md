# Instrucciones para Rellenar el Excel del TFG

El archivo Excel está diseñado para registrar y organizar datos experimentales de manera sistemática. A continuación, se detallan las instrucciones para completar cada sección de la hoja de cálculo, asegurando una entrada de datos coherente y precisa. El archivo Excel tendrá la siguiente estructura:

![image](https://github.com/user-attachments/assets/7b0e46cc-fc9d-4536-8553-0acf989aa523)


## Estructura del Archivo Excel

El archivo consta de las siguientes columnas, que deben ser completadas de acuerdo con las especificaciones proporcionadas:

- **step**: Cada fila representa un paso o medida en el experimento. Se puede rellenar o no, ya que no tiene ningún impacto sobre el código.

- **tipus**: Este campo especifica el tipo de medida. Asegúrese de seleccionar el tipo correspondiente para cada paso. El tipo puede ser o MESURA o FINAL.

- **ad_time**: Este campo se refiere al tiempo de adquisición, que indica cada cuánto tiempo se imprimirá un mensaje en la terminal. Debe ser especificado en el formato wdhms (semanas, días, horas, minutos y segundos). Si alguna unidad no es necesaria, simplemente omítala.

- **sv_time**: Este campo representa el tiempo de guardado, es decir, la frecuencia con la que los datos se guardarán en el archivo Excel. Al igual que con el tiempo de adquisición, se debe usar el formato wdhms.

- **temps**: Este campo indica la duración total de la medida. Debe rellenarse también en formato wdhms. Este tiempo se aplicará a ambas Keithleys si se seleccionan ambas para la medida.

- **mfc3, mfc6, mfc9, mfc12, mfc16, mfc20, mfc24**: Estas columnas corresponden a los flujos de los massflows para cada SMU (Source Measure Unit). Cada valor debe ser especificado según el modo de ejecución correspondiente, que se detalla a continuación.

## Modos de Ejecución y Especificaciones

Al registrar los flujos de los massflows, es crucial considerar el modo de ejecución que se está utilizando. A continuación, se presentan las especificaciones necesarias para cada modo:

- **ManualIV, AutomaticIT**: Para estos modos, se requiere el valor de voltaje y su unidad. Asegúrese de especificar el valor seguido de su unidad (mV, µV, V).

- **ManualVI, AutomaticVT**: Estos modos requieren el valor de corriente y su unidad. Similarmente, debe especificarse el valor seguido de su unidad (mA, µA, A).

- **AutomaticIV**: Este modo necesita el valor de voltaje inicial, final y el número de steps. El valor debe ser ingresado en la forma `valorInicial-valorFinal/steps` junto con la unidad correspondiente.

- **AutomaticVI**: Para este modo, se necesita el valor de corriente inicial, final y el número de steps. El valor se debe ingresar en el formato `valorInicial-valorFinal/steps` junto con la unidad adecuada.

## Unidades de Medida

Las unidades que se deben utilizar en el archivo son las siguientes:

- **Voltaje**: mV (milivoltios), µV (microvoltios), V (voltios).
- **Corriente**: mA (miliamperios), µA (microamperios), A (amperios).

## Registro de Medidas

Cada fila en el archivo Excel representa una medida. Es posible añadir tantas filas como sea necesario para registrar todas las medidas del experimento. Sin embargo, es imperativo que la última fila esté marcada como "FINAL" para indicar la conclusión de las mediciones.

Se aconseja revisar minuciosamente cada entrada antes de guardar el archivo para asegurar que todos los datos son correctos y están en el formato adecuado.

## Conclusiones

Estas instrucciones son esenciales para garantizar que el archivo Excel sea completado de manera adecuada y consistente
