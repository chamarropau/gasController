from view.MenuController import MenuController, MainMenuOptions, MeasurementMenuOptions
import sys

class TerminalView:
    def __init__(self, controller):
        self.controller = controller
        self.menu = MenuController()

    def start(self):
        print("Setting up the environment for the first time...")
        self.menu.display_menu("main")
        option = self.menu.get_option("main")
        
        
        if option == MainMenuOptions.AUTOMATIC_MEASUREMENT.value:
            # self.controller.set_mode("automatic", num_keithley=1, excel=file, sheet=sheet)
            num_keithleys = self.controller.get_num_keithleys()

            if num_keithleys == 1:
                self.menu.menus["select_keithleys"]["options"] = {
                    1: "Keithley"
                }

            self.menu.display_menu("select_keithleys")
            option = self.menu.get_option("select_keithleys")
            print("OPTION",int(option))
            self.controller.set_mode("automatic", keithley_selected=option)


        elif option == MainMenuOptions.MANUAL_MEASUREMENT.value:
            measurement_time, ad_time, sv_time = self.get_times()
            self.controller.set_mode('manual', keithley_selected=1, sv_time=sv_time)
            self.get_manual_options(measurement_time)
            self.controller.set_data_manager(measurement_time, ad_time, sv_time)
            
        elif option == MainMenuOptions.EXIT.value:
            print("\n\nGoodbye! :D\n\n")
            sys.exit(0)
        
        print(self.controller.run_mode()) # measurement_time, ad_time, sv_time
            
    def get_manual_options(self, measurement_time):
        self.menu.display_menu("measurement")
        option = self.menu.get_option("measurement")
    
        if option == MeasurementMenuOptions.NO_MEASUREMENT.value:
            pass
        
        elif option == MeasurementMenuOptions.MANUAL_VI.value:
            self.menu.display_menu("current_scale")
            current_option = self.menu.get_option("current_scale")
            current_unit = self.menu.menus["current_scale"]["options"][current_option]
            current = self.menu.get_user_input("Introduce the Current Value (%s): " % current_unit, min_value=0, type='float')
            self.controller.set_manual_VI(current, current_unit, measurement_time) 
        
        elif option == MeasurementMenuOptions.MANUAL_IV.value:
            self.menu.display_menu("voltage_scale")
            voltage_option = self.menu.get_option("voltage_scale")
            voltage_unit = self.menu.menus["voltage_scale"]["options"][voltage_option]
            voltage = self.menu.get_user_input("Introduce the Voltage Value (%s): " % voltage_unit, type='float')
            self.controller.set_manual_IV(voltage, voltage_unit, measurement_time) 
        
        elif option == MeasurementMenuOptions.AUTOMATIC_VI.value:
            self.menu.display_menu("current_scale")
            current_option = self.menu.get_option("current_scale")
            initial_unit = self.menu.menus["current_scale"]["options"][current_option]
            initial_current = self.menu.get_user_input("Introduce the Initial Current Value (%s): " % initial_unit)

            self.menu.display_menu("current_scale")
            current_option = self.menu.get_option("current_scale")
            final_unit = self.menu.menus["current_scale"]["options"][current_option]
            final_current = self.menu.get_user_input("Introduce the Final Current Value (%s): " % final_unit)
            n_points_current = self.menu.get_user_input("Introduce the number of points you want: ", min_value=0)
            
            # self.controller.set_automatic_VI(initial_current, final_current, current_unit, n_points_current, measurement_time)
            self.controller.set_automatic_VI(initial_current, initial_unit, final_current, final_unit, n_points_current, measurement_time)

        elif option == MeasurementMenuOptions.AUTOMATIC_IV.value:
            self.menu.display_menu("voltage_scale")
            voltage_option = self.menu.get_option("voltage_scale")
            initial_unit = self.menu.menus["voltage_scale"]["options"][voltage_option]
            initial_voltage = self.menu.get_user_input("Introduce the Initial Voltage Value (%s): " % initial_unit)

            self.menu.display_menu("voltage_scale")
            voltage_option = self.menu.get_option("voltage_scale")
            final_unit = self.menu.menus["voltage_scale"]["options"][voltage_option]
            final_voltage = self.menu.get_user_input("Introduce the Final Voltage Value (%s): " % final_unit, type='float')
            n_points_voltage = self.menu.get_user_input("Introduce the number of points you want: ", min_value=0)
            
            # self.controller.set_automatic_IV(initial_voltage, final_voltage, voltage_unit, n_points_voltage, measurement_time)
            self.controller.set_automatic_IV(initial_voltage, initial_unit, final_voltage, final_unit, n_points_voltage, measurement_time)

        elif option == MeasurementMenuOptions.AUTOMATIC_VT.value:
            self.menu.display_menu("current_scale")
            current_option = self.menu.get_option("current_scale")
            current_unit = self.menu.menus["current_scale"]["options"][current_option]
            current = self.menu.get_user_input("Introduce the Current Value (%s): " % current_unit, min_value=0, type='float')
            
            self.controller.set_automatic_VT(current, current_unit, measurement_time)
            
        elif option == MeasurementMenuOptions.AUTOMATIC_IT.value:
            self.menu.display_menu("voltage_scale")
            voltage_option = self.menu.get_option("voltage_scale")
            voltage_unit = self.menu.menus["voltage_scale"]["options"][voltage_option]
            voltage = self.menu.get_user_input("Introduce the Voltage Value (%s): " % voltage_unit)
            
            self.controller.set_automatic_IT(voltage, voltage_unit, measurement_time)

    def get_times(self):
        measurement_time = self.menu.get_user_input("Introduce the measurement time (minuts): ", min_value=0, type='float')
        # ad_time = self.menu.get_user_input("Introduce adquisition time (minuts): ", min_value=0, type='float')
        sv_time = self.menu.get_user_input("Introduce save time (minuts): ", min_value=0, type='float')
        measurement_time = measurement_time * 60
        ad_time = 0
        sv_time = sv_time * 60

        return measurement_time, ad_time, sv_time
