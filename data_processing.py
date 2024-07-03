# data_processing.py

import pandas as pd
import os

# Define data structures
class FinancialRecord:
    def __init__(self, tarjeta, fecha, numero_referencia, descripcion, forma_pago, valor_dolares, saldo_diferido, month):
        self.tarjeta = tarjeta
        self.fecha = pd.to_datetime(fecha, format='%d/%m/%Y')  # Parse date correctly
        self.numero_referencia = numero_referencia
        self.descripcion = descripcion
        self.forma_pago = forma_pago
        self.valor_dolares = valor_dolares
        self.saldo_diferido = saldo_diferido
        self.month = month

# Data input
def read_initial_info(file_path):
    initial_data = pd.read_excel(file_path, nrows=20, header=None)
    initial_info = {}
    for index, row in initial_data.iterrows():
        label = row[0]
        value = row[1] if not pd.isna(row[1]) else 'PLACEHOLDER'
        initial_info[label] = value
    return initial_info

def read_financial_data(file_path):
    # Read the month from cell B7
    month = pd.read_excel(file_path, skiprows=6, nrows=1, usecols="B").iloc[0, 0]
    if isinstance(month, str):
        # Convert the month string to a more consistent format (e.g., "2024-06" for June 2024)
        month = pd.to_datetime(month, format='%d/%m/%Y').strftime('%Y-%m')

    # Read the financial data starting from row 21
    df = pd.read_excel(file_path, skiprows=20)
    df.columns = ['TARJETA', 'FECHA', 'NUMERO_REFERENCIA', 'DESCRIPCION', 'FORMA_PAGO', 'VALOR_DOLARES', 'SALDO_DIFERIDO']
    records = []
    for index, row in df.iterrows():
        record = FinancialRecord(
            tarjeta=row['TARJETA'],
            fecha=row['FECHA'],
            numero_referencia=row['NUMERO_REFERENCIA'],
            descripcion=row['DESCRIPCION'],
            forma_pago=row['FORMA_PAGO'],
            valor_dolares=row['VALOR_DOLARES'],
            saldo_diferido=row['SALDO_DIFERIDO'],
            month=month
        )
        records.append(record)
    return records

# Data processing and storage
def calculate_totals_by_month(records):
    totals = {}
    for record in records:
        if record.month not in totals:
            totals[record.month] = 0
        totals[record.month] += record.valor_dolares
    return totals

def read_all_records(directory):
    all_records = []

    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory, filename)
            initial_info = read_initial_info(file_path)
            print(f"Initial Information for {filename}:")
            for key, value in initial_info.items():
                print(f"{key}: {value}")

            records = read_financial_data(file_path)
            all_records.extend(records)

    return all_records
