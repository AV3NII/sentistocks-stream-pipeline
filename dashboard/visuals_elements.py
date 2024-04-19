import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def plot_candlestick_chart(df, ma_options):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Opening_Price'], high=df['Highest_Price'],
                    low=df['Lowest_Price'], close=df['Closing_Price'],
                    name="Candlestick")])

    # Calculate and add moving averages based on selected options
    for ma in ma_options:
        if ma > 0:  # Ensure the moving average window is greater than 0
            ma_column = f'MA{ma}'
            df[ma_column] = df['Closing_Price'].rolling(window=ma).mean()
            fig.add_trace(go.Scatter(x=df['Date'], y=df[ma_column], mode='lines', 
                                     name=f'MA {ma}', 
                                     line=dict(width=1.5)))

    # Adding volume bars to the figure
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume_Traded'], name="Volume", 
                         marker_color='rgba(100, 150, 238, 0.6)', yaxis='y2'))

    # Updating layout to display volume bars
    fig.update_layout(
        #title="Candlestick Chart with Moving Averages and Volume Bars",
        yaxis_title='Price',
        yaxis=dict(domain=[0.3, 1]),
        yaxis2=dict(title='Volume', domain=[0, 0.2], anchor='x'),
        xaxis=dict(type='date', rangeslider=dict(visible=False)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig



def create_correlation_heatmap(df):
    """
    This function creates and displays a correlation heatmap using Plotly.

    Parameters:
    correlation (DataFrame): A pandas DataFrame containing the correlation matrix.

    Returns:
    fig (Figure): A Plotly graph object figure containing the heatmap.
    """
    # Calculating cumulative price changes for the simulated Point and Figure chart
    df['Cumulative Price Changes'] = (df['Closing_Price'] - df['Opening_Price']).cumsum()
    correlation = df[[
        'Lowest_Price', 'Highest_Price', 'Opening_Price', 'Closing_Price', 'Volume_Traded', 'Cumulative Price Changes'
        ]].corr()
    # Generate data for heatmap
    heatmap_data = correlation.values
    x_labels = correlation.columns
    y_labels = correlation.index

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
                        z=heatmap_data,
                        x=x_labels,
                        y=y_labels,
                        colorscale='RdBu',
                        zmin=-1,  # Set the scale of the heatmap to -1 to 1
                        zmax=1))

    fig.update_layout(
       # title='Correlation Heatmap',
        xaxis_nticks=36,
        yaxis_nticks=36,
        xaxis_title="Metric",
        yaxis_title="Metric",
        autosize=True)

    return fig