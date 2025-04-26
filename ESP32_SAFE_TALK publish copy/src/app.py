import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import json
import pytz

file_path = r"C:/Users/lucia/OneDrive/Dokument/PlatformIO/Projects/ESP32_SAFE_TALK/src/sensor_data.txt"

def load_data():
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        times = []
        temperatures = []
        
        for line in lines:
            try:
                entry = json.loads(line)
                temperature = entry['data'][0][0]
                time_label = entry['labels'][0]
                temperatures.append(temperature)
                times.append(time_label)
            except json.JSONDecodeError:
                print(f"Failed to decode JSON: {line.strip()}")
        
        data = pd.DataFrame({
            'Time': times,
            'Temperature': temperatures
        })

        data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S', errors='coerce')
        local_tz = pytz.timezone('Europe/Stockholm')
        data['Time'] = data['Time'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
        data = data.dropna(subset=['Time'])
        
        print("Processed data:")
        print(data)
        
        return data

    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame(columns=['Time', 'Temperature'])

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Temperature Data Over Time"),
    dcc.Graph(id='temperature-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )
])

@app.callback(Output('temperature-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph(n):
    data = load_data()
    
    if data.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Temperature'],
        mode='lines+markers',
        name='Temperature',
        marker=dict(color='red')
    ))
    
    fig.update_layout(
        title='Temperature Over Time',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        template='plotly_dark',
        xaxis=dict(tickformat='%H:%M:%S')
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
