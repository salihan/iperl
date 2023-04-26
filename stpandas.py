import streamlit as st
import pandas as pd
import streamlit_pandas as sp
from st_aggrid import AgGrid, GridOptionsBuilder

@st.cache_data
def load_data():
    df = pd.read_csv(file)
    df['Max'] = df[['Cognitive', 'Psychomotor', 'Affective']].max(axis=1)
    df['Skill'] = df[['Cognitive', 'Psychomotor', 'Affective']].idxmax(axis=1)
    df['Current Total'] = df['TEST1'] + df['CONTINUOUS']
    po1 = df['TEST1'] + df['FINAL']
    po2 = df['CONTINUOUS'] * 0.95
    po3 = po2.mean() * 0.5
    return df

file = "Salihan.csv"
df = load_data()

create_data = {"NAMA KURSUS": "multiselect",
                "SEM": "multiselect"}
columns_to_display = ['Skill', 'TEST1', 'CONTINUOUS', 'Current Total',
                                  'FINAL', 'GRADE', 'PREDICTED GRADE', 'Cognitive', 'Psychomotor', 'Affective']

all_widgets = sp.create_widgets(df, create_data,
                                ignore_columns=['FAKULTI', 'MATRIC_NEW', 'KOD KURSUS', 'GENDER',
                                                'FINAL', 'GRADE', 'PREDICTED GRADE',
                                                'Cognitive', 'Psychomotor', 'Affective'])

res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
# st.dataframe(df[columns_to_display])

#---------------- agrid ----------------
# Create a GridOptionsBuilder object to customize the appearance of the table
gob = GridOptionsBuilder.from_dataframe(res)
gob.configure_pagination()

# Display the paginated table using st_aggrid
grid_response = AgGrid(res, gridOptions=gob.build(), height=500)

# Get the selected rows from the table
selected_rows = grid_response[columns_to_display]
#---------------------------------------

st.header("Result DataFrame")
# st.write(res[columns_to_display])


