import pandas as pd
import mysql.connector
from pymongo import MongoClient

# Database configurations
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DATABASE = 'ecommerce'

NOSQL_DB_URL = 'mongodb://localhost:27017/'
NOSQL_DB_NAME = 'ecommerce_aggregated'

# Connect to MySQL database
mysql_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

# MongoDB client
mongo_client = MongoClient(NOSQL_DB_URL)
mongo_db = mongo_client[NOSQL_DB_NAME]

def extract_data():
    queries = {
        'customers': "SELECT * FROM customers",
        'orders': "SELECT * FROM orders",
        'order_items': "SELECT * FROM order_items",
        'products': "SELECT * FROM products",
        'categories': "SELECT * FROM categories",
        'reviews': "SELECT * FROM reviews"
    }
    data = {}
    cursor = mysql_connection.cursor(dictionary=True)
    for table, query in queries.items():
        cursor.execute(query)
        data[table] = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return data

def clean_data(data):
    for table in data:
        data[table].drop_duplicates(inplace=True)
        data[table].dropna(inplace=True)
    return data

def transform_data(data):
    df = data['customers']
    df_orders = data['orders']
    df_order_items = data['order_items']
    df_products = data['products']
    df_categories = data['categories']
    df_reviews = data['reviews']
    df = df.merge(df_orders, on='customer_id')
    df = df.merge(df_order_items, on='order_id')
    df = df.merge(df_products, on='product_id')
    df = df.merge(df_categories, on='category_id')
    df = df.merge(df_reviews, on=['product_id', 'customer_id'], how='left')
    
    # Aggregate data
    agg_df = df.groupby('customer_id').agg({
        'total_amount': 'sum',
        'order_id': 'count',
        'price': 'mean',
        'quantity': 'sum',
        'rating': 'mean'
    }).reset_index()
    
    agg_df.columns = [
        'customer_id', 'total_amount_spent', 'total_orders', 
        'average_order_value', 'total_products_ordered', 'average_rating'
    ]
    agg_df = agg_df.merge(data['customers'], on='customer_id')
    agg_df = agg_df.merge(data['customers'], on='customer_id')
    return agg_df, df

def load_data(agg_df, insights):
    mongo_db.aggregated_data.insert_many(agg_df.to_dict('records'))
    mongo_db.insights.insert_many(insights)

def generate_insights(df, all_df):
    insights = []

    # Ensure total_amount_spent is numeric
    df['total_amount_spent'] = pd.to_numeric(df['total_amount_spent'])

    # Top 5 customers by total amount spent
    top_customers = df.nlargest(5, 'total_amount_spent')[['customer_id', 'total_amount_spent']].to_dict('records')
    insights.append({'insight': 'Top 5 customers by total amount spent', 'data': top_customers})

    print(all_df['product_id'])

    # Top 5 products by number of orders
    top_products = all_df.groupby('product_id').agg({'order_id': 'count'}).nlargest(5, 'order_id').reset_index().to_dict('records')
    insights.append({'insight': 'Top 5 products by number of orders', 'data': top_products})

    # Average rating of products by category
    avg_rating = all_df.groupby('category_id')['rating'].mean().reset_index().to_dict('records')
    insights.append({'insight': 'Average rating of products by category', 'data': avg_rating})

    # # Monthly sales trend
    monthly_sales = all_df.groupby(pd.Grouper(key='order_date', freq='M'))['total_amount'].sum().reset_index().to_dict('records')
    insights.append({'insight': 'Monthly sales trend', 'data': monthly_sales})

    return insights


if __name__ == "__main__":
    data = extract_data()
    data = clean_data(data)
    agg_df, all_df = transform_data(data)
    insights = generate_insights(agg_df, all_df)
    load_data(agg_df, insights)
