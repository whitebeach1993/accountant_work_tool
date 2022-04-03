import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

app = dash.Dash(
    external_stylesheets=[dbc.themes.SIMPLEX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
server = app.server

df = pd.read_csv("data/transaction.csv", encoding="cp932")
view_columns = ['日付', '顧客名', '商品名', '分類', '単価', '数量', '金額']
df = df[view_columns]
df["日付"] = pd.to_datetime(df['日付'], format='%Y-%m-%d')
df["年"] = df['日付'].dt.year
df["月"] = df['日付'].dt.month
df["金額"] = df['金額'].astype(int)

df_sum = df.groupby(["顧客名", "商品名", "単価"]).sum().sort_values(
    ["金額"], ascending=False).reset_index()
view_columns = ['顧客名', '商品名', '単価', '数量', '金額']
df_sum = df_sum[view_columns]

transction_scatter = px.scatter(df_sum, x="数量", y="単価", color="顧客名",
                                size='金額', hover_data=['商品名'])

df_time = df.groupby(["顧客名", "年", "月"]).sum().sort_values(
    ["顧客名", "金額"], ascending=False).reset_index()
df_time["日付"] = pd.to_datetime(df_time['年'].astype(
    str)+df_time['月'].astype(str), format='%Y%m')
df_time = df_time.sort_values(["顧客名", "日付"])
transction_line = px.line(df_time, x="日付", y="金額", color="顧客名")

print("--------------------------------------")
app.layout = dbc.Container(
    [dbc.Row(
        [
            dbc.Col(
                html.H1("仕分けの全体像の可視化", className='text-center text-primary mb-4'),
                width=12
            )
        ],
        className="h-30",
    ),
        dbc.Row(
            [
                dbc.Col([
                    html.H4("サンプルデータ(取引数: "+str(len(df))+")"),
                    dash_table.DataTable(df.to_dict('records'),
                                         [{"name": i, "id": i}
                                             for i in view_columns],
                                         page_size=5,
                                         sort_action='native',)


                ],
                    xs=12, sm=12, md=12, lg=6, xl=6,
                ),
                dbc.Col([
                    html.H4("サンプルデータの顧客名と商品名ごとの金額の合計値"),
                    dash_table.DataTable(df_sum.to_dict('records'),
                                         [{"name": i, "id": i}
                                             for i in df_sum.columns],
                                         page_size=5,
                                         sort_action='native',
                                         )

                ],
                    xs=12, sm=12, md=12, lg=6, xl=6,

                ),
            ],
        className="g-0",
    ),
        dbc.Row(
            [
                dbc.Col([
                    html.H4("取引（単価×数量)と取引先との関係"),
                    dcc.Graph(
                        id='transction_scatter',
                        config={
                            'displayModeBar': False,
                        },
                        figure=transction_scatter,
                    ), ],
                    xs=12, sm=12, md=12, lg=6, xl=6,
                ),
                dbc.Col([
                    html.H4("時期別取引金額の推移"),
                    dcc.Graph(
                        id='transction_line',
                        config={
                            'displayModeBar': False,
                        },
                        figure=transction_line,
                    ),
                ],
                    xs=12, sm=12, md=12, lg=6, xl=6,
                ),
            ],
    ),

    ],
    # style={"height": "90vh"},
)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
