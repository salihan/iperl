import streamlit as st
import pandas as pd
# from streamlit_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# Sample data
data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Henry', 'Ivy'],
    'Age': [23, 34, 45, 32, 29, 54, 38, 27, 41],
    'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'New York', 'Paris', 'London', 'Sydney']
})

# Define the AgGrid component
grid_height = 400
grid_width = '100%'

data_lenght = len(data)

pagination_size = 10

with st.expander("View Data"):
    grid = AgGrid(
        data=data,
        height=grid_height,
        width=grid_width,
        pagination=True,
        page_size=pagination_size,
        keep_multiindex=False,
        allow_download=False,
        fit_columns_on_grid_load=True,
        )

