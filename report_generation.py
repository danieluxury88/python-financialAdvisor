# report_generation.py
from config import HTML_REPORT
import pandas as pd
import matplotlib.pyplot as plt

# Reporting and visualization
def generate_report(totals, file_path):
    months = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(10, 5))
    plt.plot(months, amounts, marker='o')
    plt.xlabel('Month')
    plt.ylabel('Total Valor en Dólares')
    plt.title('Reporte Financiero Mensual')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

# Table generation
def generate_table(totals):
    df = pd.DataFrame(list(totals.items()), columns=['Month', 'Total Valor en Dólares'])
    df.sort_values(by='Month', inplace=True)
    return df

# Comprehensive table of all financial records
def generate_comprehensive_table(records):
    df = pd.DataFrame([{
        'TARJETA': record.tarjeta,
        'FECHA': record.fecha,
        'NUMERO_REFERENCIA': record.numero_referencia,
        'DESCRIPCION': record.descripcion,
        'FORMA_PAGO': record.forma_pago,
        'VALOR_DOLARES': record.valor_dolares,
        'SALDO_DIFERIDO': record.saldo_diferido,
        'MONTH': record.month
    } for record in records])
    df.sort_values(by='DESCRIPCION', inplace=True)  # Sort by DESCRIPTION alphabetically
    return df

# Function to sort the comprehensive table by any column
def sort_table(df, column, ascending=True):
    sorted_df = df.sort_values(by=column, ascending=ascending)
    return sorted_df

# Function to filter the comprehensive table based on specific criteria
def filter_table(df, column, value):
    filtered_df = df[df[column] == value]
    return filtered_df

# Function to filter the comprehensive table based on partial match criteria
def filter_table_contains(df, column, value):
    filtered_df = df[df[column].str.contains(value, case=False, na=False)]
    return filtered_df

# Function to group the data and aggregate values
def group_table(df, by_column, agg_column, agg_func='sum'):
    grouped_df = df.groupby(by_column).agg({agg_column: agg_func}).reset_index()
    return grouped_df

# Function to group the data based on partial match criteria and aggregate values
def group_table_contains(df, by_column, value, agg_column, agg_func='sum'):
    df_filtered = df[df[by_column].str.contains(value, case=False, na=False)]
    grouped_df = df_filtered.groupby(by_column).agg({agg_column: agg_func}).reset_index()
    return grouped_df

# Function to sum all positive values in VALOR_DOLARES
def sum_positive_values(df):
    positive_sum = df[df['VALOR_DOLARES'] > 0]['VALOR_DOLARES'].sum()
    return positive_sum

# Function to sum all negative values in VALOR_DOLARES
def sum_negative_values(df):
    negative_sum = df[df['VALOR_DOLARES'] < 0]['VALOR_DOLARES'].sum()
    return negative_sum

# Function to generate HTML report
# Function to generate HTML report
def generate_html_report(totals_by_month, comprehensive_df, sorted_df, filtered_df, filtered_df_contains, grouped_df, grouped_df_contains, sum_positive, sum_negative, plot_path):
    html = f"""
    <html>
    <head>
        <title>Financial Report</title>
        <style>
            table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 5px; }}
            th {{ background-color: #f2f2f2; }}
            th, td {{ text-align: center; }}
        </style>
    </head>
    <body>
        <h1>Financial Report</h1>

        <h2>Monthly Totals</h2>
        {totals_by_month.to_html(index=False)}

        <h2>Comprehensive Financial Records</h2>
        {comprehensive_df.to_html(index=False)}

        <h2>Sorted by Valor Dolares (Descending)</h2>
        {sorted_df.to_html(index=False)}

        <h2>Filtered by Forma Pago = 'CORRIENTE'</h2>
        {filtered_df.to_html(index=False)}

        <h2>Filtered by Descripcion containing 'pizza'</h2>
        {filtered_df_contains.to_html(index=False)}

        <h2>Grouped by Month (Sum of Valor Dolares)</h2>
        {grouped_df.to_html(index=False)}

        <h2>Grouped by Descripcion containing 'pizza' (Sum of Valor Dolares)</h2>
        {grouped_df_contains.to_html(index=False)}

        <h2>Sum of Positive Valor Dolares</h2>
        <p>{sum_positive}</p>

        <h2>Sum of Negative Valor Dolares</h2>
        <p>{sum_negative}</p>

        <h2>Monthly Financial Report Plot</h2>
        <img src="{plot_path}" alt="Monthly Financial Report Plot">
    </body>
    </html>
    """
    with open(HTML_REPORT, "w") as file:
        file.write(html)

