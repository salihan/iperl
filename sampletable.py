import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Sample data
data = pd.read_csv("Salihan.csv")
df = pd.DataFrame(data)

# Set default values for sorting and pagination
default_sort = 'MATRIC_NEW'
default_page_size = 2

# Sidebar filters
with st.sidebar:
    search_term = st.text_input("Search by COUNTRY:")
    page_size = st.selectbox("Page size:", [2, 5, 10, 20], index=0)
    sort = st.selectbox("Sort by:", ['COUNTRY', 'GENDER', 'GRADE'], index=0)

# Sort the dataframe
df.sort_values(sort, inplace=True)

# Filter by search term
if search_term:
    df = df[df['Name'].str.contains(search_term, case=False)]

# Paginate the results
total_rows = df.shape[0]
num_pages = int(total_rows / page_size)
if total_rows % page_size > 0:
    num_pages += 1

page_num = st.sidebar.number_input("Page", min_value=1, max_value=num_pages, value=1, step=1)
start = (page_num - 1) * page_size
end = start + page_size

# Create a Streamlit app and add the table to it
with st.container():
    st.write('<h2>Employee Information</h2>', unsafe_allow_html=True)
    css = """
        .table-container {
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        table.dataframe {
            font-size: 16px;
            border-collapse: collapse;
            margin-bottom: 0;
        }
        th {
            background-color: #007bff;
            color: #fff;
        }
        td {
            background-color: #fff;
        }
        tbody tr:hover {
            background-color: #e9ecef;
        }
        """
    components.html(f"<style>{css}</style><div class='table-container'>", height=10)
    if search_term:
        st.write(f"Results for search term '{search_term}':")
    else:
        st.write("All Results:")
    st.write(df.iloc[start:end])
    components.html("</div>", height=10)
