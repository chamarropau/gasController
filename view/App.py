from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QCheckBox, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QSpinBox, QGridLayout, QWidget, QGroupBox,
    QMessageBox, QDoubleSpinBox, QApplication, QLineEdit, QLabel, QGraphicsOpacityEffect
)
from view.ElectricalTypeDialog import ElectricalTypeDialog
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QCursor
from matplotlib.backend_bases import MouseEvent
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import time
from PyQt5.QtCore import QThread, pyqtSignal

MAX_MEASUREMENT_TIME = 5000
MAX_ADQUISITION_TIME = 5000
MAX_SAVING_TIME = 5000
MAX_FLOW = 200

NO_MODE_SELECTED = "You need to select a mode to run."
NO_FILE_SELECTED = "You need to select an Excel file to run the automatic mode."
NO_EL_TYPE_SELECTED = "You need to select an electrical type to run the manual mode."
NO_DATA_SHEET_SELECTED = "You need to select a data sheet to run the automatic mode."
NO_KEITHLEY_SELECTED = "You need to select at least one Keithley to run the program."
NO_FLOWS_SET = "You need to set the flows for the MFCs."
TOTAL_FLOW_HIGHER_THAN_MAX = "The total flow is higher than the maximum allowed. Please adjust the flows."
MODE_RUNNED_SUCCESSFULLY = "The mode has been runned successfully. Proceding to the next step."

class RunModeThread(QThread):
    finished = pyqtSignal()  # Señal para notificar cuando termine el modo
    error = pyqtSignal(str)  # Señal para manejar errores

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        try:
            self.controller.run_mode()
            self.finished.emit()  # Emitir señal cuando termine
        except Exception as e:
            self.error.emit(str(e))  # Emitir señal de error si ocurre

class App(QMainWindow):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.last_hovered_point = None
        self.graphs = None
        self.keithley_selected = None
        self.measurements = []

        self.mfc_labels = ["MFC3", "MFC6", "MFC9", "MFC12", "MFC16", "MFC20"]

        self.selected_file_path = None
        self.configured_type = None

        # List for the graphic
        self.valueA = []
        self.valueB = []
        self.valueC = []
        self.valueD = []

        # Configure the main window
        self.setWindowTitle("Development of the control software for the greenhouse gas analysis platform.")
        self.center()

        # Create the main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.keithleys_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # Create controller buttons
        self.manual_mode_checkbox = QCheckBox("Enable Manual Mode")
        self.automatic_mode_checkbox = QCheckBox("Enable Automatic Mode")
        self.run_btn = QPushButton("RUN")
        self.clean_mode = QPushButton("Clean Mode")
        self.keithley_one = QPushButton("Keithley One")
        self.keithley_two = QPushButton("Keithley Two")
        self.both_keithley = QPushButton("Both Keithley")
        self.el_type_btn = QPushButton("Electrical Type")

        # ----------------------------- Display Area -----------------------------
        self.set_graphic()
        self.set_manual_mode()
        self.set_automatic_mode()
        self.keithleys_layout.addWidget(self.keithley_one)
        self.keithleys_layout.addWidget(self.keithley_two)
        self.keithleys_layout.addWidget(self.both_keithley)

        # ----------------------------- Set up signals -----------------------------
        self.manual_mode_checkbox.stateChanged.connect(self.toggle_automatic_mode)
        self.automatic_mode_checkbox.stateChanged.connect(self.toggle_manual_mode)
        self.keithley_one.clicked.connect(self.toggle_keithley_one)
        self.keithley_two.clicked.connect(self.toggle_keithley_two)
        self.both_keithley.clicked.connect(self.toggle_both_keithleys)
        self.run_btn.clicked.connect(self.start)
        self.clean_mode.clicked.connect(self.clean_modes)

        # ----------------------------- Set the main layout -----------------------------
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addLayout(self.keithleys_layout)
        self.main_layout.addWidget(self.run_btn)
        self.main_layout.addWidget(self.clean_mode)

        self.main_widget.setLayout(self.main_layout)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------- CENTER THE WINDOW --------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    
    def center(self):
        width = 1000
        height = 800

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        x = (screen_rect.width() - width) // 2
        y = (screen_rect.height() - height) // 2

        self.setGeometry(x, y, width, height)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------- SETTERS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def set_graphic(self, x_label="X", y_label="Y", title="Real-Time Measurements", num_graphs=1, additional_ylabel="Y2"):

        if hasattr(self, 'canvas') and self.canvas is not None:
            self.top_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True)
        self.top_layout.addWidget(self.canvas)
        
        # Inicializar la leyenda vacía
        self.legend_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, fontsize=10,
                                        verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
        
        # Conectar el evento de clic
        self.canvas.mpl_connect("button_press_event", self.on_click)

        if hasattr(self, 'canvas2') and self.canvas2 is not None:
                self.top_layout.removeWidget(self.canvas2)
                self.canvas2.deleteLater()
                self.canvas2 = None

        if num_graphs == 2:
            self.figure2 = Figure()
            self.canvas2 = FigureCanvas(self.figure2)
            self.ax2 = self.figure2.add_subplot(111)
            self.ax2.set_title(title)
            self.ax2.set_xlabel(x_label)
            self.ax2.set_ylabel(additional_ylabel)
            self.ax2.grid(True)
            self.top_layout.addWidget(self.canvas2)

            self.legend_text2 = self.ax2.text(0.02, 0.95, '', transform=self.ax2.transAxes, fontsize=10,
                                            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
            
            self.canvas2.mpl_connect("button_press_event", self.on_click)

    def configure_graphic(self, mode):
        mode_labels = {
            "ManualIV": ("Voltage (V)", "Current (A)", "Voltage vs Current"),
            "ManualVI": ("Current (A)", "Voltage (V)", "Current vs Voltage"),

            "AutomaticIV": ("Voltage (V)", "Current (A)", "Voltage vs Current"),
            "AutomaticVI": ("Current (A)", "Voltage (V)", "Current vs Voltage"),

            "AutomaticIT": ("Time (s)", "Current (A)", "Current during Time"),
            "AutomaticVT": ("Time (s)", "Voltage (V)", "Voltage during Time"),
        }

        if mode in mode_labels:
            x_label, y_label, title = mode_labels[mode]
            self.set_graphic(x_label=x_label, y_label=y_label, title=title)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def set_manual_mode(self):
        self.manual_mode_group = QGroupBox("Manual Mode")
        manual_layout = QGridLayout()
        manual_layout.addWidget(self.manual_mode_checkbox, 0, 0, 1, 2)
        
        self.measurement_time = QDoubleSpinBox()
        # self.adquisition_time = QDoubleSpinBox()
        self.saving_time = QDoubleSpinBox()
        self.measurement_time.setRange(0, MAX_MEASUREMENT_TIME)
        # self.adquisition_time.setRange(0, MAX_ADQUISITION_TIME)
        self.saving_time.setRange(0, MAX_SAVING_TIME)
        self.measurement_time.setSuffix(" min")
        # self.adquisition_time.setSuffix(" min")
        self.saving_time.setSuffix(" min")
        self.measurement_time.setEnabled(False)
        # self.adquisition_time.setEnabled(False)
        self.saving_time.setEnabled(False)

        # Ask for the time of the measurement, adquisition and saving
        manual_layout.addWidget(QLabel("Measurement Time"), 1, 0, 1, 1)
        manual_layout.addWidget(self.measurement_time, 1, 2, 1, 2)
        # manual_layout.addWidget(QLabel("Adquisition Time"), 2, 0, 1, 1)
        # manual_layout.addWidget(self.adquisition_time, 2, 2, 1, 2)
        manual_layout.addWidget(QLabel("Saving Time"), 3, 0, 1, 1)
        manual_layout.addWidget(self.saving_time, 3, 2, 1, 2)

        self.mfc_checkboxes = {}
        self.mfc_spinboxes = {}

        # Insert MFC and SpinBoxes 
        for i, label in enumerate(self.mfc_labels):
            mfc_checkbox = QCheckBox(label)
            mfc_spinbox = QSpinBox()
            mfc_spinbox.setRange(0, 20 if i == 5 else 200)
            mfc_spinbox.setEnabled(False)
            mfc_checkbox.setEnabled(False)
            self.mfc_checkboxes[label] = mfc_checkbox
            self.mfc_spinboxes[label] = mfc_spinbox

            row = 4 + (i // 2)
            column = (i % 2) * 2

            # Add checkbox and spinbox to the layout
            manual_layout.addWidget(mfc_checkbox, row, column)
            manual_layout.addWidget(mfc_spinbox, row, column + 1)  

            # Connect the checkbox state with the corresponding spinbox
            mfc_checkbox.stateChanged.connect(lambda state, key=label: self.toggle_spinbox(key, state))

        self.el_type_btn.setEnabled(False)
        self.el_type_btn.clicked.connect(self.toggle_electrical_type)

        manual_layout.addWidget(self.el_type_btn, 10, 1, 1, 2)

        # Set the layout of the manual mode group
        self.manual_mode_group.setLayout(manual_layout)
        self.bottom_layout.addWidget(self.manual_mode_group)

    def set_automatic_mode(self):
        self.automatic_mode_group = QGroupBox("Automatic Mode")

        # Layout principal para centrar vertical y horizontalmente
        vbox_layout = QVBoxLayout()

        # Añadimos la casilla de verificación en la parte superior (arriba del todo)
        vbox_layout.addWidget(self.automatic_mode_checkbox, alignment=Qt.AlignLeft)

        # Espaciador flexible para empujar el resto del contenido hacia el centro vertical
        vbox_layout.addStretch(1)

        # Creamos un layout de cuadrícula para los widgets
        automatic_layout = QGridLayout()

        # Botón Import Excel en la fila 0, centrado horizontalmente
        self.import_excel_button = QPushButton("Import Excel")
        self.import_excel_button.setEnabled(False)
        self.import_excel_button.setFixedSize(100, 50)
        self.import_excel_button.setCursor(Qt.PointingHandCursor)
        self.import_excel_button.clicked.connect(self.import_excel)

        # Añadimos el botón Import Excel centrado horizontalmente
        automatic_layout.addWidget(self.import_excel_button, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        # Añadimos un QLabel y QLineEdit en la misma fila, centrados horizontalmente
        self.sheet_name_label = QLabel("Sheet Name:")
        self.sheet_name_input = QLineEdit()
        self.sheet_name_input.setPlaceholderText("Enter sheet name")

        # Añadimos ambos widgets en la fila 1
        automatic_layout.addWidget(self.sheet_name_label, 1, 0, alignment=Qt.AlignRight)
        automatic_layout.addWidget(self.sheet_name_input, 1, 1, alignment=Qt.AlignLeft)

        # Añadimos el layout de cuadrícula al layout vertical
        vbox_layout.addLayout(automatic_layout)

        # Espaciador flexible en la parte inferior para empujar el contenido hacia arriba
        vbox_layout.addStretch(1)

        # Establecemos el layout del grupo y añadimos el layout vertical
        self.automatic_mode_group.setLayout(vbox_layout)
        self.bottom_layout.addWidget(self.automatic_mode_group)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #-------------------------------------- TOGGLE FUNCTIONS --------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def toggle_manual_mode(self, state):
        if state == Qt.Checked:
            self.manual_mode_checkbox.setChecked(False)
            self.toggle_import_excel(True)
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)

        if not self.automatic_mode_checkbox.isChecked() and not self.manual_mode_checkbox.isChecked():
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)
            self.toggle_import_excel(False)

    def toggle_time_spinboxes(self, state):
        self.measurement_time.setEnabled(state)
        # self.adquisition_time.setEnabled(state)
        self.saving_time.setEnabled(state)

    def toggle_spinbox(self, label, state):
        self.mfc_spinboxes[label].setEnabled(state == Qt.Checked)
    
    def toggle_mfcs(self, state):
        for i, label in enumerate(self.mfc_labels):
            self.mfc_checkboxes[label].setEnabled(state)

    def toggle_electrical_type(self):
        dialog = ElectricalTypeDialog(self)
        dialog.exec_()
        self.configured_type = dialog.configured_el_type

    def toggle_el_type(self, state):
        self.el_type_btn.setEnabled(state)
            
    def toggle_automatic_mode(self, state):
        if state == Qt.Checked:
            self.automatic_mode_checkbox.setChecked(False)
            self.toggle_import_excel(False)
            self.toggle_time_spinboxes(True)
            self.toggle_mfcs(True)
            self.toggle_el_type(True)
        
        if not self.manual_mode_checkbox.isChecked() and not self.automatic_mode_checkbox.isChecked():
            self.toggle_time_spinboxes(False)
            self.toggle_mfcs(False)
            self.toggle_el_type(False)
            self.toggle_import_excel(False)

    def toggle_import_excel(self, state):
        self.import_excel_button.setEnabled(state)
        self.sheet_name_input.setEnabled(state)

    def toggle_keithley_one(self):
        self.keithley_one.setEnabled(False)
        self.keithley_two.setEnabled(True)
        self.both_keithley.setEnabled(True)

    def toggle_keithley_two(self):
        self.keithley_one.setEnabled(True)
        self.keithley_two.setEnabled(False)
        self.both_keithley.setEnabled(True)

    def toggle_both_keithleys(self):
        self.keithley_one.setEnabled(True)
        self.keithley_two.setEnabled(True)
        self.both_keithley.setEnabled(False)


    def import_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        
        if file_name:
            self.selected_file_path = file_name

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------ WARNINGS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def show_warning(self, message):
        warning_box = QMessageBox()
        warning_box.setWindowTitle("Warning")
        warning_box.setText(message)
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------------------- GETTERS ------------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    def get_manual_values(self):
        dict_config = {}
        dict_selected_type = {}

        measurement_time = self.measurement_time.value() * 60
        # adquisition_time = self.adquisition_time.value() * 60
        saving_time = self.saving_time.value() * 60
        mfc_values = {label: self.mfc_spinboxes[label].value() for label, checkbox in self.mfc_checkboxes.items() if checkbox.isChecked()}

        # Check if the total flow is higher than the maximum allowed
        total_flow = sum(mfc_values.values())
        if total_flow > MAX_FLOW:
            self.show_warning(TOTAL_FLOW_HIGHER_THAN_MAX)

            # Set all MFC spinboxes to 0
            for spinbox in self.mfc_spinboxes.values():
                spinbox.setValue(0)

            # Set mfc_values to an empty dictionary
            mfc_values = {}

        dict_config["measurement_time"] = measurement_time
        dict_config["adquisition_time"] = 0
        dict_config["saving_time"] = saving_time

        if self.configured_type is None:
            self.show_warning(NO_EL_TYPE_SELECTED)

        else:
            selected_type = self.configured_type.get("electrical_type", None)   
            voltage_value = self.configured_type.get("voltage", None)
            final_voltage_value = self.configured_type.get("final_voltage", None)
            current_value = self.configured_type.get("current", None)
            final_current_value = self.configured_type.get("final_current", None)
            unit_value = self.configured_type.get("unit", None)
            initial_unit = self.configured_type.get("initial_unit", None)
            final_unit = self.configured_type.get("final_unit", None)
            n_points_value = self.configured_type.get("n_points", None)

            dict_selected_type["selected_type"] = selected_type
            dict_selected_type["voltage_value"] = voltage_value
            dict_selected_type["final_voltage_value"] = final_voltage_value
            dict_selected_type["current_value"] = current_value
            dict_selected_type["final_current_value"] = final_current_value
            dict_selected_type["unit_value"] = unit_value
            dict_selected_type["initial_unit"] = initial_unit
            dict_selected_type["final_unit"] = final_unit
            dict_selected_type["n_points_value"] = n_points_value

            return dict_config, mfc_values, dict_selected_type



    def get_automatic_values(self):
        if self.selected_file_path is None:
            self.show_warning(NO_FILE_SELECTED)

        elif self.sheet_name_input.text() == "":
            self.show_warning(NO_DATA_SHEET_SELECTED)

        else:
            # Return the selected file path
            data = {}
            data["selected_file_path"] = self.selected_file_path
            data["sheet_name"] = self.sheet_name_input.text()
            return data
        

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #------------------------------ FUNCTIONS FOR THE MAIN PROGRAM --------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    def map_selected_type(self, selected_type):
        self.input_mapping = {
            "ManualIV": 1,
            "ManualVI": 2,
            "AutomaticIV": 3,
            "AutomaticVI": 4,
            "AutomaticIT": 5,
            "AutomaticVT": 6,
        }
        return self.input_mapping[selected_type]
        
    def set_measurement_manual_mode(self, type, measurement_time):
        # Obatin the selected type
        selected_type = type["selected_type"]
        voltage_value = type["voltage_value"]
        final_voltage_value = type["final_voltage_value"]
        current_value = type["current_value"]
        final_current_value = type["final_current_value"]
        unit_value = type["unit_value"]
        initial_unit = type["initial_unit"]
        final_unit = type["final_unit"]
        n_points_value = type["n_points_value"]

        # Map the selected type
        mapped_type = self.map_selected_type(selected_type)
        print(mapped_type)

        if mapped_type == 1: # ManualIV
            self.controller.set_manual_IV(voltage_value, unit_value, measurement_time)

        elif mapped_type == 2: # ManualVI
            self.controller.set_manual_VI(current_value, unit_value, measurement_time)

        elif mapped_type == 3: # AutomaticIV
            self.controller.set_automatic_IV(voltage_value, initial_unit, final_voltage_value, final_unit, n_points_value, measurement_time)

        elif mapped_type == 4: # AutomaticVI
            self.controller.set_automatic_VI(current_value, initial_unit, final_current_value, final_unit, n_points_value, measurement_time)

        elif mapped_type == 5: # AutomaticIT
            self.controller.set_automatic_IT(voltage_value, unit_value, measurement_time)

        elif mapped_type == 6: # AutomaticVT
            self.controller.set_automatic_VT(current_value, unit_value, measurement_time)

    def clean_modes(self):
        self.measurement_time.setValue(0)
        # self.adquisition_time.setValue(0)
        self.saving_time.setValue(0)

        for spinbox in self.mfc_spinboxes.values():
            spinbox.setValue(0)

        for checkbox in self.mfc_checkboxes.values():
            checkbox.setChecked(False)

        # Set and clean electrical type
        self.configured_type = None

        # Clean the keithley selection
        self.keithley_one.setEnabled(True)
        self.keithley_two.setEnabled(True)
        self.both_keithley.setEnabled(True)

        # Clean the graphic
        self.set_graphic()

        # Clean the selected file path
        self.selected_file_path = None
        self.sheet_name_input.setText("")

        self.valueA = []
        self.valueB = []
        self.prev_len = 0
        self.valueC = []
        self.valueD = []

        self.controller.clean_measures()

    def clean_graphics(self):
        self.ax.clear()
        self.canvas.draw_idle()

        self.valueA = []
        self.valueB = []
        self.prev_len = 0
        self.valueC = []
        self.valueD = []

    def show_popup(self):
        # Crear un QLabel como notificación
        popup = QLabel("Flows set correctly", self)
        popup.setStyleSheet("background-color: lightgreen; color: black; font-size: 16px; border-radius: 10px;")
        popup.setAlignment(Qt.AlignCenter)
        popup.setGeometry(50, 50, 200, 50)  # Posición y tamaño

        # Mostrar el popup y cerrarlo después de 2 segundos
        popup.show()
        QTimer.singleShot(2000, popup.close)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    #-------------------------------------- RUN THE PROGRAM ---------------------------------------------#
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################

    # Método modificado en la clase App
    def start(self):

        if not self.keithley_one.isEnabled() and not self.keithley_two.isEnabled() and not self.both_keithley.isEnabled():
            self.show_warning(NO_KEITHLEY_SELECTED)
        else:
            if self.manual_mode_checkbox.isChecked() and self.configured_type is not None:
                config, mfcs, type = self.get_manual_values()
                self.type_conf = type
                self.configure_graphic(type["selected_type"])

                if mfcs == {}:
                    self.show_warning(NO_FLOWS_SET)
                else:
                    print("Saving time: ", config["saving_time"])
                    self.controller.set_mode("manual", flows=mfcs, keithley_selected=1, sv_time=config["saving_time"])

                    measurement_time = config["measurement_time"]
                    ad_time = config["adquisition_time"]
                    sv_time = config["saving_time"]

                    self.set_measurement_manual_mode(type, measurement_time)
                    self.controller.set_data_manager(measurement_time, ad_time, sv_time)

                    # Crear y configurar el hilo para ejecutar run_mode
                    self.run_mode_thread = RunModeThread(self.controller)
                    self.run_mode_thread.finished.connect(self.on_run_mode_finished)
                    self.run_mode_thread.error.connect(self.show_error)

                    # Iniciar el hilo
                    self.run_mode_thread.start()

                    # Configurar e iniciar el temporizador
                    self.prev_len = 0
                    self.measures = []
                    self.timer = QTimer()
                    self.start_time = None
                    self.timer.timeout.connect(self.check_measurements)
                    self.timer.start(5)

            elif self.automatic_mode_checkbox.isChecked():
                excel = self.get_automatic_values()
                print(excel["selected_file_path"], excel["sheet_name"])
                file = excel['selected_file_path']
                sheet = excel['sheet_name']

                if not self.keithley_one.isEnabled():
                    self.set_graphic(x_label="Time (s)", y_label="Current (A)")
                    self.graphs = 1
                    self.controller.set_mode("automatic", keithley_selected=1, excel=file, sheet=sheet)
                    self.keithley_selected = 1

                elif not self.keithley_two.isEnabled():
                    self.set_graphic(x_label="Time (s)", y_label="Voltage (V)")
                    self.graphs = 1
                    self.controller.set_mode("automatic", keithley_selected=2, excel=file, sheet=sheet)
                    self.keithley_selected = 2

                elif not self.both_keithley.isEnabled():
                    self.set_graphic(x_label="Time (s)", y_label="Current (A)", num_graphs=2, additional_ylabel="Voltage (V)")
                    self.graphs = 2
                    self.controller.set_mode("automatic", keithley_selected=3, excel=file, sheet=sheet)
                    self.keithley_selected = 3

                self.run_mode_thread = RunModeThread(self.controller)
                self.run_mode_thread.finished.connect(self.on_run_mode_finished)
                self.run_mode_thread.error.connect(self.show_error)

                self.run_mode_thread.start()
 
                self.prev_len = 0
                self.measures = []
                self.timer = QTimer()
                self.start_time = None
                self.timer.timeout.connect(self.check_automatic_measures)
                self.timer.start(5)

            else:
                self.show_warning(NO_MODE_SELECTED)

    def on_run_mode_finished(self):
        """Llamado cuando el hilo de run_mode termina."""
        self.timer.stop()  # Detener el temporizador
        self.controller.close_mfcs()  # Apagar los dispositivos
        
    def show_error(self, message):
        """Mostrar un mensaje de error desde el hilo."""
        self.show_warning(message)

    def check_measurements(self):
        measurements = self.controller.get_measurements()

        if measurements and len(measurements) != self.prev_len:
            last_tuple = measurements[-1]

            if self.type_conf["selected_type"] in ["AutomaticVT", "AutomaticIT"]:
                if len(last_tuple) == 3:
                    valueA, valueB, valueC = last_tuple
                    self.fixedValue = valueB
                    self.update_graphic_realtime(valueA, valueC)
            else:
                if len(last_tuple) == 2: 
                    valueA, valueB = last_tuple
                    self.update_graphic_realtime(valueA, valueB)

            self.prev_len = len(measurements)

    def check_automatic_measures(self):

        measures = self.controller.get_automatic_measures(self.keithley_selected)

        # Seleccionamos las listas según el valor de self.graphs
        if len(measures) == 1:
            measures1 = measures[0]
            lists_to_process = [measures1]

        if len(measures) == 2:
            measures1 = measures[0]
            measures2 = measures[1]
            if not self.keithley_one.isEnabled():
                lists_to_process = [measures1]
            elif not self.keithley_two.isEnabled():
                lists_to_process = [measures2]
            elif not self.both_keithley.isEnabled():
                lists_to_process = [measures1, measures2]

        for measures in lists_to_process:
            if len(measures) != 0:
                if len(measures) != self.prev_len:
                    last_tuple = measures[-1]
                    valueA, valueB = last_tuple

                    self.setMValue = valueB

                    if self.start_time is None:
                        self.start_time = time.time()

                    elapsed_time = time.time() - self.start_time  # Calculamos el tiempo transcurrido

                    # Actualizamos el gráfico (puedes diferenciar por lista si es necesario)
                    self.update_graphic_realtime(valueA, elapsed_time)

                    # Actualizamos el tamaño previo solo si estamos trabajando con una lista específica
                    self.prev_len = len(measures)

    def update_graphic_realtime(self, valueA, valueB):
        """Método para actualizar la gráfica en tiempo real."""
        self.valueA.append(valueA)
        self.valueB.append(valueB)

        self.ax.plot(self.valueB, self.valueA, color='b')
        self.ax.scatter(self.valueB, self.valueA, color='r', marker='x')
        self.ax.grid(True)
        
        # Volver a agregar la leyenda
        self.legend_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, fontsize=10,
                                        verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

        self.canvas.draw_idle()

        if self.graphs == 2:
            self.ax2.plot(self.valueB, self.valueA, color='b')
            self.ax2.scatter(self.valueB, self.valueA, color='r', marker='x')
            self.ax2.grid(True)
            self.legend_text2 = self.ax2.text(0.02, 0.95, '', transform=self.ax2.transAxes, fontsize=10,
                                            verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
            self.canvas2.draw_idle()


    def on_click(self, event):
        """Detecta clics cerca de un punto y actualiza la leyenda para uno o dos gráficos."""
        from termcolor import colored
        # Determinar qué ejes y lienzo procesar
        axes = [self.ax]
        canvases = [self.canvas]
        
        if self.graphs == 2:
            axes.append(self.ax2)
            canvases.append(self.canvas2)

        for ax, canvas in zip(axes, canvases):
            if event.inaxes != ax:
                continue  # Si el clic no está en el eje actual, pasa al siguiente

            # Buscar el punto más cercano
            min_dist = float('inf')
            closest_point = None
            for x, y in zip(self.valueB, self.valueA):  # Ajusta si valueB y valueA son diferentes para ax2
                dist = (event.xdata - x) ** 2 + (event.ydata - y) ** 2
                if dist < min_dist and dist < 0.05:  # Umbral de cercanía
                    min_dist = dist
                    closest_point = (x, y)

            # Si se encuentra un punto cercano, actualizar la leyenda
            if closest_point:
                if ax.get_legend():
                    ax.get_legend().remove()  # Eliminar la leyenda anterior

                if not self.automatic_mode_checkbox.isChecked():
                    if self.type_conf["selected_type"] == "AutomaticIV" or self.type_conf["selected_type"] == "ManualIV":
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {closest_point[0]:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {closest_point[1]:.4e} A...")
                        legend_text = f"Voltage: {closest_point[0]:.4e} V\nCurrent: {closest_point[1]:.4e} A"

                    elif self.type_conf["selected_type"] == "AutomaticVI" or self.type_conf["selected_type"] == "ManualVI":
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {closest_point[1]:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {closest_point[0]:.4e} A...")
                        legend_text = f"Voltage: {closest_point[1]:.4e} V\nCurrent: {closest_point[0]:.4e} A"

                    elif self.type_conf["selected_type"] == "AutomaticIT":
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {self.fixedValue:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {closest_point[1]:.4e} A...")
                        print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                        legend_text = f"Voltage: {self.fixedValue:.4e} V\nCurrent: {closest_point[1]:.4e} A\nTime: {closest_point[0]:.4e} s"

                    elif self.type_conf["selected_type"] == "AutomaticVT":
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {closest_point[1]:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {self.fixedValue:.4e} A...")
                        print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                        legend_text = f"Current: {self.fixedValue:.4e} A\nVoltage: {closest_point[1]:.4e} V\nTime: {closest_point[0]:.4e} s"

                else:
                    if not self.keithley_one.isEnabled():
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {self.setMValue:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {closest_point[1]:.4e} A...")
                        print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                        legend_text = f"Voltage: {self.setMValue:.4e} V\nCurrent: {closest_point[1]:.4e} A\nTime: {closest_point[0]:.4e} s"

                    elif not self.keithley_two.isEnabled():
                        print(f"{colored('[INFO]', 'light_cyan')} Voltage: {closest_point[1]:.4e} V...")
                        print(f"{colored('[INFO]', 'light_cyan')} Curent: {self.setMValue:.4e} A...")
                        print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                        legend_text = f"Current: {self.setMValue:.4e} A\nVoltage: {closest_point[1]:.4e} V\nTime: {closest_point[0]:.4e} s"

                    elif not self.both_keithley.isEnabled():
                        if ax == self.ax2 and self.graphs == 2:
                            print(f"{colored('[INFO]', 'light_cyan')} Voltage: {closest_point[1]:.4e} V...")
                            print(f"{colored('[INFO]', 'light_cyan')} Curent: {self.setMValue:.4e} A...")
                            print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                            legend_text = f"Current: {self.setMValue:.4e} A\nVoltage: {closest_point[1]:.4e} V\nTime: {closest_point[0]:.4e} s"
                        else:
                            print(f"{colored('[INFO]', 'light_cyan')} Voltage: {self.setMValue:.4e} V...")
                            print(f"{colored('[INFO]', 'light_cyan')} Curent: {closest_point[1]:.4e} A...")
                            print(f"{colored('[INFO]', 'light_cyan')} Time: {closest_point[0]:.4e} s...")
                            legend_text = f"Current: {closest_point[1]:.4e} A\nVoltage: {self.setMValue:.4e} V\nTime: {closest_point[0]:.4e} s"

                # Crear nueva leyenda sin marcador
                ax.legend([legend_text], loc="upper left", handlelength=0)  # Sin línea
                canvas.draw_idle()
