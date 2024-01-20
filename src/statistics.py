from src.data_processor import filter_last_week_data, filter_before_n_month_data, filter_last_month_data
## Time Management
def calculate_total_duration_by_category(data, week):
    if week:
        data = filter_last_week_data(data)
    data['total_duration'] = data['duration'].apply(lambda x: int(x.hour) + int(x.minute)/60)
    return data.groupby('category')['total_duration'].sum()
def calculate_total_duration_by_day(data, week):
    if week:
        data = filter_last_week_data(data)
    data['total_duration'] = data['duration'].apply(lambda x: int(x.hour) + int(x.minute)/60)
    return data.groupby('date')['total_duration'].sum()

def calculate_average_daily_duration_by_month(data):
    data['total_duration'] = data['duration'].apply(lambda x: int(x.hour) * 60 + int(x.minute))

    data['month'] = data['date'].dt.strftime('%Y-%m')

    monthly_data = data.groupby('month').agg(
        total_duration=('total_duration', 'sum'),
        last_day_of_month=('date', lambda x: x.dt.days_in_month.max())
    )

    monthly_data['average_daily_duration'] = monthly_data['total_duration'] / monthly_data['last_day_of_month']/60

    return monthly_data[['average_daily_duration']].reset_index()

def calculate_project_duration(data, week):
    if week:
        data = filter_last_week_data(data)
    if 'category' not in data.columns:
        raise ValueError("Data does not contain 'category' column.")

    data['total_duration'] = data['duration'].apply(lambda x: x.hour + x.minute / 60)

    project_duration = data.groupby(['project name', 'category'])['total_duration'].sum().reset_index()

    project_duration = project_duration.sort_values(by='total_duration', ascending=False)
    if not week:
        project_duration = project_duration.sort_values(by='total_duration', ascending=False).head(10)

    return project_duration

### Accouting Book
def calculate_total_balance(data, n):
    data = filter_before_n_month_data(data, n)
    latest_balances = data.drop_duplicates(subset=['account'], keep='last')
    total_balance = latest_balances['balance'].sum()
    formatted_number = f"{total_balance:,.2f}"
    return formatted_number

def calculate_expense_by_category(detail_data, last_month):
    filtered_data = detail_data[(detail_data['category'] != '0-info') &
                                (detail_data['expenditure'].notna()) &
                                (detail_data['expenditure'] != 0)]
    if last_month:
        filtered_data = filter_last_month_data(filtered_data)
    expenses = filtered_data.groupby('category')['expenditure'].sum().reset_index()
    expenses = expenses.sort_values('category').set_index('category')
    return expenses['expenditure']

def calculate_expense_by_tags(detail_data):
    filtered_data = detail_data[(detail_data['tag'] != 'daily') &
                                (detail_data['expenditure'].notna()) &
                                (detail_data['expenditure'] != 0)]
    expenses = filtered_data.groupby('tag')['expenditure'].sum().reset_index()
    expenses = expenses.sort_values('tag').set_index('tag')
    return expenses['expenditure']
def calculate_total_expense_last_month(data):
    data = data[(data['category'] != '0-info') &
                       (data['expenditure'].notna()) &
                       (data['expenditure'] != 0)]
    data = filter_last_month_data(data)
    total_expense_last_month = data['expenditure'].sum()
    return total_expense_last_month

def calculate_total_income_last_month(data):
    data = data[(data['category'] != '0-info') &
            (data['income'].notna()) &
            (data['income'] != 0)]
    data = filter_last_month_data(data)

    total_income_last_month = data['income'].sum()
    return total_income_last_month

def calculate_informational_transfer_last_month(data):
    category_name = "0-info"

    data = data[
        (data['category'] == category_name)
        ]
    data = filter_last_month_data(data)

    total_income = data['income'].sum()
    total_expense = data['expenditure'].sum()

    informational_transfer = total_income - total_expense
    return informational_transfer

def calculate_monthly_expense(data):

    data = data[data['category'] != '0-info']
    data['month'] = data['date'].dt.strftime('%Y-%m')

    monthly_expense = data.groupby('month')['expenditure'].sum()
    print(monthly_expense)
    return monthly_expense.reset_index()

def calculate_monthly_income(data):
    data = data[data['category'] != '0-info']
    data['month'] = data['date'].dt.strftime('%Y-%m')

    monthly_expense = data.groupby('month')['income'].sum()
    return monthly_expense.reset_index()