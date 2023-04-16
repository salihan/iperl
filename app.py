import streamlit as st
import pandas as pd

def login():
    st.image("logo.png", width=200)
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

    group_nos = df['GROUP_NO'].unique().tolist()
    selected_group_no = st.sidebar.multiselect("Select Group Number", group_nos)

    semesters = df['SEM'].unique().tolist()
    selected_semester = st.sidebar.multiselect("Select Semester", semesters)

    filtered_df = df
    # apply the filters when the button is clicked
    if st.sidebar.button("Apply Filters"):
        filtered_df = df[(df['NAMA KURSUS'].isin(selected_course)) &
                         (df['GROUP_NO'].isin(selected_group_no)) &
                         (df['SEM'].isin(selected_semester))]

    filtered_df['Max'] = filtered_df[['Cognitive', 'Psychomotor', 'Affective']].max(axis=1)
    filtered_df['Skill'] = filtered_df[['Cognitive', 'Psychomotor', 'Affective']].idxmax(axis=1)
    filtered_df['Current Total'] = filtered_df['TEST1'] + filtered_df['CONTINUOUS']
    print(filtered_df.head())

    with st.container():
        col1, col2, col3 = st.columns([2, 2, 4])
        with col1:
            wch_colour_box = (0, 204, 102)
            wch_colour_font = (0, 0, 0)
            fontsize = 18
            valign = "left"
            iconname = "fas fa-users"
            sline = "Number of Students"
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
            # st.write(max_label)
            # st.write(max_value)

        with col2:
            total_marks = filtered_df['TEST1'] + filtered_df['CONTINUOUS']
            average_marks = round(total_marks.mean(),2)

            wch_colour_box = (255,127,80)
            wch_colour_font = (0, 0, 0)
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

        with col3:
            st.bar_chart(filtered_df['GRADE'].value_counts())

    with st.container():
        tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

        with tab1:
            st.header("A cat")
            st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

        with tab2:
            columns_to_display = ['MATRIC_NEW', 'GRADE', 'Max', 'Skill', 'Current Total', 'FINAL', 'GRADE', 'PREDICTED GRADE',
                                  'Cognitive', 'Psychomotor', 'Affective']
            st.dataframe(filtered_df[columns_to_display])

        with tab3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    # display the data as a table with tabs
    # st.write("LSTM Data:")
    # tabs = ["Table", "Line Chart"]
    # selected_tab = st.radio("", tabs)
    # if selected_tab == "Table":
    #     st.dataframe(df)
    # elif selected_tab == "Line Chart":
    #     st.line_chart(df)

# --------------- run --------------
st.set_page_config(layout="wide")
st.sidebar.image("logo.png", width=200)
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




