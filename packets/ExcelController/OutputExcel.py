import pandas as pd

class OutputExcel:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def save_excel(self):
        df = pd.DataFrame(self.data)
        df = df.apply(pd.Series.explode)
        df = df.loc[:, ~df.columns.duplicated()]

        # Separar valores y unidades en Voltage_1
        df[['Voltage_1', 'Voltage_Unit']] = df['Voltage_1'].str.split(' ', expand=True)

        # Separar valores y unidades en Current_1
        df[['Current_1', 'Current_Unit']] = df['Current_1'].str.split(' ', expand=True)

        # Separar valores y unidades en MFC3, MFC6, MFC9, MFC12, MFC16, MFC20
        # df[['MFC3_Flow', 'MFC3_Unit']] = df['MFC3'].str.split(' ', expand=True)
        # df[['MFC6_Flow', 'MFC6_Unit']] = df['MFC6'].str.split(' ', expand=True)
        # df[['MFC9_Flow', 'MFC9_Unit']] = df['MFC9'].str.split(' ', expand=True)
        # df[['MFC12_Flow', 'MFC12_Unit']] = df['MFC12'].str.split(' ', expand=True)
        # df[['MFC16_Flow', 'MFC16_Unit']] = df['MFC16'].str.split(' ', expand=True)
        # df[['MFC20_Flow', 'MFC20_Unit']] = df['MFC20'].str.split(' ', expand=True)

        # Definir el orden de las columnas que nos interesa
        # ordered_columns = ['MFC3_Flow', 'MFC3_Unit', 'MFC6_Flow', 'MFC6_Unit', 'MFC9_Flow', 'MFC9_Unit', 'MFC12_Flow', 'MFC12_Unit', 'MFC16_Flow', 'MFC16_Unit', 'MFC20_Flow', 'MFC20_Unit', 'temperature', 'humidity', 'time', 'Voltage_1', 'Voltage_Unit', 'Current_1', 'Current_Unit']
        ordered_columns = ['temperature', 'humidity', 'time', 'Voltage_1', 'Voltage_Unit', 'Current_1', 'Current_Unit']

        # Filtrar las columnas del DataFrame que están en ordered_columns
        existing_columns = [col for col in ordered_columns if col in df.columns]

        # Agregar las columnas adicionales (no en ordered_columns) al inicio
        additional_columns = [col for col in df.columns if col not in existing_columns]

        # Reordenar las columnas: primero las adicionales, luego las ordenadas
        df = df[additional_columns + existing_columns]

        df.to_excel(self.filename, index=False)
