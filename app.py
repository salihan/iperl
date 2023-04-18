import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import itables.options as opt
from itables import show

def color_func(val):
    if val > 70:
        color = 'green'
    elif val >= 40:
        color = 'yellow'
    else:
        color = 'red'
    return f'background-color: {color}'


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

def lecturer_dashboard(df):
    # filter the data by course, group number, and semester
    courses = df['NAMA KURSUS'].unique().tolist()
    selected_course = st.sidebar.multiselect("Select Course", courses)

    # group_nos = df['GROUP_NO'].unique().tolist()
    # selected_group_no = st.sidebar.multiselect("Select Group Number", group_nos)

    semesters = df['SEM'].unique().tolist()
    selected_semester = st.sidebar.multiselect("Select Semester", semesters)

    filtered_df = df
    # apply the filters when the button is clicked
    if st.sidebar.button("Apply Filters"):
        filtered_df = df[(df['NAMA KURSUS'].isin(selected_course)) &
                         (df['SEM'].isin(selected_semester))] # & (df['GROUP_NO'].isin(selected_group_no))


    filtered_df['Max'] = filtered_df[['Cognitive', 'Psychomotor', 'Affective']].max(axis=1)
    filtered_df['Skill'] = filtered_df[['Cognitive', 'Psychomotor', 'Affective']].idxmax(axis=1)
    filtered_df['Current Total'] = filtered_df['TEST1'] + filtered_df['CONTINUOUS']
    po1 = filtered_df['TEST1'] + filtered_df['FINAL']
    po2 = filtered_df['CONTINUOUS'] * 0.95
    po3 = po2.mean() * 0.5

    # drop data that got null grade
    filtered_df = filtered_df.dropna(subset=['GRADE'])

    c_plus_and_below = filtered_df[filtered_df['GRADE'].str.contains('C\+|C|D\+|D|F')]
    num_c_plus_and_below = round(( len(c_plus_and_below) / len(filtered_df) ) * 100 ,2)
    print(type(c_plus_and_below))

    if selected_course:
        # st.subheader(f"Course Name: {selected_course}. Semester: {selected_semester}. % at risk: :orange[{num_c_plus_and_below}]")
        st.markdown(
            f"<h4>Course Name: {selected_course[0]}. Semester: {selected_semester[0]}. &nbsp; &nbsp; &nbsp; <span style='background-color: orange; color: white;'>{num_c_plus_and_below}% at risk</span></h4>",
            unsafe_allow_html=True)

    # ----------- tab --------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Student at-risk", "All", "Graph", "PO Analysis", "Engagement"])

    with tab1:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                wch_colour_box = (128, 128, 0)
                wch_colour_font = (255, 255, 255)
                fontsize = 18
                valign = "left"
                iconname = "fas fa-users"
                sline = "Student Count"
                lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
                i = c_plus_and_below.shape[0]

                htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                                          {wch_colour_box[1]}, 
                                                                          {wch_colour_box[2]}, 0.75); 
                                                    color: rgb({wch_colour_font[0]}, 
                                                               {wch_colour_font[1]}, 
                                                               {wch_colour_font[2]}, 0.75); 
                                                    font-size: {fontsize}px; 
                                                    border-radius: 7px; 
                                                    padding-left: 12px; 
                                                    padding-top: 18px; 
                                                    padding-bottom: 18px; 
                                                    line-height:25px;'>
                                                    <i class='{iconname} fa-xs'></i> {i}
                                                    </style><BR><span style='font-size: 14px; 
                                                    margin-top: 0;'>{sline}</style></span></p>"""

                st.markdown(lnk + htmlstr, unsafe_allow_html=True)

                st.write(
                    """
                    <style>
                    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
                        gap: 0.5rem;
                    }
                    [data-testid="stMetricDelta"] svg {
                        display: none;
                    }
                    [data-testid="stMetricValue"] {
                        font-size: 20px;
                        color: #008080;
                    }
                    </style>
                    """, unsafe_allow_html=True,
                )
                st.metric(label="% Attainment PO1", value=round(po1.mean(), 2))
                st.metric(label="% Attainment PO2", value=round(po2.mean(), 2))
                st.metric(label="% Attainment PO3", value=round(po3, 2))
                # st.write(f"% Attainment PO1: {round(po1.mean(),2)}")
                # st.write(f"% Attainment PO2: {round(po2.mean(), 2)}")
                # st.write(f"% Attainment PO3: {round(po3, 2)}")

            with col2:
                total_marks = c_plus_and_below['TEST1'] + c_plus_and_below['CONTINUOUS']
                average_marks = round(total_marks.mean(), 2)

                wch_colour_box = (102, 51, 153)
                wch_colour_font = (255, 255, 255)
                fontsize = 18
                valign = "left"
                iconname = "fas fa-wave-square"
                sline = "Average Marks"
                lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
                i = average_marks

                htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                              {wch_colour_box[1]}, 
                                                              {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                   {wch_colour_font[1]}, 
                                                   {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 18px; 
                                        padding-bottom: 18px; 
                                        line-height:25px;'>
                                        <i class='{iconname} fa-xs'></i> {i}
                                        </style><BR><span style='font-size: 14px; 
                                        margin-top: 0;'>{sline}</style></span></p>"""

                st.markdown(lnk + htmlstr, unsafe_allow_html=True)

                # st.markdown(f"""*Assessment Info*
                #             \nTest1: {round(filtered_df['TEST1'].mean(),2)}
                #             \nContinuous Assessment: {round(filtered_df['CONTINUOUS'].mean(),2)}
                #             \nFinal: {round(filtered_df['FINAL'].mean(),2)}""")
                st.write("_Assessment Info:_")
                st.write(f"Test1: :blue[{round(filtered_df['TEST1'].mean(), 2)}]")
                st.write(f"Continuous Assessment: :blue[{round(filtered_df['CONTINUOUS'].mean(), 2)}]")
                st.write(f"Final: :blue[{round(filtered_df['FINAL'].mean(), 2)}]")
                # st.write("<div style='text-align: center;'>Centered text</div>", unsafe_allow_html=True)

            with col3:
                # st.bar_chart(filtered_df['GRADE'].value_counts())
                sorted_counts = filtered_df['GRADE'].value_counts().sort_index()
                fig = px.bar(sorted_counts, x=sorted_counts.index, y=sorted_counts.values, color=sorted_counts.index)
                fig.update_layout(title='Grade Distribution', height=350, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig)

    with tab2:
        with st.container():
            po1 = filtered_df['TEST1'] + filtered_df['FINAL']
            po2 = filtered_df['CONTINUOUS'] * 0.95
            po3 = po2.mean() * 0.5
            # drop data that got null grade
            filtered_df = filtered_df.dropna(subset=['GRADE'])

            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                wch_colour_box = (128,128,0)
                wch_colour_font = (255,255,255)
                fontsize = 18
                valign = "left"
                iconname = "fas fa-users"
                sline = "Student Count"
                lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
                i = filtered_df.shape[0]

                htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                                          {wch_colour_box[1]}, 
                                                                          {wch_colour_box[2]}, 0.75); 
                                                    color: rgb({wch_colour_font[0]}, 
                                                               {wch_colour_font[1]}, 
                                                               {wch_colour_font[2]}, 0.75); 
                                                    font-size: {fontsize}px; 
                                                    border-radius: 7px; 
                                                    padding-left: 12px; 
                                                    padding-top: 18px; 
                                                    padding-bottom: 18px; 
                                                    line-height:25px;'>
                                                    <i class='{iconname} fa-xs'></i> {i}
                                                    </style><BR><span style='font-size: 14px; 
                                                    margin-top: 0;'>{sline}</style></span></p>"""

                st.markdown(lnk + htmlstr, unsafe_allow_html=True)

                st.write(
                    """
                    <style>
                    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
                        gap: 0.5rem;
                    }
                    [data-testid="stMetricDelta"] svg {
                        display: none;
                    }
                    [data-testid="stMetricValue"] {
                        font-size: 20px;
                        color: #008080;
                    }
                    </style>
                    """, unsafe_allow_html=True,
                )
                st.metric(label="% Attainment PO1", value=round(po1.mean(), 2))
                st.metric(label="% Attainment PO2", value=round(po2.mean(), 2))
                st.metric(label="% Attainment PO3", value=round(po3, 2))
                # st.write(f"% Attainment PO1: {round(po1.mean(),2)}")
                # st.write(f"% Attainment PO2: {round(po2.mean(), 2)}")
                # st.write(f"% Attainment PO3: {round(po3, 2)}")

            with col2:
                total_marks = filtered_df['TEST1'] + filtered_df['CONTINUOUS']
                average_marks = round(total_marks.mean(), 2)

                wch_colour_box = (102,51,153)
                wch_colour_font = (255,255,255)
                fontsize = 18
                valign = "left"
                iconname = "fas fa-wave-square"
                sline = "Average Marks"
                lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
                i = average_marks

                htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                              {wch_colour_box[1]}, 
                                                              {wch_colour_box[2]}, 0.75); 
                                        color: rgb({wch_colour_font[0]}, 
                                                   {wch_colour_font[1]}, 
                                                   {wch_colour_font[2]}, 0.75); 
                                        font-size: {fontsize}px; 
                                        border-radius: 7px; 
                                        padding-left: 12px; 
                                        padding-top: 18px; 
                                        padding-bottom: 18px; 
                                        line-height:25px;'>
                                        <i class='{iconname} fa-xs'></i> {i}
                                        </style><BR><span style='font-size: 14px; 
                                        margin-top: 0;'>{sline}</style></span></p>"""

                st.markdown(lnk + htmlstr, unsafe_allow_html=True)

                # st.markdown(f"""*Assessment Info*
                #             \nTest1: {round(filtered_df['TEST1'].mean(),2)}
                #             \nContinuous Assessment: {round(filtered_df['CONTINUOUS'].mean(),2)}
                #             \nFinal: {round(filtered_df['FINAL'].mean(),2)}""")
                st.write("_Assessment Info:_")
                st.write(f"Test1: :blue[{round(filtered_df['TEST1'].mean(), 2)}]")
                st.write(f"Continuous Assessment: :blue[{round(filtered_df['CONTINUOUS'].mean(), 2)}]")
                st.write(f"Final: :blue[{round(filtered_df['FINAL'].mean(), 2)}]")
                # st.write("<div style='text-align: center;'>Centered text</div>", unsafe_allow_html=True)


            with col3:
                # st.bar_chart(filtered_df['GRADE'].value_counts())
                sorted_counts = filtered_df['GRADE'].value_counts().sort_index()
                fig = px.bar(sorted_counts, x=sorted_counts.index, y=sorted_counts.values, color=sorted_counts.index)
                fig.update_layout(title='Grade Distribution', height=300, margin=dict(l=0, r=10, t=30, b=0))
                st.plotly_chart(fig)

        with st.container():
            columns_to_display = ['Skill', 'TEST1', 'CONTINUOUS', 'Current Total',
                                  'FINAL', 'GRADE', 'PREDICTED GRADE', 'Cognitive', 'Psychomotor', 'Affective']
            #create a copy of the filtered dataframe
            styled_df = filtered_df[columns_to_display].copy()

            # ----------- block ni jadi tapi berat ------------
            # apply the color_total function to the 'Current Total' column
            styled_df = styled_df.style.applymap(color_func, subset=['Current Total'])
            # # # st.table(styled_df) # satu
            # div = f"<div style='height: 200px; overflow-y: scroll'>{styled_df.render()}</div>"
            # st.markdown(div, unsafe_allow_html=True)
            #-------------------------------------------------

            styled_df = styled_df.format(
                {'TEST1': '{:.2f}', 'CONTINUOUS': '{:.2f}', 'Current Total': '{:.2f}', 'FINAL': '{:.2f}',
                 'Cognitive': '{:.2f}', 'Psychomotor': '{:.2f}', 'Affective': '{:.2f}'})

            st.write(styled_df)

            # st.table(styled_df)
            # AgGrid(styled_df)
            # create AgGrid configuration
            # ag_grid_config = {
            #     'enable_pagination': True,
            #     'page_size': 10,
            #     'fit_columns_on_grid_load': True
            # }
            # AgGrid(styled_df, **ag_grid_config)

            # st.dataframe(filtered_df[columns_to_display])
            # st.markdown(filtered_df[columns_to_display].style.hide(axis="index").to_html(), unsafe_allow_html=True)

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
st.set_page_config(page_title='AIPerLA', layout='wide', page_icon=':rocket:')
st.markdown("""
        <style>
               .css-1544g2n {
                  margin-top: -75px;
                }
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    st.sidebar.image("images/logo.png", width=200)
    st.sidebar.title("Navigation")

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login()
    else:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.experimental_rerun()
        else:
            # read in the data from the CSV file
            df = pd.read_csv("Salihan.csv")
            if st.session_state.role == "admin":
                admin_dashboard()
            elif st.session_state.role == "lecturer":
                lecturer_dashboard(df)
            else:
                student_dashboard()




