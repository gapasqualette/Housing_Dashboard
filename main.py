import pandas as pd
import streamlit as st
import numpy as np

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

df = df.rename({df.columns[0]: "AvgArea (sqft)", df.columns[1]: "AvgAge (years)", df.columns[2]: "AvgRooms", df.columns[3]: "AvgBedrooms"}, axis='columns')

df = df.round(2)

df["Street"] = df["Address"].str.split(",").str[0]

df["State"] = df["Address"].str.split().str[-2]

df = df.drop(columns=["Address"], axis=1)

cols_num = ["AvgArea (sqft)", "AvgAge (years)", "AvgRooms", "AvgBedrooms", "Area Population", "Price"]

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
    tile.write(f'**Average Area**: **{np.mean(df['AvgArea (sqft)']):,.2f}** sqft')
    tile.write(f'**Smallest Area**: **{np.min(df["AvgArea (sqft)"]):,.2f}** sqft')
    tile.write(f'**Biggest Area**: **{np.max(df["AvgArea (sqft)"]):,.2f}** sqft')

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

btn_columns = st.columns([45,5,50])
tile_btns = btn_columns[0].container(height=150)
tile2_btns = btn_columns[0].container()
abbr_state = []
code_states = []

for state in us_states_and_territories_military:
    abbr_state.append(f'{state} - {us_states_and_territories_military.get(state,)}')

with tile_btns:
    st.session_state.states_selected = tile_btns.multiselect('Choose the states', abbr_state)

with tile2_btns:
    if st.session_state.states_selected:
        states = [state.split(" - ")[1] for state in st.session_state.states_selected]
        str_states = ' | '.join(sorted(states))
        st.subheader(f'Chosen states: {str_states}', divider=True)
        code_states = [state.split(" - ")[0] for state in st.session_state.states_selected]

        #################### Area Section ##############################
        with st.expander('Area 🌎', expanded=True):
            areas = [df[df["State"] == estado]["AvgArea (sqft)"].mean() for estado in code_states]
            st.write(f'**Average States Area**: **{np.mean(areas):,.2f}** sqft')

            area_fewer = min(code_states, key= lambda estado: df[df["State"] == estado]["AvgArea (sqft)"].values[0])
            area_fewer_data = df[df["State"] == area_fewer].nsmallest(1, "AvgArea (sqft)")
            area_fewer_street = area_fewer_data["Street"].values[0]
            area_fewer_area = area_fewer_data["AvgArea (sqft)"].values[0]
            st.write(f'**Smallest Area** in **{area_fewer_street}** - **{area_fewer}** with **{area_fewer_area:,.2f}** sqft')

            área_max = max(code_states, key= lambda estado: df[df["State"] == estado]["AvgArea (sqft)"].values[0])
            area_max_data = df[df["State"] == área_max].nlargest(1, "AvgArea (sqft)")
            área_max_street = area_max_data["Street"].values[0]
            área_max_area = area_max_data["AvgArea (sqft)"].values[0]
            st.write(f'**Biggest Area** in **{área_max_street}** - **{área_max}** with **{área_max_area:,.2f}** sqft')

        ####################### Population Section #############################
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

        with st.expander('Rooms & Bedrooms 💻', expanded=True):
            rooms = [df[df["State"] == estado]['AvgRooms'].mean() for estado in code_states]
            bedrooms = [df[df["State"] == estado]['AvgBedrooms'].mean() for estado in code_states]
            st.write(f'**Average States Number of Rooms**: **{np.mean(rooms):,.2f}**')
            room_min = min(code_states, key= lambda estado: df[df["State"] == estado]['AvgRooms'].values[0])
            room_min_data = df[df["State"] == room_min].nsmallest(1,'AvgRooms')
            room_min_street = room_min_data['Street'].values[0]
            room_min_room = room_min_data['AvgRooms'].values[0]
            st.write(f'**Smallest Number of Rooms** are in **{room_min_street}** - **{room_min}** with **{room_min_room}** rooms')

            room_max = max(code_states, key= lambda estado: df[df["State"] == estado]['AvgRooms'].values[0])
            room_max_data = df[df["State"] == room_max].nlargest(1,'AvgRooms')
            room_max_street = room_max_data['Street'].values[0]
            room_max_room = room_max_data['AvgRooms'].values[0]
            st.write(f'**Highest Number of Rooms** are in **{room_max_street}** - **{room_max}** with **{room_max_room}** rooms')

            st.write(f'**Average States Number of Bedrooms**: **{np.mean(bedrooms):,.2f}**')
            bedroom_min = min(code_states, key= lambda estado: df[df["State"] == estado]['AvgBedrooms'].values[0])
            bedroom_min_data = df[df["State"] == bedroom_min].nsmallest(1,'AvgBedrooms')
            bedroom_min_street = bedroom_min_data['Street'].values[0]
            bedroom_min_bedrooms = bedroom_min_data['AvgBedrooms'].values[0]
            st.write(f'**Smallest Number of Bedrooms** are in **{bedroom_min_street}** - **{bedroom_min}** with **{bedroom_min_bedrooms}** Bedrooms')

            bedroom_max = min(code_states, key= lambda estado: df[df["State"] == estado]['AvgBedrooms'].values[0])
            bedroom_max_data = df[df["State"] == bedroom_max].nlargest(1,'AvgBedrooms')
            bedroom_max_street = bedroom_max_data['Street'].values[0]
            bedroom_max_bedrooms = bedroom_max_data['AvgBedrooms'].values[0]
            st.write(f'**Highest Number of Bedrooms** are in **{bedroom_max_street}** - **{bedroom_max}** with **{bedroom_max_bedrooms}** Bedrooms')


with btn_columns[1]:
    if st.session_state.states_selected:
        st.markdown('<div class = "vl"></div>', unsafe_allow_html=True)

with btn_columns[2]:
    if st.session_state.states_selected:
        df_filter = df[df["State"].isin(code_states)]
        df_filter = df_filter.groupby("State")[cols_num].mean()

        st.subheader('Areas & Populations Comparisons 📈')
        chart_area = df_filter[['AvgArea (sqft)', 'Area Population']]
        st.line_chart(chart_area, x_label='Data per State', y_label='Average Values')

        st.subheader('Rooms & Bedrooms Comparisons 📉')
        chart_rooms = df_filter[['AvgRooms', 'AvgBedrooms']]
        st.line_chart(chart_rooms, x_label='Data per State', y_label='Average Values')

        st.subheader('Prices Comparisons 📊')
        chart_price = df_filter[['Price']]
        st.bar_chart(chart_price, x_label='Data per State', y_label='Average Values', height=200)
        