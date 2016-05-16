import sys
from analyzer.parsers import SabadellParser
from decimal import Decimal
from datetime import date
import plotly
import plotly.graph_objs as go

filename = sys.argv[1]
parsed_data = SabadellParser(filename).parse()

# 1. All expenses above 50 grouped by day

# get expenses higher or equal 50.0
big_expenses = filter(lambda x: x.amount <= Decimal('-50.0'), parsed_data)

# user Scatter GL for better performance and to get rid of labeling bug
trace = go.Scattergl(
    x=[x.date for x in big_expenses],
    y=[str(y.amount) for y in big_expenses],
    mode='markers',
    marker=dict(size=12,
                line=dict(width=1)
                ),
    text=[t.title for t in big_expenses]
)

# plot
fig = go.Figure(data=[trace])
plot_url = plotly.offline.plot(fig, filename='major_expenses')


# 2. Monthly expenses: compare above 50 vs below 50
def group(expense, dict):
    # month = "%s/%02d" % (expense.date.year, expense.date.month)
    month = date(expense.date.year, expense.date.month, 1)
    try:
        group = dict[month]
    except KeyError:
        group = dict[month] = []
    group.append(expense)

monthly_expenses = {}
map(lambda x: group(x, monthly_expenses), parsed_data)


def summarise_monthly_data(data, filter_function):
    return [int(sum([x.amount for x in (filter(filter_function, data[key]))])) for key in monthly_expenses.keys()]

# TODO format the date nicely
expenses = go.Bar(
    y=monthly_expenses.keys(),
    x=summarise_monthly_data(monthly_expenses, lambda exp: exp.amount < Decimal(0)),
    name='Expenses',
    orientation='h',
    marker = dict(
        color='rgba(239, 15, 15, 0.6)',
        line=dict(
            color='rgba(239, 15, 15, 1.0)',
            width=1,
        ),
    ),
)

income = go.Bar(
    y=monthly_expenses.keys(),
    x=summarise_monthly_data(monthly_expenses, lambda exp: exp.amount > Decimal(0)),
    name='Income',
    orientation='h',
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1,
        ),
    ),
)
layout = go.Layout(
    # barmode='stack'
)
# plot
fig = go.Figure(data=[expenses, income], layout=layout)
plot_url = plotly.offline.plot(fig, filename='expenses_vs_income')