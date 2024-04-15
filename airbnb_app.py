import pandas as pd
import pymongo
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

st.set_page_config(page_title = "Airbnb Data Visualization",
                   layout = "wide",
                   initial_sidebar_state = "expanded",
                   menu_items={'About': """# The dashboard app is created !"""}
)

st.title("Airbnb Analysis", anchor=None)
st.divider()

selected = option_menu(
    menu_title = None,
    options = ["HOME", "STATISTICS", "ANALYSIS"],
    icons =["house","graph-up-arrow","bar-chart-line"],
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": " #7FD8BE","size":"cover", "width": "200"},
        "icon": {"color": "black", "font-size": "25px"},

        "nav-link": {"font-size": "25px", "text-align": "center", "margin": "-2px", "--hover-color": " #FCEFEF"},
        "nav-link-selected": {"background-color": "#FF7F50",  "font-family": "YourFontFamily"}})
    

df = pd.read_csv(r"C:/Users/dell/Downloads/Data Science/capstone project/airbnb analysis/airbnb_data.csv")

if selected == "HOME":

    st.markdown("##### :blue[INTRODUCTION]")
    st.write("Airbnb is an online marketplace that links those looking for lodging—usually for short stays—with those who wish to rent out their property. A comparatively simple option for hosts to make some money from their house is through Airbnb. Visitors frequently discover that Airbnb apartments are cozier and less expensive than hotels.")
    
    st.markdown("##### :blue[PROBLEM STATEMENT]")
    st.write("In order to obtain insights into pricing variations, availability patterns, and location-based trends, this project will use MongoDB Atlas to analyze Airbnb data, execute data cleaning and preparation, produce interactive geospatial visualizations, and create dynamic plots.")
    
    st.markdown("##### :blue[OBJECTIVE]")
    st.write("The project entails preparing and cleaning the Airbnb dataset, creating an interactive web application called Streamlit for listing exploration, utilizing dynamic visualizations to analyze pricing and availability, and looking into location-based insights.")

if selected == "STATISTICS":
    
    country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()), sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
    price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

    df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
    fig = px.bar(df1,
                 title='Top 10 Property Types',
                 x='Listings',
                 y='property_type',
                 orientation='h',
                 color='property_type',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig, use_container_width=True)

    df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
    fig = px.bar(df2,
                 title='Top 10 Hosts with Highest number of Listings',
                 x='Listings',
                 y='host_name',
                 orientation='h',
                 color='host_name',
                 color_continuous_scale=px.colors.sequential.Agsunset)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
    fig = px.pie(df1,
                 title='Total Listings in each room_types',
                 names='room_type',
                 values='counts',
                 color_discrete_sequence=px.colors.sequential.Rainbow
                 )
    fig.update_traces(textposition='outside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)

    country_df = df.query(query).groupby(['country'], as_index=False)['name'].count().rename(columns={'name': 'Total_Listings'})
    fig = px.choropleth(country_df,
                        title='Total Listings in each country',
                        locations='country',
                        locationmode='country names',
                        color='Total_Listings',
                        color_continuous_scale=px.colors.sequential.Plasma
                        )
    st.plotly_chart(fig, use_container_width=True)


    rev_df = df.groupby('room_type', as_index=False)['review_scores'].mean().sort_values(by='review_scores')


    fig = px.bar(rev_df, x='room_type', y='review_scores', 
                title='Average Review Scores by Room Type', 
                labels={'room_type': 'Room Type', 'review_scores': 'Average Review Scores'}, 
                color='review_scores',
                color_continuous_scale='Viridis')

    st.plotly_chart(fig, use_container_width=True)


    pr_df = df.groupby('room_type', as_index=False)['price'].mean().sort_values(by='price')

    fig = px.bar(pr_df, x='room_type', y='price', title='Average Price by Room Type', labels={'room_type': 'Room Type', 'price': 'Average Price'})
    fig.update_layout(xaxis_title='Room Type', yaxis_title='Average Price')

    st.plotly_chart(fig, use_container_width=True)


if selected == "ANALYSIS":
    st.markdown("## ANALYSIS more about the Airbnb data")
    
    
    country = st.sidebar.multiselect('Select a country',sorted(df.country.unique()),sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.slider('Select price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    
    
    pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
    fig = px.bar(data_frame=pr_df,
                 x='room_type',
                 y='price',
                 color='price',
                 title='Avg price in each Room type'
                )
    st.plotly_chart(fig,use_container_width=True)
   
    
    
    country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                                   locations='country',
                                   color= 'price', 
                                   hover_data=['price'],
                                   locationmode='country names',
                                   size='price',
                                   title= 'Avg price in each country',
                                   color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)
    
    
    st.markdown("#   ")
    st.markdown("#   ")
    
    
    country_df = df.query(query).groupby('country',as_index=False)['availability_365'].mean()
    country_df.availability_365 = country_df.availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                                   locations='country',
                                   color= 'availability_365', 
                                   hover_data=['availability_365'],
                                   locationmode='country names',
                                   size='availability_365',
                                   title= 'Avg Availability in each country',
                                   color_continuous_scale='agsunset'
                        )
    st.plotly_chart(fig,use_container_width=True)

    
    
    availability_by_room_type = df.query(query).groupby('room_type')['availability_365'].mean().reset_index()
    fig = px.pie(availability_by_room_type,
                names='room_type',
                values='availability_365',
                title='Average Availability by Room Type',
                labels={'availability_365': 'Average Availability (in days)', 'room_type': 'Room Type'},
                color='room_type',
                color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True)