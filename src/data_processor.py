import pandas as pd
from datetime import datetime, timedelta

def read_excel(file_path, sheet_name):
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        return data
    except Exception as e:
        print(f"Error Encountered Reading Excel: {e}")
        return None
def process_data(data):
    data.columns = [col.lower() for col in data.columns]
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'])
    return data
def filter_last_week_data(data):
    start_of_week = current_date - timedelta(days=current_date.weekday() + 7)
    start_of_week = datetime(start_of_week.year, start_of_week.month, start_of_week.day, 0, 0, 0)
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    return data[(data['date'] >= start_of_week) & (data['date'] <= end_of_week)]

def filter_before_n_month_data(data, n):
    today = datetime.now()
    n_month_ago = today - timedelta(days=30)*n
    data_n_month_ago = data[data['date'] <= n_month_ago]
    return data_n_month_ago

def filter_last_month_data(data):
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_month = last_day_of_previous_month.month
    previous_month_year = last_day_of_previous_month.year

    # 筛选出上个月的数据
    previous_month_data = data[
        (data['date'].dt.month == previous_month) &
        (data['date'].dt.year == previous_month_year)
        ]
    return previous_month_data
