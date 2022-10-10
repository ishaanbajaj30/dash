from multiprocessing.sharedctypes import Value
from matplotlib.pyplot import xlabel
import pandas as pd          # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st       # pip install streamlit
from PIL import Image        # pip install Image
import json                  # JSON
from datetime import datetime

img = Image.open('trident.png')

st.set_page_config(page_title="HR Dashboard",
                   page_icon=img, layout="wide")

india_states = json.load(open("states_india.geojson", "r"))


i = 0

idk = [0, 35, 28, 12, 18, 10, 22, 25, 30, 24, 6, 2, 1, 20, 29, 32, 31,
       23, 27, 14, 4, 34, 3, 8, 11, 33, 16, 9, 5, 19, 21, 26, 17, 15, 13, 7]
look_up = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
           6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
for feature in india_states["features"]:
    feature["id"] = idk[i]
    i = i+1

state_id_map = {'Telangana': 0,
                'Andaman & Nicobar Island': 35,
                'Andhra Pradesh': 28,
                'Arunanchal Pradesh': 12,
                'Assam': 18,
                'Bihar': 10,
                'Chhattisgarh': 22,
                'Daman & Diu': 25,
                'Goa': 30,
                'Gujarat': 24,
                'Haryana': 6,
                'Himachal Pradesh': 2,
                'Jammu and Kashmir': 1,
                'Jharkhand': 20,
                'Karnataka': 29,
                'Kerala': 32,
                'Lakshadweep': 31,
                'Madhya Pradesh': 23,
                'Maharashtra': 27,
                'Manipur': 14,
                'Chandigarh': 4,
                'Puducherry': 34,
                'Punjab': 3,
                'Rajasthan': 8,
                'Sikkim': 11,
                'Tamil Nadu': 33,
                'Tripura': 16,
                'Uttar Pradesh': 9,
                'Uttarakhand': 5,
                'West Bengal': 19,
                'Odisha': 21,
                'Dadara & Nagar Havelli': 26,
                'Meghalaya': 17,
                'Mizoram': 15,
                'Nagaland': 13,
                'Delhi': 7}

my_datetime = datetime(1999, 1, 1)
# ---- MAINPAGE ----
col1, col2 = st.columns([1, 20])
with col1:
    st.image(img, width=64)
with col2:
    st.title("HR Dashboard")
st.markdown("##")

st.markdown("""---""")


uploaded_file = st.file_uploader("Choose a file", type='xlsx')

if uploaded_file:
    def get_data_from_excel():
        df = pd.read_excel(
            io=uploaded_file,
            engine="openpyxl",
        )
        return df

    df = get_data_from_excel()

    # ---- SIDEBAR ----

    st.sidebar.header("Please Filter Here:")
    status = st.sidebar.multiselect(
        "Select the Status:",
        options=df["Employee Status"].unique(),
        default=df["Employee Status"].unique()
    )
    gen = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique(),
    )

    payw = st.sidebar.multiselect(
        "Select the Pay Grade:",
        options=df["Pay Grade"].unique(),
        default=df["Pay Grade"].unique(),
    )
    ban = st.sidebar.multiselect(
        "Select the Company Name:",
        options=df["Company Name"].unique(),
        default=df["Company Name"].unique(),
    )
    cna = st.sidebar.multiselect(
        "Select the Business Area Name:",
        options=df["Business Area Name"].unique(),
        default=df["Business Area Name"].unique(),
    )

    df_selection = df.query(
        "`Employee Status` == @status & Gender ==@gen & `Pay Grade` ==@payw & `Company Name`==@ban   & `Business Area Name`==@cna"
    )
    rcheck = st.sidebar.checkbox('Exit Reason Wise')
    if rcheck:
        rea = st.sidebar.multiselect(
            "Select the Exit Reason:",
            options=df["Exit Reason"].unique(),
            default=df["Exit Reason"].unique(),
        )
        df_selection = df.query(
            "`Employee Status` == @status & Gender ==@gen & `Pay Grade` ==@payw & `Company Name`==@ban & `Exit Reason`==@rea  & `Business Area Name`==@cna"
        )
    stcheck = st.sidebar.checkbox('State-Wise')
    if stcheck:
        sa = st.sidebar.multiselect(
            "Select the Sate:",
            options=df["State"].unique(),
            default=df["State"][0]
        )

        df_selection = df_selection.query(
            "`Employee Status` == @status & Gender ==@gen & `Pay Grade` ==@payw & `Company Name`==@ban   & State==@sa & `Business Area Name`==@cna"
        )

    mcheck = st.sidebar.checkbox('Filter according to joining date')
    if mcheck:

        d1 = st.sidebar.date_input(
            "From", min_value=my_datetime)

        d2 = st.sidebar.date_input(
            "To", min_value=my_datetime)
        d1 = datetime.combine(d1, datetime.min.time())
        d2 = datetime.combine(d2, datetime.min.time())
        df_selection['Joining Date'] = pd.to_datetime(
            df_selection['Joining Date'])
        mask = (
            df_selection['Joining Date'] >= d1) & (df_selection['Joining Date'] <= d2)
        df_selection = df_selection.loc[mask]

    dfs1 = df_selection
    # Employee ID correct
    # df_selection['Employee ID'] = df_selection['Employee ID'].astype(
    #     str).apply(lambda x: x.replace('.0', ''))
    # dfs1 = df_selection
    st.dataframe(df_selection)

    # --------CNA-----------
    by_cna = (
        pd.DataFrame(data=dfs1['Company Name'].value_counts())
    )
    df100 = by_cna
    df100.rename({'Company Name': 'Count'}, axis=1, inplace=True)
    df100.index.names = ['Company Name']
    fig_by_cna = px.bar(
        df100,
        y="Count",
        x=df100.index,
        orientation="v",
        title="<b>Company Name Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(df100),
        template="plotly_white",

    )
    fig_by_cna.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)))

    # --------BNA-----------
    by_bna = (
        pd.DataFrame(data=dfs1['Business Area Name'].value_counts())
    )
    df1069 = by_bna
    df1069.rename({'Business Area Name': 'Count'}, axis=1, inplace=True)
    df1069.index.names = ['Business Area Name']
    fig_by_bna = px.bar(
        df1069,
        y="Count",
        x=df1069.index,
        orientation="v",
        title="<b>Business Area Name Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(df1069),
        template="plotly_white",

    )
    fig_by_bna.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_by_cna, use_container_width=True)
    right_column.plotly_chart(fig_by_bna, use_container_width=True)

    # --------EG-----------
    by_eg = (
        pd.DataFrame(data=dfs1['Employee Group'].value_counts())
    )
    df1069 = by_eg
    df1069.rename({'Employee Group': 'Count'}, axis=1, inplace=True)
    df1069.index.names = ['Employee Group']
    fig_by_eg = px.bar(
        df1069,
        y="Count",
        x=df1069.index,
        orientation="v",
        title="<b>Employee Group Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(df1069),
        template="plotly_white",

    )
    fig_by_eg.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
        xaxis={'categoryorder': 'array', 'categoryarray': [
            'Regular', 'Intern', 'Apprentice', 'Cons on Retainership']}
    )

    # -------Cadre Wise--------
    by_pay = (
        pd.DataFrame(data=dfs1['Pay Grade'].value_counts())
    )
    df4 = by_pay
    df4.rename({'Pay Grade': 'Count'},
               axis=1, inplace=True)
    df4.index.names = ['Pay Grade']

    fig_by_pay = px.bar(
        df4,
        y="Count",
        x=by_pay.index,
        orientation="v",
        title="<b>Cadre Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(by_pay),
        template="plotly_white",
    )

    fig_by_pay.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
        xaxis={'categoryorder': 'array', 'categoryarray': [
            'Apprentice', 'Trainee- IL0', 'Karamayogi - IL1', 'Karamayogi - IL2', 'Karamayogi - IL3', 'DC - IL4', 'DC - IL5', 'DC - IL6', 'IB - IL7', 'IB - IL8', 'Cons on Retainership']}

    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_by_eg, use_container_width=True)
    right_column.plotly_chart(fig_by_pay, use_container_width=True)

    # -------EXPERIENCE WISE-------
    bins = [0, 1, 5, 10, 20, 100]
    labels = ['0-1', '1-5', '5-10', '10-20', '20+']
    by_exp = (
        pd.DataFrame(data=pd.cut(
            dfs1['Experience(in years)'], bins=bins, labels=labels, right=True).value_counts())
    )
    df3 = by_exp
    df3.rename({'Experience(in years)': 'Count'},
               axis=1, inplace=True)
    df3.index.names = ['Experience(in years)']
    fig_by_exp = px.bar(
        df3,
        y="Count",
        x=by_exp.index,
        orientation="v",
        title="<b>Experience Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(by_exp),
        template="plotly_white",
    )
    fig_by_exp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)), xaxis={'categoryorder': 'array',  'categoryarray': [
            '0-1', '1-5', '5-10', '10-20', '20+']}
    )

    # -------AGE WISE-------
    bins = [0, 24, 30, 40, 50, 100]
    labels = ['18-24', '24-30', '30-40', '40-50', '50+']
    by_age = (
        pd.DataFrame(data=pd.cut(
            dfs1['Age'], bins=bins, labels=labels, right=True).value_counts())
    )
    df69 = by_age
    df69.rename({'Age': 'Count'},
                axis=1, inplace=True)
    df69.index.names = ['Age(in years)']

    fig_by_age = px.bar(
        df69,
        y="Count",
        x=df69.index,
        orientation="v",
        title="<b>Age Wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(df69),
        template="plotly_white",

    )
    fig_by_age.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
        xaxis={'categoryorder': 'array',  'categoryarray': [
            '18-24', '24-30', '30-40', '40-50', '50+']}
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_by_exp, use_container_width=True)
    right_column.plotly_chart(fig_by_age, use_container_width=True)

    # -------GENDER WISE-------
    sales_by_product_line = (
        pd.DataFrame(data=dfs1['Gender'].value_counts())
    )
    df1 = sales_by_product_line
    df1.rename({'Gender': 'Count'}, axis=1, inplace=True)
    df1.index.names = ['Gender']

    fig_product_sales = px.pie(
        df1, values=df1['Count'], names=df1.index, title='<b>Gender Wise</b>',  color=df1.index, color_discrete_map={  # replaces default color mapping by value
            "M": "#27806E", "F": "#FBAC12"
        },
    )
    # -------MARITAL STATUS-------
    by_marital_status = (
        pd.DataFrame(data=dfs1['Marital Status'].value_counts())
    )
    df2 = by_marital_status
    df2.rename({'Marital Status': 'Count'}, axis=1, inplace=True)
    df2.index.names = ['Marital Status']
    fig_by_marital_status = px.pie(
        df2, values=df2['Count'], names=df2.index, color=df2.index, title='<b>Marital Status</b>', color_discrete_map={  # replaces default color mapping by value
            "Single": "#27806E", "Married": "#FBAC12"
        },)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(
        fig_product_sales, use_container_width=True)
    right_column.plotly_chart(fig_by_marital_status, use_container_width=True)

    # -------Exit Reason-------
    by_exit_reason = (
        pd.DataFrame(data=dfs1['Exit Reason'].value_counts())
    )
    df9 = by_exit_reason
    df9.rename({'Exit Reason': 'Count'}, axis=1, inplace=True)
    df9.index.names = ['Exit Reason']
    fig_by_exit_reason = px.pie(
        df9, values=df9['Count'], names=df9.index, color=df9.index, title='<b>Exit Reason</b>', color_discrete_map={  # replaces default color mapping by value
            "Absenteeism": "#FBAC12", "Better Career Prospects": "#0DD254", "Domestic Problem": "#27806E", "Deteriorating Health": "#CB8411"
        },)

    # ------Month Wise---------------
    dfs1['month'] = dfs1['Exit Date'].dt.month_name()
    by_month = (
        pd.DataFrame(data=dfs1['month'].value_counts())
    )
    dfm = by_month
    dfm.rename({'month': 'Count'}, axis=1, inplace=True)
    dfm.index.names = ['Month']
    fig_by_month = px.bar(
        dfm,
        y="Count",
        x=dfm.index,
        orientation="v",
        title="<b>Exit Date Month wise</b>",
        text_auto=True,
        color_discrete_sequence=["#FBAC12"] * len(dfm),
        template="plotly_white",

    )
    fig_by_month.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
        xaxis={'categoryorder': 'array', 'categoryarray': [
            'January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November', 'December']}
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_by_exit_reason, use_container_width=True)
    right_column.plotly_chart(fig_by_month, use_container_width=True)

    # ----State Wise--------
    by_state = (
        pd.DataFrame(data=dfs1['State'].value_counts())
    )
    dfst = by_state
    dfst.rename({'State': 'Count'}, axis=1, inplace=True)
    dfst["auxi"] = dfst.index
    dfst["id"] = dfst["auxi"].apply(lambda x: state_id_map[x])
    # st.dataframe(dfst)

    fig = px.choropleth(
        dfst,
        locations="id",
        geojson=india_states,
        color="Count",
        hover_name="auxi",
        hover_data=["Count"],
        title="<b>State Wise</b>",
    )
    fig.update_geos(fitbounds="locations", visible=False, resolution=50,
                    showcountries=True, countrycolor="Black",
                    showsubunits=True, subunitcolor="Blue")
    fig.add_scattergeo(
        geojson=india_states,
        locations=dfst['id'],
        text=dfst['Count'],
        # featureidkey="properties.NAME_3",
        mode='text',
        textfont=dict(
            family="Monospace",
            size=11,
            color="White"
        ))

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig, use_container_width=True)

    # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
             # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
