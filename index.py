import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv("data/transaction.csv", encoding="cp932")
df["日付"] = pd.to_datetime(df['日付'], format='%Y-%m-%d')
df["年"] = df['日付'].dt.year
df["月"] = df['日付'].dt.month
df["金額"] = df['金額'].astype(int)

df_sum = df.groupby(["顧客名", "商品名"]).sum().sort_values(
    ["顧客名", "金額"], ascending=False).reset_index()


transction_scatter = px.scatter(df_sum, x="数量", y="単価", color="顧客名",
                                size='金額', hover_data=['商品名'])

df_time = df.groupby(["顧客名", "年", "月"]).sum().sort_values(
    ["顧客名", "金額"], ascending=False).reset_index()
df_time["日付"] = pd.to_datetime(df_time['年'].astype(
    str)+df_time['月'].astype(str), format='%Y%m')
df_time = df_time.sort_values(["顧客名", "日付"])
transction_line = px.line(df_time, x="日付", y="金額", color="顧客名")

app.layout = html.Div(children=[
    html.H1(children='仕分けの可視化'),

    html.Div(children='''
        仕分けの情報を可視化することで不正な取引のあたりをつける
    '''),

    dcc.Graph(
        id='transction_scatter',
        figure=transction_scatter
    ),

    dcc.Graph(
        id='transction_line',
        figure=transction_line
    )
])

if __name__ == '__main__':
    app.run_server()
