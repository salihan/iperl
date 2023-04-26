import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_pandas as sp
from common import set_page_container_style
from st_aggrid import AgGrid, GridOptionsBuilder
import json
import numpy as np

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df['Max'] = df[['Cognitive', 'Psychomotor', 'Affective']].max(axis=1)
    df['Skill'] = df[['Cognitive', 'Psychomotor', 'Affective']].idxmax(axis=1)
    df['Current Total'] = df['TEST1'] + df['CONTINUOUS']
    return df

def login():
    st.image("images/logo.png", width=200)
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.success("Logged in as admin")
            st.session_state.logged_in = True
            st.session_state.role = "admin"
        elif username == "student" and password == "pelajar123":
            st.success("Logged in as student")
            st.session_state.logged_in = True
            st.session_state.role = "student"
        elif username == "lecturer" and password == "cikgu123":
            st.success("Logged in as lecturer")
            st.session_state.logged_in = True
            st.session_state.role = "lecturer"
        else:
            st.error("Incorrect username or password")

def student_dashboard():
    st.image("logo.png", width=200)
    st.title("Student Dashboard")
    st.write("Welcome, student!")
    st.write("This is your dashboard.")
    st.write("You do not have access to any admin features.")

def admin_dashboard():
    st.image("logo.png", width=200)
    st.title("Admin Dashboard")
    st.write("Welcome, admin!")
    st.write("This is your dashboard.")
    st.write("You have access to all features.")

def lecturer_dashboard():
    file = "Salihan.csv"
    df = load_data(file)
    columns_to_display = ['MATRIC_NEW', 'Skill', 'TEST1', 'CONTINUOUS', 'Current Total',
                          'FINAL', 'GRADE', 'PREDICTED GRADE', 'Cognitive', 'Psychomotor', 'Affective']
    create_data = {"KOD KURSUS": "multiselect",
                   "SEM": "multiselect",
                   "GROUP_NO": "multiselect"}
    all_widgets = sp.create_widgets(df, create_data, ignore_columns=[
        'FAKULTI', 'MATRIC_NEW', 'GENDER', 'AGE', 'MARITAL_STATUS', 'COUNTRY',
        'TYPE_SPONSOR', 'NAMA KURSUS', 'TEST1',
        'CONTINUOUS', 'FINAL', 'GRADE', 'PREDICTED GRADE', 'Cognitive',
        'Psychomotor', 'Affective', 'ENGAGE_W8', 'ENGAGE_W20', 'RESOURCES_W8',
        'RESOURCES_W20', 'FORUM_W8', 'FORUM_W20', 'GPA', 'CGPA', 'Max', 'Skill',
        'Current Total'])

    print(all_widgets)
    with st.container():
        # get the selected values of the widgets
        selected_values = {}
        for widget in all_widgets:
            if widget[1] == 'multiselect':
                selected_values[widget[0]] = st.session_state[widget[0]]
            elif widget[1] == 'selectbox':
                selected_values[widget[0]] = st.session_state[widget[0]]

        # Convert any numpy integer values to Python integer values
        # selected_values = {k: v.tolist() if isinstance(v, np.integer) else v for k, v in selected_values.items()}
        # selected_values_str = "   ".join(
        #     [f"{k.capitalize()}: {', '.join(map(str, v))}" for k, v in selected_values.items()])
        # st.markdown(f"<h3>Selected Values: {selected_values_str}</h3>", unsafe_allow_html=True)

        # Remove any key-value pairs where the value is an empty list
        selected_values = {k: v for k, v in selected_values.items() if v}
        # Convert any numpy integer values to Python integer values
        selected_values = {k: v.tolist() if isinstance(v, np.integer) else v for k, v in selected_values.items()}
        # selected_values_str = "   ".join([f"{k.capitalize()}: {', '.join(v)}" for k, v in selected_values.items()])
        selected_values_str = ";   ".join([f"{k.capitalize()}: {', '.join(str(vv) for vv in v)}" for k, v in selected_values.items()])

        st.markdown(f"<h4>{selected_values_str}</h4>", unsafe_allow_html=True)

        # st.write('Selected Values: ', json.dumps(selected_values, indent=4, default=str))


    # ----------- tab --------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Student at-risk", "All", "Graph", "PO Analysis", "Engagement"])

    with tab1:
        # filter the DataFrame using boolean indexing with isin()
        below_cplus_grades = ['C', 'C-', 'D+', 'D', 'D-', 'F']
        filtered_df = df[(df['Current Total'] > 0) & (df['GRADE'].isin(below_cplus_grades))]

        res_df = sp.filter_df(filtered_df, all_widgets)
        res_length = len(res_df)

        po1 = res_df['TEST1'] + res_df['FINAL']
        po2 = res_df['CONTINUOUS'] * 0.95
        po3 = po2.mean() * 0.5

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.metric(label="% Attainment PO1", value=round(po1.mean(), 2))
                st.metric(label="% Attainment PO2", value=round(po2.mean(), 2))
                st.metric(label="% Attainment PO3", value=round(po3, 2))

            with col2:
                st.write("_Assessment Info:_")
                st.write(f"Test1: :blue[{round(res_df['TEST1'].mean(), 2)}]")
                st.write(f"Continuous Assessment: :blue[{round(res_df['CONTINUOUS'].mean(), 2)}]")
                st.write(f"Final: :blue[{round(res_df['FINAL'].mean(), 2)}]")

            with col3:
                # st.markdown("<h4 style='text-align: center; color: Turquoise;'>Grade Distribution</h4>", unsafe_allow_html=True)
                sorted_counts = res_df['GRADE'].value_counts().sort_index()
                fig = px.bar(sorted_counts, x=sorted_counts.index, y=sorted_counts.values, color=sorted_counts.index)
                fig.update_layout(title="Grade Distribution", title_x=0.4, xaxis_title="Grade", yaxis_title="Count",
                                  height=300, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        # apply red color to the Current Total column
        res_df_style = res_df[columns_to_display].style \
            .apply(lambda x: ['color: red' if v < 40 else '' for v in x], subset=['Current Total']) \
            .format({'Current Total': '{:.2f}', 'TEST1': '{:.2f}', 'CONTINUOUS': '{:.2f}', 'FINAL': '{:.2f}',
                     'Cognitive': '{:.2f}', 'Psychomotor': '{:.2f}', 'Affective': '{:.2f}'}) \
            .hide_index()

        # display the DataFrame with the style
        with st.container():
            if res_length > 0:
                st.write(res_df_style)
            else:
                st.write("No record found.")
            st.caption(f"_Record found: {res_length}_")

    with tab2:
        res_alldf = sp.filter_df(df, all_widgets)
        res_alllength = len(res_alldf)

        po1 = res_alldf['TEST1'] + res_alldf['FINAL']
        po2 = res_alldf['CONTINUOUS'] * 0.95
        po3 = po2.mean() * 0.5

        with st.container():

            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                st.metric(label="% Attainment PO1", value=round(po1.mean(), 2))
                st.metric(label="% Attainment PO2", value=round(po2.mean(), 2))
                st.metric(label="% Attainment PO3", value=round(po3, 2))

            with col2:
                st.write("_Assessment Info:_")
                st.write(f"Test1: :blue[{round(res_alldf['TEST1'].mean(), 2)}]")
                st.write(f"Continuous Assessment: :blue[{round(res_alldf['CONTINUOUS'].mean(), 2)}]")
                st.write(f"Final: :blue[{round(res_alldf['FINAL'].mean(), 2)}]")

            with col3:
                sorted_counts = res_alldf['GRADE'].value_counts().sort_index()
                fig = px.bar(sorted_counts, x=sorted_counts.index, y=sorted_counts.values, color=sorted_counts.index)
                fig.update_layout(title="Grade Distribution", title_x=0.4, xaxis_title="Grade", yaxis_title="Count",
                                  height=300, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            res_alldf.index.name = "Anonymous"
            if res_alllength > 0:
                st.write(res_alldf[columns_to_display])
            else:
                st.write("No record found.")
            st.caption(f"_Record found: {res_alllength}_")

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    with tab4:
        st.header("Tab 4")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    with tab5:
        st.header("Tab 5")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



# --------------- run --------------
st.set_page_config(
    page_title='AIPerLA',
    layout='wide',
    page_icon=':rocket:'
)
st.markdown("""
        <style>
               .css-1544g2n {
                  margin-top: -75px;
                }      
                .css-6wvkk3 {
                  margin-top: -75px;
                }          
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

set_page_container_style(
        max_width = 1100, max_width_100_percent = True,
        padding_top = 0, padding_right = 10, padding_left = 5, padding_bottom = 10
)

if __name__ == '__main__':
    st.sidebar.empty()
    st.sidebar.image("images/aiperla-side.png", width=200)
    st.sidebar.title("Options")

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login()
    else:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.experimental_rerun()
        else:
            if st.session_state.role == "admin":
                admin_dashboard()
            elif st.session_state.role == "lecturer":
                lecturer_dashboard()
            else:
                student_dashboard()




