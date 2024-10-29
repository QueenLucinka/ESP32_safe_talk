import dash  # Import Dash library for creating web applications
from dash import dcc, html  # Import Dash components for layout
from dash.dependencies import Input, Output  # Import Input and Output for callbacks
import pandas as pd  # Import pandas for data manipulation
import plotly.graph_objs as go  # Import Plotly for graphing
import json  # Import JSON module for parsing JSON data
import pytz  # Import pytz for timezone handling

# Path to your sensor data file
file_path = r"C:/Users/lucia/OneDrive/Dokument/PlatformIO/Projects/ESP32_SAFE_TALK/src/sensor_data.txt"

def load_data():
    """Load data from the specified file and return a DataFrame with the temperature and time."""
    try:
        # Open the sensor data file for reading
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Read all lines from the file
        
        # Initialize lists to hold the time and temperature data
        times = []
        temperatures = []
        
        # Process each line in the file
        for line in lines:
            try:
                # Parse the line as JSON to extract temperature and time
                entry = json.loads(line)
                temperature = entry['data'][0][0]  # Extract the temperature value
                time_label = entry['labels'][0]  # Extract the time label
                
                # Append the extracted values to the respective lists
                temperatures.append(temperature)
                times.append(time_label)
            except json.JSONDecodeError:
                # Print any lines that failed to decode
                print(f"Failed to decode JSON: {line.strip()}")  
        
        # Create a DataFrame from the lists of time and temperature
        data = pd.DataFrame({
            'Time': times,
            'Temperature': temperatures
        })

        # Convert the 'Time' column to datetime format
        data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S', errors='coerce')
        
        # Define the timezone for your location (e.g., Stockholm)
        local_tz = pytz.timezone('Europe/Stockholm')

        # Localize the 'Time' column to UTC and convert to local timezone
        data['Time'] = data['Time'].dt.tz_localize('UTC').dt.tz_convert(local_tz)

        # Drop rows with NaT (Not a Time) in 'Time' to avoid plotting errors
        data = data.dropna(subset=['Time'])
        
        # Print the processed data for debugging purposes
        print("Processed data:")
        print(data)
        
        return data  # Return the DataFrame containing the processed data

    except Exception as e:
        # Print any errors encountered while reading the file
        print(f"Error reading the file: {e}")
        return pd.DataFrame(columns=['Time', 'Temperature'])  # Return an empty DataFrame with the correct columns

# Create a Dash application instance
app = dash.Dash(__name__)

# Define the layout of the Dash application
app.layout = html.Div(children=[
    html.H1("Temperature Data Over Time"),  # Main title of the app
    dcc.Graph(id='temperature-graph'),  # Placeholder for the temperature graph
    dcc.Interval(
        id='interval-component',  # Component to trigger updates at regular intervals
        interval=60*1000,  # Update every minute (in milliseconds)
        n_intervals=0  # Initial number of intervals
    )
])

# Define a callback function to update the graph based on the data
@app.callback(Output('temperature-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph(n):
    data = load_data()  # Load the latest data from the file
    
    # Check if data is available
    if data.empty:
        return go.Figure()  # Return an empty figure if there is no data

    # Create the figure for the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Time'],  # Set the x-axis data to time
        y=data['Temperature'],  # Set the y-axis data to temperature
        mode='lines+markers',  # Display both lines and markers on the graph
        name='Temperature',  # Legend entry for this trace
        marker=dict(color='red')  # Set the marker color to red
    ))
    
    # Update layout settings for the figure
    fig.update_layout(
        title='Temperature Over Time',  # Title of the graph
        xaxis_title='Time',  # Label for the x-axis
        yaxis_title='Temperature (°C)',  # Label for the y-axis
        template='plotly_dark',  # Use a dark theme for the plot
        xaxis=dict(tickformat='%H:%M:%S')  # Format for the X-axis ticks to show time
    )
    
    return fig  # Return the figure to be displayed

# Run the application if this script is executed
if __name__ == '__main__':
    app.run_server(debug=True)  # Start the Dash server in debug mode
