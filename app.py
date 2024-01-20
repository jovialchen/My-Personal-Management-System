from flask import Flask, render_template
from src.data_processor import read_excel, process_data
from src.statistics import *
from src.visualization import *

app = Flask(__name__)

# Configuration
TIME_FILE_PATH = 'data/time.xlsx'
TIME_SHEET_NAME = ('history_data')
MONEY_FILE_PATH = 'data/finance.xlsx'  # Excel文件路径
MONEY_SHEETS_NAME = ['details', 'my_account']
def get_processed_data(file_path, sheet_name):
    data = read_excel(file_path, sheet_name)
    if data is None:
        return None
    return process_data(data)

def generate_statistics_time(processed_data):
    stats = {
        'total_duration_by_category': calculate_total_duration_by_category(processed_data, False),
        'average_duration_by_month': calculate_average_daily_duration_by_month(processed_data),
        'total_duration_by_project': calculate_project_duration(processed_data, False),
        'total_duration_by_category_last_week': calculate_total_duration_by_category(processed_data, True),
        'total_duration_by_day_last_week': calculate_total_duration_by_day(processed_data, True),
        'total_duration_by_project_last_week': calculate_project_duration(processed_data, True)
    }
    return stats

def generate_charts_time(stats):
    charts = {
        'category_chart': create_category_duration_chart(stats['total_duration_by_category'].reset_index()),
        'daily_chart': create_average_month_daily_duration_chart(stats['average_duration_by_month'].reset_index()),
        'project_chart': create_project_duration_chart(stats['total_duration_by_project']),
        'last_week_category_chart': create_category_duration_chart(stats['total_duration_by_category_last_week'].reset_index()),
        'last_week_daily_chart': create_daily_duration_chart(stats['total_duration_by_day_last_week'].reset_index()),
        'last_week_project_chart': create_project_duration_chart(stats['total_duration_by_project_last_week'])
    }
    return charts
def generate_value_money(data):
    values = {
        'total_balance': calculate_total_balance(data['details'], 0),
        'total_balance_1_month': calculate_total_balance(data['details'], 1),
        'total_balance_2_month': calculate_total_balance(data['details'], 2),
        'expense_last_month': calculate_total_expense_last_month(data['details']),
        'income_last_month': calculate_total_income_last_month((data['details'])),
        'informational_transfer_last_month':calculate_informational_transfer_last_month((data['details']))
    }
    return values
def generate_statistics_money(processed_data):
    stats = {
        'expenses_by_category': calculate_expense_by_category(processed_data['details'], False),
        'expenses_by_category_last_month': calculate_expense_by_category(processed_data['details'], True),
        'expense_by_tag': calculate_expense_by_tags(processed_data['details']),
        'expense_by_month': calculate_monthly_expense(processed_data['details']),
        'income_by_month': calculate_monthly_income(processed_data['details']),
    }
    return stats
def generate_chart_money(stats):
    charts = {
        'expense_category_chart': create_expense_chart_by_category(stats['expenses_by_category'].to_dict()),
        'expense_category_chart_last_month': create_expense_chart_by_category(stats['expenses_by_category_last_month'].to_dict()),
        'expense_tag_chart': create_expense_chart_by_tag(stats['expense_by_tag'].to_dict()),
        'expense_by_month': create_monthly_expense_chart(stats['expense_by_month'].to_dict()),
        'income_by_month': create_monthly_income_chart(stats['income_by_month'].to_dict()),

    }
    return charts
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/time-management')
def time_management():
    processed_data = get_processed_data(TIME_FILE_PATH, TIME_SHEET_NAME)
    if processed_data is not None:
        stats = generate_statistics_time(processed_data)
        charts = generate_charts_time(stats)
        return render_template('time_management.html', **charts)

    return "无法加载数据，请检查文件路径和格式。"

@app.route('/accounting')
def accounting():
    data = read_excel(MONEY_FILE_PATH, MONEY_SHEETS_NAME)
    if data is not None:
        values = generate_value_money(data)
        stats = generate_statistics_money(data)
        charts = generate_chart_money(stats)
        return render_template('accounting.html', **values, **charts)

    return "无法加载数据，请检查文件路径和格式。"

if __name__ == '__main__':
    app.run(debug=True)