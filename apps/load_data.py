import pandas as pd
import os

def load_data():
    base_path = os.path.join(os.path.dirname(__file__), '../data')

    df_customer = pd.read_csv(os.path.join(base_path, 'olist_customers_dataset.csv'))
    df_geoloc = pd.read_csv(os.path.join(base_path, 'olist_geolocation_dataset.csv'))
    df_order_item = pd.read_csv(os.path.join(base_path, 'olist_order_items_dataset.csv'))
    df_payment = pd.read_csv(os.path.join(base_path, 'olist_order_payments_dataset.csv'))
    df_order_review = pd.read_csv(os.path.join(base_path, 'olist_order_reviews_dataset.csv'))
    df_order = pd.read_csv(os.path.join(base_path, 'olist_orders_dataset.csv'))
    df_product = pd.read_csv(os.path.join(base_path, 'olist_products_dataset.csv'))
    df_seller = pd.read_csv(os.path.join(base_path, 'olist_sellers_dataset.csv'))
    df_product_category = pd.read_csv(os.path.join(base_path, 'product_category_name_translation.csv'))

    return {
        'customer': df_customer,
        'geoloc': df_geoloc,
        'order_item': df_order_item,
        'payment': df_payment,
        'order_review': df_order_review,
        'order': df_order,
        'product': df_product,
        'seller': df_seller,
        'product_category': df_product_category
    }
