import plotly.express as px

category_colors = {
    'Work': '#ffadad',
    'Hobby': '#fdffb6',
    'Study': '#caffbf'
}
colors = ['#ffadad', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff']
def create_project_duration_chart(project_duration_stats):


    fig = px.bar(
        project_duration_stats,
        x='total_duration',
        y='project name',
        color='category',
        orientation='h',
        title='Commitment Hours for Projects',
        labels={'x': 'Lasting Time（Hour）', 'y': 'Project Name'},
        color_discrete_map=category_colors  # 使用类别颜色字典
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig.to_html(full_html=False)


def create_category_duration_chart(data):
    fig = px.pie(data, values='total_duration', names='category', color='category', title='Commitment Hours for Different Categories',color_discrete_map=category_colors)
    return fig.to_html(full_html=False)


def create_daily_duration_chart(data):
    fig = px.bar(data, x='date', y='total_duration', title='Commitment Hours Everyday', color='date', color_discrete_sequence=colors)
    return fig.to_html(full_html=False)

def create_average_month_daily_duration_chart(average_daily_duration):
    data = average_daily_duration.reset_index()

    fig = px.bar(data, x='month', y='average_daily_duration', title='Average Daily Commitment Hours for Each Month', color='month', color_discrete_sequence=colors)

    return fig.to_html(full_html=False)


def create_expense_chart_by_category(expenses_by_category):
    categories = list(expenses_by_category.keys())
    expenses = list(expenses_by_category.values())

    # 创建条形图
    fig = px.bar(
        x=expenses,
        y=categories,
        labels={'x': 'Expenditure', 'y': 'Category'},
        orientation='h',
        title='Total Expenditure for Each Category',
        color=categories,
        color_discrete_sequence=colors[:len(categories)]
    )
    return fig.to_html(full_html=False)

def create_expense_chart_by_tag(expenses_by_tag):
    tags = list(expenses_by_tag.keys())
    expenses = list(expenses_by_tag.values())
    fig = px.bar(
        x=expenses,
        y=tags,
        labels={'x': 'expenditure', 'y': 'category'},
        orientation='h',
        title='Total Expenditure for Different Activites',
        color=tags,
        color_discrete_sequence=colors[:len(tags)]
    )

    return fig.to_html(full_html=False)

def create_monthly_expense_chart(monthly_expense):
    fig = px.bar(monthly_expense, x='month', y='expenditure', title='Total Expenditure Every Month', color='month', color_discrete_sequence=colors)
    return fig.to_html(full_html=False)
def create_monthly_income_chart(monthly_income):
    fig = px.bar(monthly_income, x='month', y='income', title='Total Income Every Month', color='month', color_discrete_sequence=colors)
    return fig.to_html(full_html=False)