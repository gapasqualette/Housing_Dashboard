import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
us_states_and_territories_military = {
    # 50 U.S. States
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",

    # U.S. Territories
    "DC": "District of Columbia", "AS": "American Samoa", "GU": "Guam",
    "MP": "Northern Mariana Islands", "PR": "Puerto Rico", "VI": "U.S. Virgin Islands",
    "FM": "Federated States of Micronesia", "MH": "Marshall Islands", "PW": "Palau",

    # Military Addresses (APO/FPO/DPO)
    "AA": "Armed Forces Americas",  
    "AE": "Armed Forces Europe, the Middle East, and Canada",  
    "AP": "Armed Forces Pacific"
}

st.set_page_config("Housing Dashboard", layout='wide')

if 'states_selected' not in st.session_state:
    st.session_state.states_selected = []

df = pd.read_csv("housing.csv")
df.dropna(inplace=True)

df = df.rename(
    {
        df.columns[0]: "area_income", 
        df.columns[1]: "house_age", 
        df.columns[2]: "avg_rooms", 
        df.columns[3]: "avg_bedrooms"
        }, 
        axis='columns'
    )

df = df.round(2)

df["Street"] = df["Address"].str.split(",").str[0]

df["State"] = df["Address"].str.split().str[-2]

df['n_people'] = df['avg_bedrooms'].astype(int) + 1

df['income_house'] = np.round(df['area_income'] / df['n_people'], 2)

# Income Range
df['income_range'] = pd.cut(
    df['area_income'],
    bins=[0, 60000, 72500, 85000, np.inf],
    labels=['Low', 'Medium', 'High', 'Rich']
)

df['prop_appr'] = np.round(df['Price'] / df['house_age'], 2)

df = df.drop(["Address"], axis=1)

st.header(f"**USA Housing Dashboard** - **Housing.csv On Kaggle**", anchor=False, divider=True)

st.markdown(
        """
        <style>
        .vl {
            border-left: 3px solid white;
            height: 1100px; /* Altura da linha */
            position: absolute;
            left: 50%; /* Alinhamento horizontal */
            margin-left: -1px; /* Centralização */
            top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
)

column = st.columns(4)

with column[0]:
    tile = column[0].container(height='stretch', border=True)
    tile.subheader("Area Stats 🌎", divider=True)
    tile.write(f'**Average Income**: **US${np.mean(df['area_income']):,.2f}**')
    tile.write(f'**Smallest Income**: **US${np.min(df["area_income"]):,.2f}**')
    tile.write(f'**Biggest Income**: **US${np.max(df["area_income"]):,.2f}**')

with column[1]:
    tile2 = column[1].container(height='stretch', border=True)
    tile2.subheader("Population Stats 👨‍👩‍👧‍👦", divider=True)
    tile2.write(f'**Average Population**: **{int(np.mean(df["Area Population"]))}** people')
    tile2.write(f'**Smallest Population**: **{int(np.min(df["Area Population"]))}** people')
    tile2.write(f'**Biggest Population**: **{int(np.max(df["Area Population"]))}** people')

with column[2]:
    tile3 = column[2].container(height='stretch', border=True)
    tile3.subheader("Price Stats 💵", divider=True)
    tile3.write(f'**Average Price**: **US${round(np.mean(df["Price"]),2):,.2f}**')
    tile3.write(f'**Smallest Price**: **US${round(np.min(df["Price"]),2):,.2f}**')
    tile3.write(f'**Biggest Price**: **US${round(np.max(df["Price"]),2):,.2f}**')

with column[3]:
    tile4 = column[3].container(height='stretch', border=True)
    tile4.subheader("Housing Number per State 🏡", divider=True)
    tile4.write(f'**Most Housing**: **{us_states_and_territories_military.get(df["State"].value_counts().idxmax(), 'Unknown')}** - **{df["State"].value_counts().max()}**')
    tile4.write(f'**Fewest Housing**: **{us_states_and_territories_military.get(df["State"].value_counts().idxmin(), 'Unknown')}** - **{df["State"].value_counts().min()}** ')

st.divider()

abbr_state = []
code_states = []

for state in us_states_and_territories_military:
    abbr_state.append(f'{state} - {us_states_and_territories_military.get(state,)}')

st.session_state.states_selected = st.multiselect('Choose the states', abbr_state)

if len(st.session_state.states_selected) > 1:
    states = [state.split(" - ")[1] for state in st.session_state.states_selected]
    str_states = ' | '.join(sorted(states))
    st.subheader(f'Chosen states: {str_states}', divider=True)
    code_states = [state.split(" - ")[0] for state in st.session_state.states_selected]
    cols_expander = st.columns(2)

    #################### Income Section ##############################
    with cols_expander[0]:
        with st.expander('Area 🌎', expanded=True):
            income = [df[df["State"] == estado]["area_income"].mean() for estado in code_states]
            st.write(f'**Average States Income**: **US${np.mean(income):,.2f}**')

            income_fewer = min(code_states, key= lambda estado: df[df["State"] == estado]["area_income"].values[0])
            income_fewer_data = df[df["State"] == income_fewer].nsmallest(1, "area_income")
            income_fewer_street = income_fewer_data["Street"].values[0]
            income_fewer_area = income_fewer_data["area_income"].values[0]
            st.write(f'**Smallest Income** in **{income_fewer_street}** - **{income_fewer}** with **US${income_fewer_area:,.2f}**')

            income_max = max(code_states, key= lambda estado: df[df["State"] == estado]["area_income"].values[0])
            income_max_data = df[df["State"] == income_max].nlargest(1, "area_income")
            income_max_street = income_max_data["Street"].values[0]
            income_max_area = income_max_data["area_income"].values[0]
            st.write(f'**Biggest Income** in **{income_max_street}** - **{income_max}** with **US${income_max_area:,.2f}**')

        with st.expander('Price 💵', expanded=True):
            prices = [df[df["State"] == estado]['Price'].mean() for estado in code_states]
            st.write(f'**Average States Price**: **US${np.mean(prices): ,.2f}**')

            price_fewer = min(code_states, key= lambda estado: df[df["State"] == estado]["Price"].values[0])
            price_fewer_data = df[df["State"] == price_fewer].nsmallest(1, "Price")
            price_fewer_street = price_fewer_data["Street"].values[0]
            price_fewer_price = price_fewer_data["Price"].values[0]
            st.write(f'**Smallest Price** in **{price_fewer_street}** - **{price_fewer}** costing **US${price_fewer_price: ,.2f}**')

            price_max = max(code_states, key= lambda estado: df[df["State"] == estado]["Price"].values[0])
            price_max_data = df[df["State"] == price_max].nlargest(1, "Price")
            price_max_street = price_max_data['Street'].values[0]
            price_max_price = price_max_data['Price'].values[0]
            st.write(f'**Biggest Population** in **{price_max_street}** - **{price_max}** costing **US${price_max_price: ,.2f}**')


        ####################### Population Section #############################
    with cols_expander[1]:   
        with st.expander('Population 👨‍👩‍👧‍👦', expanded=True):
            populations = [df[df["State"] == estado]['Area Population'].mean() for estado in code_states]
            st.write(f'**Average Areas Population**: **{int(np.mean(populations))}**')

            pop_fewer : str = min(code_states, key= lambda estado: df[df["State"] == estado]["Area Population"].values[0])
            pop_fewer_data = df[df["State"] == pop_fewer].nsmallest(1, "Area Population")
            pop_fewer_street= pop_fewer_data["Street"].values[0]
            pop_fewer_pop = int(pop_fewer_data["Area Population"].values[0])
            st.write(f'**Smallest Population** in **{pop_fewer_street}** - **{pop_fewer}** with **{pop_fewer_pop}** People')

            pop_max = max(code_states, key= lambda estado: df[df["State"] == estado]["Area Population"].values[0])
            pop_max_data = df[df["State"] == pop_max].nlargest(1, "Area Population")
            pop_max_street = pop_max_data["Street"].values[0]
            pop_max_pop = int(pop_max_data["Area Population"].values[0])
            st.write(f'**Biggest Population** in **{pop_max_street}** - **{pop_max}** with **{pop_max_pop}** People')

        ######################## Price Section ##################################
        
        with st.expander('Rooms & Bedrooms 💻', expanded=True):
            rooms = [df[df["State"] == estado]['avg_rooms'].mean() for estado in code_states]
            bedrooms = [df[df["State"] == estado]['avg_bedrooms'].mean() for estado in code_states]
            st.write(f'**Average States Number of Rooms**: **{np.mean(rooms):,.2f}**')
            room_min = min(code_states, key= lambda estado: df[df["State"] == estado]['avg_rooms'].values[0])
            room_min_data = df[df["State"] == room_min].nsmallest(1,'avg_rooms')
            room_min_street = room_min_data['Street'].values[0]
            room_min_room = room_min_data['avg_rooms'].values[0]
            st.write(f'**Smallest Number of Rooms** are in **{room_min_street}** - **{room_min}** with **{room_min_room}** rooms')

            room_max = max(code_states, key= lambda estado: df[df["State"] == estado]['avg_rooms'].values[0])
            room_max_data = df[df["State"] == room_max].nlargest(1,'avg_rooms')
            room_max_street = room_max_data['Street'].values[0]
            room_max_room = room_max_data['avg_rooms'].values[0]
            st.write(f'**Highest Number of Rooms** are in **{room_max_street}** - **{room_max}** with **{room_max_room}** rooms')

            st.write(f'**Average States Number of Bedrooms**: **{np.mean(bedrooms):,.2f}**')
            bedroom_min = min(code_states, key= lambda estado: df[df["State"] == estado]['avg_bedrooms'].values[0])
            bedroom_min_data = df[df["State"] == bedroom_min].nsmallest(1,'avg_bedrooms')
            bedroom_min_street = bedroom_min_data['Street'].values[0]
            bedroom_min_bedrooms = bedroom_min_data['avg_bedrooms'].values[0]
            st.write(f'**Smallest Number of Bedrooms** are in **{bedroom_min_street}** - **{bedroom_min}** with **{bedroom_min_bedrooms}** Bedrooms')

            bedroom_max = min(code_states, key= lambda estado: df[df["State"] == estado]['avg_bedrooms'].values[0])
            bedroom_max_data = df[df["State"] == bedroom_max].nlargest(1,'avg_bedrooms')
            bedroom_max_street = bedroom_max_data['Street'].values[0]
            bedroom_max_bedrooms = bedroom_max_data['avg_bedrooms'].values[0]
            st.write(f'**Highest Number of Bedrooms** are in **{bedroom_max_street}** - **{bedroom_max}** with **{bedroom_max_bedrooms}** Bedrooms')



df_filter = df[df["State"].isin(code_states)]
df_filter_avg = df_filter.groupby('State')[['area_income', 'house_age', 'avg_rooms', 'avg_bedrooms', 'Area Population', 'Price', 'prop_appr']].mean().round(2)

if len(st.session_state.states_selected) > 1:
    st.subheader('Plots', divider=True)    
    btn_columns = st.columns([49,2,49])
    with btn_columns[0]:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(df_filter_avg, x='State', y='Price', linewidth = 1.5, edgecolor = 'black', )
        ax.set_title('Plot 1 - Average Price per State & Number of Rooms')
        ax.set_xlabel('States')
        ax.set_ylabel('Average Price')
        ax.set_ylim(bottom=df_filter_avg['Price'].min() - 50000)
        ax2 = ax.twinx()
        sns.lineplot(df_filter_avg, x='State', y='avg_rooms', marker='o', linewidth = 3, color = 'red')

        ax2.set_ylabel('Average Number of Rooms', color = 'red')

        with st.container(height='stretch', width='stretch', border=True):
            st.pyplot(fig)

        df_profile = df_filter.groupby(['State', 'income_range']).size().reset_index(name='count_profiles')

        fig, ax = plt.subplots(figsize=(7,3))
        sns.barplot(df_profile, x='State', y='count_profiles', linewidth = 1.25, edgecolor = 'black', hue='income_range', palette='pastel')
        ax.set_xlabel('State')
        ax.set_ylabel('Profile Count')
        ax.set_title('Plot 3 - Profile Count per State')

        with st.container(height='stretch', width='stretch', border=True):
            st.pyplot(fig)

    with btn_columns[1]:
        st.html(
        """<div style="
            border-left: 3px solid red;
            height: 1000px;
            margin: auto;
            width: 0;
            "></div>
        """ 
    )

    with btn_columns[2]:
        fig, ax = plt.subplots(figsize=(7,3))
        sns.barplot(df_filter_avg, x='State', y='area_income', linewidth = 1.5, edgecolor = 'black', )
        ax.set_title('Plot 2 - Average Income per State & Number of Rooms')
        ax.set_xlabel('States')
        ax.set_ylabel('Average Income')
        ax.set_ylim(bottom=df_filter_avg['area_income'].min() - 5000)
        ax2 = ax.twinx()
        sns.lineplot(df_filter_avg, x='State', y='avg_rooms', marker='o', linewidth = 3, color = 'red')

        ax2.set_ylabel('Average Number of Rooms', color = 'red')

        with st.container(height='stretch', width='stretch', border=True):
            st.pyplot(fig)
        #####

        #####

        fig, ax = plt.subplots(figsize=(7,3))
        sns.barplot(df_filter_avg, x='State', y='prop_appr', linewidth = 2, edgecolor = 'black', palette='pastel')
        ax.set_xlabel('State')
        ax.set_ylabel('Property Appreciation')
        ax.set_title('Plot 4 - Property Appreciation (PRICE / AGE) per State')
        ax.set_ylim(df_filter_avg['prop_appr'].min() - 10000)

        with st.container(height='stretch', width='stretch', border=True):
            st.pyplot(fig)