# main.py

from config import EXCEL_DIRECTORY, PLOT_PATH
from data_processing import read_all_records, calculate_totals_by_month
from report_generation import (
    generate_report,
    generate_table,
    generate_comprehensive_table,
    sort_table,
    filter_table,
    filter_table_contains,
    group_table,
    group_table_contains,
    sum_positive_values,
    sum_negative_values,
    generate_html_report
)

def main():
    all_records = read_all_records(EXCEL_DIRECTORY)

    totals_by_month = calculate_totals_by_month(all_records)
    generate_report(totals_by_month, PLOT_PATH)
    totals_df = generate_table(totals_by_month)
    comprehensive_df = generate_comprehensive_table(all_records)

    sorted_df = sort_table(comprehensive_df, 'VALOR_DOLARES', ascending=False)
    filtered_df = filter_table(comprehensive_df, 'FORMA_PAGO', 'CORRIENTE')
    filtered_df_contains = filter_table_contains(comprehensive_df, 'DESCRIPCION', 'pizza')
    filtered_df_contains = filter_table_contains(comprehensive_df, 'DESCRIPCION', 'ND ')
    grouped_df = group_table(comprehensive_df, 'MONTH', 'VALOR_DOLARES', 'sum')
    grouped_df_contains = group_table_contains(comprehensive_df, 'DESCRIPCION', 'pizza', 'VALOR_DOLARES', 'sum')

    sum_positive = sum_positive_values(comprehensive_df)
    sum_negative = sum_negative_values(comprehensive_df)

    generate_html_report(
        totals_df, comprehensive_df, sorted_df, filtered_df, filtered_df_contains,
        grouped_df, grouped_df_contains, sum_positive, sum_negative, PLOT_PATH
    )

if __name__ == "__main__":
    main()
