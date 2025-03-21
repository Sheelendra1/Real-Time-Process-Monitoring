from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import psutil
from collections import deque
import time
from threading import Thread

app = Dash(__name__)

cpu_data = deque(maxlen=50)
memory_data = deque(maxlen=50)
timestamps = deque(maxlen=50)

app.layout = html.Div([
    html.H1("Real-Time Process Monitoring Dashboard"),
    dcc.Graph(id='cpu-usage-graph'),
    dcc.Graph(id='memory-usage-graph'),
    html.Table(id='process-table'),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)
])

def update_data():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        timestamps.append(time.strftime("%H:%M:%S"))
        cpu_data.append(cpu_usage)
        memory_data.append(memory_usage)
        time.sleep(2)

Thread(target=update_data, daemon=True).start()

@app.callback(
    [Output('cpu-usage-graph', 'figure'),
     Output('memory-usage-graph', 'figure'),
     Output('process-table', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    cpu_fig = px.line(x=list(timestamps), y=list(cpu_data), labels={'x': 'Time', 'y': 'CPU Usage (%)'})
    memory_fig = px.line(x=list(timestamps), y=list(memory_data), labels={'x': 'Time', 'y': 'Memory Usage (%)'})
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(html.Tr([
            html.Td(proc.info['pid']),
            html.Td(proc.info['name']),
            html.Td(f"{proc.info['cpu_percent']:.2f}%"),
            html.Td(f"{proc.info['memory_percent']:.2f}%"),
            html.Td(html.Button('Kill', id=f"kill-{proc.info['pid']}", n_clicks=0))
        ]))
    
    process_table = html.Table([
        html.Thead(html.Tr([html.Th("PID"), html.Th("Name"), html.Th("CPU (%)"), html.Th("Memory (%)"), html.Th("Action")])),
        html.Tbody(processes)
    ])
    
    return cpu_fig, memory_fig, process_table

@app.callback(
    Output('process-table', 'children', allow_duplicate=True),
    [Input(f"kill-{proc.info['pid']}", 'n_clicks') for proc in psutil.process_iter(['pid'])],
    prevent_initial_call=True
)
def kill_process(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    pid = int(button_id.split('-')[1])
    try:
        psutil.Process(pid).terminate()
    except psutil.NoSuchProcess:
        pass
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(html.Tr([
            html.Td(proc.info['pid']),
            html.Td(proc.info['name']),
            html.Td(f"{proc.info['cpu_percent']:.2f}%"),
            html.Td(f"{proc.info['memory_percent']:.2f}%"),
            html.Td(html.Button('Kill', id=f"kill-{proc.info['pid']}", n_clicks=0))
        ]))
    
    return html.Table([
        html.Thead(html.Tr([html.Th("PID"), html.Th("Name"), html.Th("CPU (%)"), html.Th("Memory (%)"), html.Th("Action")])),
        html.Tbody(processes)
    ])

if __name__ == "__main__":
    app.run(debug=True)