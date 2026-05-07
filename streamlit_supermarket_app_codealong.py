import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title('Supermarkt Sales Dashboard')
st.write('''This Dashboard allows us to explore supermarket sales data using interactive strelit widgets''')

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data #it will be saved inside the internal memory and won't run everytime we run the code
def load_data():

    df = pd.read_csv("https://raw.githubusercontent.com/data-bootcamp-v4/data/main/supermarket_sales.csv")

# also possible on local machine
    #df = pd.read_csv(r"path\file_name.csv")
    
    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header('Filters')

#City
selected_city = st.sidebar.selectbox('Select a city', 
                                    options = ['All'] + list(df['City'].unique()))


#Gender
selected_gender = st.sidebar.radio('Select a gender', 
                                    options = list(df['Gender'].unique()) + ['All'])


#Rating
min_rating = st.sidebar.slider('Minimum rating', 
                              min_value = 0,
                              max_value = 10,
                              value = 5,
                              step = 1)

#Payment Method
selected_payment = st.sidebar.multiselect('Select payment methods',
                                         options = df['Payment'].unique(), 
                                         default = df['Payment'].unique())
if len(selected_payment) == 0:
    selected_payment = df['Payment'].unique()

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------
filtered_df = df.copy()

#City
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['City'] == selected_city]

#Gender
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

#Rating
filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]

#Payment Method
filtered_df = filtered_df = filtered_df[filtered_df['Payment'].isin(selected_payment)] 

if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()
# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.header('Summary Statistics (KPIs)')

#total sales $
total_sales = round(filtered_df['Total'].sum(), 2)

#avg rating
avg_rating = round(filtered_df['Rating'].mean(), 2)

#total transactions
total_transactions = filtered_df['Invoice ID'].nunique()

#avg price transactions
avg_transaction = round(filtered_df['Total'].mean(),2)

#best product line
best_product_line = filtered_df['Product line'].value_counts().index[0]

#first row
col1, col2 = st.columns(2) #can have more columns if necessary

with col1: 
    st.metric('Total Sales:', f'${total_sales:,.2f}')

with col2:
    st.metric('Average Rating:', avg_rating)

#second row
col3, col4 = st.columns(2) #can have more columns if necessary

with col3: 
    st.metric('Total Transactions:', total_transactions)

with col4:
    st.metric('Average Price per Transaction:', f'${avg_transaction:,.2f}')

#third row
st.write('### Top product line')
st.success(best_product_line)
    
# st.markdown ("HTML/CSS")

# ---------------------------------------------------
# DATAFRAME SECTION
# ---------------------------------------------------
st.header('Raw Data')

show_data = st.checkbox('Show dataset')

if show_data:
    st.dataframe(filtered_df)
    
st.divider()
# ---------------------------------------------------
# SALES OVER TIME
# ---------------------------------------------------
st.header('Sales Over Time')

sales_over_time = filtered_df.groupby(filtered_df['Date'].dt.date)['Total'].sum()
fig, ax = plt.subplots(figsize=(10,5))

ax.plot(sales_over_time)
ax.set_title('Sales over time')
ax.set_xlabel('Date')
ax.set_ylabel('Total Sales')
ax.tick_params(axis='x', rotation=45)

st.pyplot(fig) #to show the plot from python code
st.divider()
# ---------------------------------------------------
# SALES BY PRODUCT LINE
# ---------------------------------------------------



# ---------------------------------------------------
# TOP 5 TRANSACTIONS
# ---------------------------------------------------
st.header('Top 5 Transactions')

top_transactions = filtered_df.sort_values(by = 'Total', ascending=False).head()

st.table(top_transactions[['Invoice ID', 'City', 'Product line', 'Total', 'Rating']])
st.divider()
# ---------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------
st.markdown('''
<h2 style='color:#4CAF50;'>
Dashboard Loaded successfully!
</h2>
''', unsafe_allow_html=True)


