import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit_pandas as sp
import numpy as np
from common import set_page_container_style
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridOptionsBuilder
import json


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
    columns_to_display = ['Skill', 'TEST1', 'CONTINUOUS', 'Current Total',
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

    # print(all_widgets)
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Student at-risk", "All", "Graphs", "PO Analysis", "Engagement"])

    res_alldf = sp.filter_df(df, all_widgets)
    res_alllength = len(res_alldf)

    po1 = res_alldf['TEST1'] + res_alldf['FINAL']
    po2 = res_alldf['CONTINUOUS'] * 0.95
    po3 = po2.mean() * 0.5

    sort_order = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'M']

    # ---------------- tab1 -------------------
    with tab1:
        # filter the DataFrame using boolean indexing with isin()
        below_cplus_grades = ['C', 'C-', 'D+', 'D', 'D-', 'F']
        filtered_df = df[(df['Current Total'] > 0) & (df['GRADE'].isin(below_cplus_grades))]

        res_df = sp.filter_df(filtered_df, all_widgets)
        res_length = len(res_df)

        po1risk = res_df['TEST1'] + res_df['FINAL']
        po2risk = res_df['CONTINUOUS'] * 0.95
        po3risk = po2.mean() * 0.5

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.metric(label="% Attainment PO1", value=round(po1risk.mean(), 2))
                st.metric(label="% Attainment PO2", value=round(po2risk.mean(), 2))
                st.metric(label="% Attainment PO3", value=round(po3risk, 2))

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
        # res_df_style = res_df.set_index('MATRIC_NEW')[columns_to_display]
        # print(res_df_style)
        res_df_style = res_df[columns_to_display].style \
            .apply(lambda x: ['color: red' if v < 40 else '' for v in x], subset=['Current Total']) \
            .format({'Current Total': '{:.2f}', 'TEST1': '{:.2f}', 'CONTINUOUS': '{:.2f}', 'FINAL': '{:.2f}',
                     'Cognitive': '{:.2f}', 'Psychomotor': '{:.2f}', 'Affective': '{:.2f}'}) \
            .hide(axis="index")

        with st.container():
            if res_length > 0:
                # res_df_style.index.name = 'Anonymous'
                st.write(res_df_style)
            else:
                st.write("No record found.")
            st.caption(f"_Record found: {res_length}_")

    # ---------------- tab2 -------------------
    with tab2:
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
            columns_to_display = ['Skill', 'TEST1', 'CONTINUOUS', 'Current Total',
                                  'FINAL', 'GRADE', 'PREDICTED GRADE', 'Cognitive', 'Psychomotor', 'Affective']
            # res_alldf.index.name = "Anonymous"
            
            if res_alllength > 0:
                res_alldf.set_index('MATRIC_NEW')[columns_to_display]
                # st.write(res_alldf[columns_to_display])
            else:
                st.write("No record found.")
            st.caption(f"_Record found: {res_alllength}_")

    # ---------------- tab3 -------------------
    with tab3:
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

                res_alldf['GRADE'] = pd.Categorical(res_alldf['GRADE'], categories=sort_order, ordered=True)
                res_alldf['PREDICTED GRADE'] = pd.Categorical(res_alldf['PREDICTED GRADE'], categories=sort_order,
                                                              ordered=True)

                sorted_counts = res_alldf['GRADE'].value_counts().sort_index()
                sorted_predicted = res_alldf['PREDICTED GRADE'].value_counts().sort_index()

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Bar(x=sorted_counts.index, y=sorted_counts.values, name="Actual Grade"))
                fig.add_trace(go.Scatter(x=sorted_predicted.index, y=sorted_predicted.values, mode="lines+markers",
                                         name="Predicted Grade"), secondary_y=True)

                fig.update_layout(title="Actual vs Predicted Grade", title_x=0.4, xaxis_title="Grade",
                                  yaxis_title="Actual Grade Count", yaxis2_title="Predicted Grade Count",
                                  height=300, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                fig = make_subplots(rows=1, cols=3, subplot_titles=("TEST1", "Continuous Assessment", "Final"))

                fig.add_trace(
                    go.Histogram(x=res_alldf["TEST1"], nbinsx=20, name="TEST1 Marks", marker_color="CORAL"),
                    row=1, col=1
                )

                fig.add_trace(
                    go.Histogram(x=res_alldf["CONTINUOUS"], nbinsx=20, name="Continuous Assessment", marker_color="OLIVEDRAB"),
                    row=1, col=2
                )

                fig.add_trace(
                    go.Histogram(x=res_alldf["FINAL"], nbinsx=20, name="FINAL", marker_color="DARKCYAN"),
                    row=1, col=3
                )

                fig.update_layout(height=300, title_text="Marks Distribution", title_x=0.45, legend=dict(x=0.7, y=1.1), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # sorted_counts = res_alldf['GRADE'].value_counts().sort_index()
                # fig = px.pie(sorted_counts, values=sorted_counts.values, names=sorted_counts.index, sort_order=False,
                #              category_orders={"names": sort_order})
                # fig.update_layout(title="Grade Distribution", title_x=0.4, height=300,
                #                   margin=dict(l=0, r=10, t=30, b=0))
                # st.plotly_chart(fig, use_container_width=True)

                counts = res_alldf['GRADE'].value_counts()
                # create a new dataframe with sorted index based on the sort order
                sorted_counts = pd.DataFrame({'GRADE': counts.index, 'COUNT': counts.values}).sort_values\
                    ('GRADE', key=lambda x: [sort_order.index(i) for i in x])
                # plot the pie chart
                fig = px.pie(sorted_counts, values='COUNT', names='GRADE', title='Grade Distribution')
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(title_x=0.25, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ---------------- tab4 -------------------
    with tab4:
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
                res_alldf['GRADE'] = pd.Categorical(res_alldf['GRADE'], categories=sort_order, ordered=True)
                res_alldf['PREDICTED GRADE'] = pd.Categorical(res_alldf['PREDICTED GRADE'], categories=sort_order,
                                                              ordered=True)

                sorted_counts = res_alldf['GRADE'].value_counts().sort_index()
                sorted_predicted = res_alldf['PREDICTED GRADE'].value_counts().sort_index()

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Bar(x=sorted_counts.index, y=sorted_counts.values, name="Actual Grade"))
                fig.add_trace(go.Scatter(x=sorted_predicted.index, y=sorted_predicted.values, mode="lines+markers",
                                         name="Predicted Grade"), secondary_y=True)

                fig.update_layout(title="Actual vs Predicted Grade", title_x=0.4, xaxis_title="Grade",
                                  yaxis_title="Actual Grade Count", yaxis2_title="Predicted Grade Count",
                                  height=300, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            tab1, tab2, tab3 = st.tabs(["Cognitive", "Psychomotor", "Affective"])

            with tab1:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    fig = px.histogram(res_alldf, x='Cognitive', nbins=20, title='Cognitive Marks Distribution')
                    fig.update_layout(xaxis_title='Marks', yaxis_title='Count',
                                      margin=dict(l=0, r=10, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    cog_filter = res_alldf['Cognitive'] < 50
                    cog_filtered_df = res_alldf[cog_filter]
                    cog_filtered_table = cog_filtered_df.set_index('MATRIC_NEW')[['Cognitive']]
                    st.write("**Fail Cognitive Attainment**")
                    st.write(cog_filtered_table, height=200)
                    st.caption(f"Fail found: {len(cog_filtered_df)}")

                with col3:
                    # filter the dataframe
                    cog_filter2 = res_alldf['Cognitive'] >= 50
                    cog_filtered_df2 = res_alldf[cog_filter2]
                    cog_filtered_table2 = cog_filtered_df2.set_index('MATRIC_NEW')[['Cognitive']]
                    st.write("**Pass Cognitive Attainment**")
                    st.write(cog_filtered_table2, height=200)
                    st.caption(f"Pass found: {len(cog_filtered_df2)}")

            with tab2:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    fig = px.histogram(res_alldf, x='Psychomotor', nbins=20, title='Psychomotor Marks Distribution')
                    fig.update_layout(xaxis_title='Marks', yaxis_title='Count',
                                      margin=dict(l=0, r=10, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    cog_filter = res_alldf['Psychomotor'] < 50
                    cog_filtered_df = res_alldf[cog_filter]
                    cog_filtered_table = cog_filtered_df.set_index('MATRIC_NEW')[['Psychomotor']]
                    st.write("**Fail Psychomotor Attainment**")
                    st.write(cog_filtered_table, height=200)
                    st.caption(f"Fail found: {len(cog_filtered_df)}")

                with col3:
                    # filter the dataframe
                    cog_filter2 = res_alldf['Psychomotor'] >= 50
                    cog_filtered_df2 = res_alldf[cog_filter2]
                    cog_filtered_table2 = cog_filtered_df2.set_index('MATRIC_NEW')[['Psychomotor']]
                    st.write("**Pass Psychomotor Attainment**")
                    st.write(cog_filtered_table2, height=200)
                    st.caption(f"Pass found: {len(cog_filtered_df2)}")

            with tab3:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    fig = px.histogram(res_alldf, x='Affective', nbins=20, title='Affective Marks Distribution')
                    fig.update_layout(xaxis_title='Marks', yaxis_title='Count',
                                      margin=dict(l=0, r=10, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    cog_filter = res_alldf['Affective'] < 50
                    cog_filtered_df = res_alldf[cog_filter]
                    cog_filtered_table = cog_filtered_df.set_index('MATRIC_NEW')[['Affective']]
                    st.write("**Fail Affective Attainment**")
                    st.write(cog_filtered_table, height=200)
                    st.caption(f"Fail found: {len(cog_filtered_df)}")

                with col3:
                    # filter the dataframe
                    cog_filter2 = res_alldf['Affective'] >= 50
                    cog_filtered_df2 = res_alldf[cog_filter2]
                    cog_filtered_table2 = cog_filtered_df2.set_index('MATRIC_NEW')[['Affective']]
                    st.write("**Pass Affective Attainment**")
                    st.write(cog_filtered_table2, height=200)
                    st.caption(f"Pass found: {len(cog_filtered_df2)}")


    # ---------------- tab5 -------------------
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




