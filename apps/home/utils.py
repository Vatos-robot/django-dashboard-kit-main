import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import random 


def get_delivered_orders_by_month(orders_df):
    colonne_date = 'order_purchase_timestamp'  # Colonne contenant les dates des commandes
    colonne_statut = 'order_status'            # Colonne contenant les statuts des commandes


    delivered_orders = orders_df[orders_df[colonne_statut] == 'delivered']


    delivered_orders[colonne_date] = pd.to_datetime(delivered_orders[colonne_date])


    delivered_orders['year_month'] = delivered_orders[colonne_date].dt.to_period('M')


    nombre_commandes_par_mois = delivered_orders['year_month'].value_counts().sort_index()
    nombre_commandes_par_mois.index = nombre_commandes_par_mois.index.to_timestamp()

    # Utiliser seaborn pour améliorer l'apparence du graphique
    sns.set(style="whitegrid")
    plt.figure(figsize=(16, 8))

    # Tracer le graphique avec une couleur violette
    sns.lineplot(x=nombre_commandes_par_mois.index, y=nombre_commandes_par_mois.values, marker='o', color='purple')

    # Personnaliser les titres et étiquettes avec une couleur violette
    plt.title('Nombre de commandes livrées par mois pour chaque année', fontsize=20, color='purple')
    plt.xlabel('Date (Année-Mois)', fontsize=15, color='purple')
    plt.ylabel('Nombre de commandes livrées', fontsize=15, color='purple')
    plt.xticks(rotation=45, fontsize=12, color='purple')
    plt.yticks(fontsize=12, color='purple')

    # Ajouter une grille et personnaliser les couleurs
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

    # Ajuster la mise en page pour une meilleure apparence
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



def get_orders_by_town(orders_df, customers_df):
# Charger les fichiers CSV
    customers_df
    orders_df

    # Spécifiez les noms des colonnes
    colonne_client_id = 'customer_id'  # Colonne pour l'ID client
    colonne_ville = 'customer_city'     # Colonne pour la ville du client
    colonne_order_id = 'order_id'       # Colonne pour l'ID de la commande

    # Fusionner les DataFrames sur customer_id
    merged_df = pd.merge(orders_df, customers_df, on=colonne_client_id)

    # Compter le nombre de commandes par ville
    command_counts = merged_df.groupby(colonne_ville)[colonne_order_id].count()

    # Obtenir les 10 villes avec le plus de commandes
    top_10_villes = command_counts.nlargest(10)

    # Regrouper les autres villes
    autres_commandes = command_counts.drop(top_10_villes.index).sum()
    top_10_villes['Autres'] = autres_commandes

    # Définir une palette de couleurs violettes
    colors = sns.color_palette("magma", len(top_10_villes))

    # Fonction pour afficher les pourcentages en blanc
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return f'{pct:.1f}%\n({val:d})'
        return my_autopct

    # Créer le camembert avec les 10 plus grandes villes et "Autres"
    plt.figure(figsize=(10, 7))
    wedges, texts, autotexts = plt.pie(top_10_villes, labels=top_10_villes.index, autopct=make_autopct(top_10_villes), startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})

    # Personnaliser les annotations pour qu'elles soient en blanc
    for autotext in autotexts:
        autotext.set_color('white')

    plt.title('Répartition des commandes par ville (10 plus grandes + Autres)', fontsize=16, color='purple')
    plt.axis('equal')  # Pour faire un cercle
    

    # Ajuster la mise en page pour une meilleure apparence
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


def get_reviews_delivery(orders_df, order_reviews_df):
  
    # Spécifiez les noms des colonnes pertinentes
    colonne_order_id = 'order_id'
    colonne_review_score = 'review_score'
    colonne_order_status = 'order_status'
    colonne_order_approved_at = 'order_approved_at'
    colonne_order_delivered_customer_date = 'order_delivered_customer_date'

    # Convertir les colonnes de date en format datetime
    orders_df[colonne_order_approved_at] = pd.to_datetime(orders_df[colonne_order_approved_at])
    orders_df[colonne_order_delivered_customer_date] = pd.to_datetime(orders_df[colonne_order_delivered_customer_date])

    # Calculer le temps de livraison en jours
    orders_df['delivery_time'] = (orders_df[colonne_order_delivered_customer_date] - orders_df[colonne_order_approved_at]).dt.days

    # Fusionner les DataFrames pour obtenir une vue complète
    merged_df = pd.merge(orders_df, order_reviews_df, on=colonne_order_id)

    # Classifier les temps de livraison
    def classify_delivery(row):
        if pd.isna(row[colonne_order_delivered_customer_date]):
            return 'Jamais arrivé'
        elif row['delivery_time'] < 0:
            return 'En avance'
        elif row['delivery_time'] <= 15:
            return 'À l\'heure'
        else:
            return 'En retard'

    merged_df['delivery_class'] = merged_df.apply(classify_delivery, axis=1)

    # Calculer la moyenne des notes de critiques pour chaque catégorie de temps de livraison
    mean_reviews = merged_df.groupby('delivery_class')[colonne_review_score].mean()

    # Afficher les résultats
    print(mean_reviews)

    # Préparer les données pour le graphique
    labels = mean_reviews.index
    values = mean_reviews.values
    colors = ['#FF00FF', '#FF69B4', '#DA70D6', '#BA55D3']  # Tons magenta

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors)

    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2 - 0.1, yval + 0.05, round(yval, 2), fontsize=12)

    # Ajouter des labels et un titre
    plt.xlabel('Catégories de temps de livraison')
    plt.ylabel('Moyenne des notes de critiques')
    plt.title('Moyenne des notes de critiques par catégorie de temps de livraison')

    # Afficher le graphique
    plt.show()
        # Ajuster la mise en page pour une meilleure apparence
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def get_mensuel_CA(df_order_item, df_payment):

    # Spécifiez les noms des colonnes
    colonne_id_order = 'order_id'  # Colonne des identifiants de commandes
    colonne_date_order = 'order_purchase_timestamp'  # Colonne de la date d'achat
    colonne_payment_value = 'payment_value'  # Colonne du montant du paiement

    # Convertir la colonne de date en format datetime
    df_order_item[colonne_date_order] = pd.to_datetime(df_order_item[colonne_date_order])

    # Extraire l'année et le mois
    df_order_item['year_month'] = df_order_item[colonne_date_order].dt.to_period('M')

    # Fusionner les DataFrames sur order_id
    merged_df = pd.merge(df_order_item, df_payment, on=colonne_id_order)

    # Calculer le CA total par mois
    monthly_revenue = merged_df.groupby('year_month')[colonne_payment_value].sum()

    # Calculer la moyenne mensuelle du CA
    average_monthly_revenue = monthly_revenue.mean()

    print("CA mensuel moyen :")
    print(average_monthly_revenue)

    # Afficher le CA mensuel pour chaque mois
    print("CA mensuel par mois :")
    print(monthly_revenue)

    # Convertir l'index en datetime pour le traçage sans heures
    monthly_revenue.index = monthly_revenue.index.to_timestamp().strftime('%Y-%m')

    # Utiliser seaborn pour améliorer l'apparence du graphique
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(x=monthly_revenue.index, y=monthly_revenue.values, palette="magma")

    # Ajouter des annotations sur les barres
    for i, p in enumerate(ax.patches):
        if i == len(ax.patches) - 1:  # Pour le dernier élément, décalez l'annotation sur la droite
            ax.annotate(format(p.get_height(), '.2f'),
                        (p.get_x() + p.get_width(), p.get_height()),
                        ha = 'center', va = 'center',
                        xytext = (20, 9),
                        textcoords='offset points',
                        fontsize=10, color='white')
        else:
            ax.annotate(format(p.get_height(), '.2f'),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center', va = 'center',
                        xytext = (0, 9),
                        textcoords='offset points',
                        fontsize=10, color='white')

    # Personnaliser le graphique
    plt.title('CA mensuel par mois', fontsize=20, color='purple')
    plt.xlabel('Mois', fontsize=15, color='purple')
    plt.ylabel('CA', fontsize=15, color='purple')
    plt.xticks(rotation=45)
    plt.yticks(color='purple')
    plt.grid(True)

    # Ajouter une ligne de moyenne mensuelle du CA
    plt.axhline(average_monthly_revenue, color='purple', linestyle='--', linewidth=2)
    plt.text(len(monthly_revenue) - 1, average_monthly_revenue, 'CA moyen: {:.2f}'.format(average_monthly_revenue), color='purple', fontsize=12, ha='center')

    # Afficher le graphique
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def bottom_cat(order_df, product_df):
    colonne_id_produit_orders = 'product_id'
    colonne_id_produit_products = 'product_id'
    colonne_nom_produit = 'product_category_name'
    colonne_prix = 'price'

    merged_df = pd.merge(order_df, product_df, left_on=colonne_id_produit_orders, right_on=colonne_id_produit_products)

    merged_df['total_revenue'] = merged_df[colonne_prix]
    revenue_by_category = merged_df.groupby(colonne_nom_produit)['total_revenue'].sum().sort_values(ascending=True)


    product_counts = merged_df[colonne_nom_produit].value_counts().sort_values(ascending=True)

    bottom_categories_df = pd.DataFrame({
        'category_name': product_counts.index,
        'number_of_sales': product_counts.values
    }).head(10)  # 10 catégories les moins populaires

    bottom_categories_revenue_df = pd.DataFrame({
        'category_name': revenue_by_category.index,
        'total_revenue': revenue_by_category.values
    }).head(10)  # 10 catégories les moins rentables

    return bottom_categories_revenue_df, bottom_categories_df

def get_best_and_worst_category_review(orders_df, reviews_df, products_df, order_items_df):

    # Spécifiez les noms des colonnes pertinentes
    colonne_order_id = 'order_id'
    colonne_review_score = 'review_score'
    colonne_product_id = 'product_id'
    colonne_product_category_name = 'product_category_name'

    # Fusionner les DataFrames pour obtenir une vue complète
    merged_df = pd.merge(orders_df, reviews_df, on=colonne_order_id)
    merged_df = pd.merge(merged_df, order_items_df, on=colonne_order_id)
    merged_df = pd.merge(merged_df, products_df, on=colonne_product_id)

    # Calculer la moyenne des notes de critiques par catégorie de produit
    average_reviews = merged_df.groupby(colonne_product_category_name)[colonne_review_score].mean().reset_index(name='average_review_score')

    # Obtenir le top 5 des meilleures catégories
    top_5_best = average_reviews.nlargest(5, 'average_review_score')

    # Obtenir le top 5 des pires catégories
    top_5_worst = average_reviews.nsmallest(5, 'average_review_score')


    # Graphique pour les meilleures catégories
    plt.figure(figsize=(12, 6))
    plt.bar(top_5_best[colonne_product_category_name], top_5_best['average_review_score'], color='magenta')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Catégorie de Produit')
    plt.ylabel('Moyenne des Notes de Critiques')
    plt.title('Top 5 des Meilleures Catégories de Produits (basé sur les notes)')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic1 = base64.b64encode(image_png)
    graphic1 = graphic1.decode('utf-8')

    # Graphique pour les pires catégories
    plt.figure(figsize=(12, 6))
    plt.bar(top_5_worst[colonne_product_category_name], top_5_worst['average_review_score'], color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Catégorie de Produit')
    plt.ylabel('Moyenne des Notes de Critiques')
    plt.title('Top 5 des Pires Catégories de Produits (basé sur les notes)')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic2 = base64.b64encode(image_png)
    graphic2 = graphic2.decode('utf-8')

    return graphic1, graphic2

def get_ne_value_without_freight(order_items_df):

    # Spécifiez les noms des colonnes
    colonne_price = 'price'
    colonne_freight_value = 'freight_value'

    # Calculer la somme des colonnes
    total_price = order_items_df[colonne_price].sum()
    total_freight = order_items_df[colonne_freight_value].sum()

    # Soustraire freight_value de price pour chaque ligne
    order_items_df['net_value'] = order_items_df[colonne_price] - order_items_df[colonne_freight_value]

    # Calculer la somme de la colonne net_value
    total_net_value = order_items_df['net_value'].sum()

    # Préparer les données pour le graphique
    labels = ['Total Price', 'Total Freight', 'Net Value']
    values = [total_price, total_freight, total_net_value]
    colors = ['#FF00FF', '#FF69B4', '#DA70D6']  # Tons magenta

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors)

    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2 - 0.1, yval + 0.05*yval, round(yval, 2), fontsize=12)

    # Ajouter des labels et un titre
    plt.xlabel('Categories')
    plt.ylabel('Montant')
    plt.title('Prix total, valeur du fret et valeur nette')

    # Afficher le graphique
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def total_price_per_year(orders_df,order_items_df):
    # Charger les fichiers CSV

    # Convertir les colonnes de date en format datetime
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])

    # Extraire l'année de la date de livraison
    orders_df['year'] = orders_df['order_delivered_customer_date'].dt.year

    # Filtrer pour les années 2016, 2017 et 2018
    filtered_orders_df = orders_df[orders_df['year'].isin([2016, 2017, 2018])]

    # Fusionner les DataFrames sur la colonne 'order_id'
    merged_df = pd.merge(filtered_orders_df, order_items_df, on='order_id')

    # Calculer le total des prix pour chaque année
    total_price_by_year = merged_df.groupby('year')['price'].sum()

    # Convertir les valeurs en millions ou en milliers si nécessaire
    def format_value(value):
        if value >= 1e6:
            return f'{value / 1e6:.2f}M'
        elif value >= 1e3:
            return f'{value / 1e3:.2f}K'
        else:
            return f'{value:.2f}'

    # Afficher les résultats
    print("Total des prix par année (2016-2018) :")
    print(total_price_by_year)

    # Préparer les données pour le graphique
    plt.figure(figsize=(12, 6))
    bars = plt.bar(total_price_by_year.index.astype(int), total_price_by_year.values, color='deeppink')

    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2 - 0.1, yval + 0.05 * yval, format_value(yval), fontsize=12, ha='center')

    # Ajouter des labels et un titre
    plt.xlabel('Année')
    plt.ylabel('Revenu Total')
    plt.title('Revenu Total par Année (2016-2018)')

    # Afficher le graphique
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


def transport_costs_by_location(order_items_df, orders_df, customers_df):
    # Spécifiez les noms des colonnes
    colonne_price = 'price'
    colonne_freight_value = 'freight_value'
    colonne_order_id = 'order_id'
    colonne_customer_id = 'customer_id'
    colonne_customer_city = 'customer_city'

    # Fusionner les DataFrames pour obtenir les localisations des clients
    orders_customers_df = pd.merge(orders_df[[colonne_order_id, colonne_customer_id]], customers_df, on=colonne_customer_id)
    merged_df = pd.merge(order_items_df, orders_customers_df, on=colonne_order_id)

    # Calculer les frais de transport totaux par ville
    freight_by_city = merged_df.groupby(colonne_customer_city)[colonne_freight_value].sum().sort_values(ascending=False)

    # Sélectionner les 10 villes où les frais de transport sont les plus élevés
    top_10_cities = freight_by_city.head(10)

    # Afficher les résultats
    print("Frais de transport par localisation (Top 10) :")
    print(top_10_cities)

    # Préparer les données pour le graphique
    plt.figure(figsize=(12, 6))
    bars = plt.bar(top_10_cities.index, top_10_cities.values, color='deeppink')
    plt.xticks(rotation=45, ha='right')

    # Ajouter les valeurs au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05*yval, round(yval, 2), fontsize=12, ha='center')

    # Ajouter des labels et un titre
    plt.xlabel('Ville')
    plt.ylabel('Frais de Transport Total')
    plt.title('Frais de Transport par Localisation (Top 10)')

     # Afficher le graphique
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def top_sellers(order_items_df):

    colonne_seller_id = 'seller_id'
    colonne_prix = 'price'
    revenue_by_seller = order_items_df.groupby(colonne_seller_id)[colonne_prix].sum().sort_values(ascending=False)

    # Obtenir les 10 meilleurs vendeurs
    top_10_sellers = revenue_by_seller.head(10)

    # Générer des noms fictifs aléatoires
    fake_names = [
        'Alice Dupont', 'Bob Martin', 'Charlie Bernard', 'David Dubois', 'Emma Lefevre',
        'Fanny Moreau', 'George Petit', 'Hugo Blanc', 'Isabelle Robert', 'Jean Morel'
    ]
    random.shuffle(fake_names)

    # Créer un DataFrame pour les 10 meilleurs vendeurs avec des noms fictifs
    top_10_sellers_df = pd.DataFrame({
        'seller_id': top_10_sellers.index,
        'total_revenue': top_10_sellers.values,
        'seller_name': fake_names[:10]
    })
    # Préparer les données pour le graphique
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_sellers_df['seller_name'], top_10_sellers_df['total_revenue'], color='magenta')
    plt.xticks(rotation=45, ha='right')

    # Ajouter des labels et un titre
    plt.xlabel('Nom du Vendeur')
    plt.ylabel('Revenu Total')
    plt.title('Top 10 des Meilleurs Vendeurs par Revenu Total')

        # Afficher le graphique
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

