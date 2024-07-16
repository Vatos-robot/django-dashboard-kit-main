import pandas as pd
import  matplotlib.pyplot as plt
import io
import base64


def get_delivered_orders_by_month(orders_df):
    colonne_date = 'order_purchase_timestamp'  # Colonne contenant les dates des commandes
    colonne_statut = 'order_status'            # Colonne contenant les statuts des commandes


    delivered_orders = orders_df[orders_df[colonne_statut] == 'delivered']


    delivered_orders[colonne_date] = pd.to_datetime(delivered_orders[colonne_date])


    delivered_orders['year_month'] = delivered_orders[colonne_date].dt.to_period('M')


    nombre_commandes_par_mois = delivered_orders['year_month'].value_counts().sort_index()
    nombre_commandes_par_mois.index = nombre_commandes_par_mois.index.to_timestamp()

    # Tracer le graphique
    plt.figure(figsize=(12, 6))
    plt.plot(nombre_commandes_par_mois.index, nombre_commandes_par_mois.values, marker='o')
    plt.title('Nombre de commandes livrées par mois pour chaque année')
    plt.xlabel('Date (Année-Mois)')
    plt.ylabel('Nombre de commandes livrées')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


def top_cat(order_df, product_df):
    colonne_id_produit_orders = 'product_id' 
    colonne_id_produit_products = 'product_id' 
    colonne_nom_produit = 'product_category_name'  
    colonne_prix = 'price'  
    merged_df = pd.merge(order_df, product_df, left_on=colonne_id_produit_orders, right_on=colonne_id_produit_products)
    merged_df['total_revenue'] = merged_df[colonne_prix]
    product_counts = merged_df[colonne_nom_produit].value_counts()
    revenue_by_category = merged_df.groupby(colonne_nom_produit)['total_revenue'].sum().sort_values(ascending=False)
    top_categories_df = pd.DataFrame({
        'category_name': product_counts.index,
        'number_of_sales': product_counts.values
    })
    top_categories_revenue_df = pd.DataFrame({
        'category_name': revenue_by_category.index,
        'total_revenue': revenue_by_category.values
    })

    top_10_categories_df = top_categories_df.head(10)
    top_10_revenue_df = top_categories_revenue_df.head(10)

    return top_10_categories_df, top_10_revenue_df

