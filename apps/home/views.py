# -*- encoding: utf-8 -*-


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from apps.load_data import load_data
from apps.home.utils import get_delivered_orders_by_month, top_cat
import  matplotlib.pyplot as plt


@login_required(login_url="/login/")
def index(request):
    
    data = load_data()
    df = data["payment"]
    df_customer = data['customer']
    df_seller = data['seller']
    df_order = data['order']
    df_product=data['product']
    df_order_item = data['order_item']
    nom_colonne = 'payment_value'
    nom_colonne_client = 'customer_unique_id'
    somme = 0  # Valeur par défaut
    nombre_clients_uniques = 0 
    chart_img= get_delivered_orders_by_month(df_order)
    top_cate, top_cate_price= top_cat(df_order_item,df_product)
    if nom_colonne in df.columns:
        somme = df[nom_colonne].sum()
    else:
        print(f"La colonne '{nom_colonne}' n'existe pas dans le fichier.")
    
    if nom_colonne_client in df_customer.columns:
        nombre_clients_uniques = df_customer[nom_colonne_client].nunique()
    else:
        print(f"La colonne '{nom_colonne_client}' n'existe pas dans le fichier.")
    
    nom_colonne_seller = 'seller_id'
    if nom_colonne_seller in df_seller.columns:
        nombre_seller_uniques = df_seller[nom_colonne_seller].nunique()
    else:
        print(f"La colonne '{nom_colonne_seller}' n'existe pas dans le fichier.")
    

    # Spécifiez le nom de la colonne de statut des commandes
    colonne_statut = 'order_status'  # Colonne contenant les statuts des commandes

    # Filtrer les commandes avec le statut 'delivered'
    delivered_orders = df_order[df_order[colonne_statut] == 'delivered']

    # Compter le nombre total de commandes livrées
    nombre_total_commandes_livrees = len(delivered_orders)

    context = {'segment': 'index', 'total_vente': somme, 'total_client': nombre_clients_uniques, 'total_seller': nombre_seller_uniques, 'order_delivered': nombre_total_commandes_livrees, 'chart_img': chart_img, 'top_cat': top_cate, 'top_cat_price':top_cate_price}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
