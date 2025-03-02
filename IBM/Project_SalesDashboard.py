import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv(r'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

df['Recession'] = df['Recession'].astype(int)

df['Year'] = df['Year'].astype(int)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard', style={'textAlign':'center',
                                                                                        'color':'#503D36',
                                                                                        'font-size':24}),
                                html.Div(dcc.Dropdown(id='dropdown-statistics',
                                    options=[
                                        {'label':'Yearly Statistics','value':'Yearly Statistics'},
                                        {'label':'Recession Period Statistics','value':'Recession Period Statistics'}
                                    ],
                                    placeholder='Select a report type',
                                    value='Select Statistics',
                                    style={'width':'80%',
                                           'padding':'3px',
                                           'text-align-last':'center'})), # report dropdown
                                html.Div(dcc.Dropdown(id='select-year', 
                                    options=[{'label': i, 'value': i} for i in df['Year'].sort_values().unique()],
                                    placeholder='Select-year',
                                    value='Select-year',
                                    style={'width':'80%',
                                           'padding':'3px',
                                           'text-align-last':'center'})), # year dropdown
                                html.Br(),
                                html.Br(),
                                html.Div(html.Div(id='output-container',
                                                  className='chart-grid',
                                                  style={'display':'flex'}))])

@app.callback(
    Output(component_id='select-year', component_property='disabled'), # disable this component
    Input(component_id='dropdown-statistics',component_property='value')) # given somehting with this input
def update_input_container(report_type):
    if report_type =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(Output(component_id='output-container', component_property='children'),
              [Input(component_id='dropdown-statistics',component_property='value'), Input(component_id='select-year',component_property='value')])
def update_graphs(report_type, year_val: int):
    if report_type == 'Recession Period Statistics':
        rec_df = df[(df['Recession']== 1)]
        fig1 = dcc.Graph(figure=px.line(rec_df.groupby('Year')['Automobile_Sales'].mean().reset_index(), x='Year',y='Automobile_Sales', title='Recession Yearly Sales'))
        fig2 = dcc.Graph(figure=px.bar(rec_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(), x='Vehicle_Type',y='Automobile_Sales', title='Recession Vehicle Type Avg. Sales'))
        fig3 = dcc.Graph(figure=px.pie(rec_df.groupby('Vehicle_Type', as_index=False)['Advertising_Expenditure'].sum(), 
                                values='Advertising_Expenditure',
                                names='Vehicle_Type',
                                title='Recession Advertising Exp. by Vehicle Type'))
        fig4 = dcc.Graph(figure=px.bar(rec_df.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index(), 
                                       x='unemployment_rate',
                                       y='Automobile_Sales',
                                       color='Vehicle_Type',
                                       title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=fig1),
                                                       html.Div(children=fig2)],
                                                       style={'display':'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=fig3),
                                                       html.Div(children=fig4)],
                                                       style={'display':'flex'})            
        ]
    else:
        out_df = df[(df['Year']== year_val)]
        fig1 = dcc.Graph(figure=px.line(df.groupby('Year')['Automobile_Sales'].mean().reset_index(), x='Year',y='Automobile_Sales', title='Yearly Sales'))
        fig2 = dcc.Graph(figure=px.line(out_df.groupby('Month')['Automobile_Sales'].sum().reset_index(), x='Month',y='Automobile_Sales', title=f'Monthly Sales for {year_val}'))
        fig4 = dcc.Graph(figure=px.pie(out_df.groupby('Vehicle_Type', as_index=False)['Advertising_Expenditure'].sum(), 
                                values='Advertising_Expenditure',
                                names='Vehicle_Type',
                                title='Recession Advertising Exp. by Vehicle Type'))
        fig3 = dcc.Graph(figure=px.bar(out_df.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index(), x='Vehicle_Type',y='Automobile_Sales', color='Vehicle_Type', title='Sales by Vehicle Type'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=fig1),
                                                       html.Div(children=fig2)],
                                                       style={'display':'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=fig3),
                                                       html.Div(children=fig4)],
                                                       style={'display':'flex'})
        ]

if __name__ == '__main__':
    app.run_server()