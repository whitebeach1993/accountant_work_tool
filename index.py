from pydoc import pager
import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.SIMPLEX])
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

view_columns = ['日付', '顧客名', '商品名', '分類', '単価', '数量', '金額']

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("仕分けの可視化"),
                )
            ],
            className="h-30"
        ),
        dbc.Row(
            [
                # dbc.Col(
                #     html.H4("サンプルデータ"),
                #     dash_table.DataTable(
                #         id='table',
                #         columns=[{"name": i, "id": j}
                #                  for i, j in zip(df[view_columns], view_columns)],
                #         data=df.to_dict('records'),
                #         page_size=5,
                #         sort_action='native',
                #     ),
                #     width=6,
                #     style={"height": "100%", "size": "10px"},
                # ),
                dbc.Col(
                    html.H4("サンプルデータの顧客ごとの集計値"),
                    width=6,
                    style={"height": "100%", },
                ),
            ],
            className="h-50"
        ),

        dbc.Row(
            [
                # dbc.Col(
                #     html.H4("取引先ごとの数量と単価(大きさは金額)"),
                #     dcc.Graph(
                #         # id='transction_scatter',
                #         config={
                #             'displayModeBar': False,
                #         },
                #         figure=transction_scatter
                #     ),

                #     width=6,
                #     style={"height": "100%", },
                # ),
                dbc.Col(
                    dcc.Graph(
                        # id='transction_line',
                        config={
                            'displayModeBar': False,
                        },
                        figure=transction_line
                    ),
                    width=6,
                    style={"height": "100%", },
                ),
            ],
            className="h-50",
        ),
    ],
    style={"height": "90vh"},
)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
