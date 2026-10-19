# Import python packages
import streamlit as st
import os

# Importation de la fonction 'col' de Snowpark pour manipuler les colonnes

import requests

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
    """
)

# Ajout d'un champ texte pour le nom du client
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


# Ajout de la liste déroulante (selectbox)
# option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana', 'Strawberries', 'Peaches')
#)

# st.write('Your favorite fruit is:', option)


# ==========================================
# 4. CONNEXION A LA BASE ET AFFICHAGE DES DONNEES
# ==========================================

# Récupération de la session active 

cnx = st.connection("snowflake")
session = cnx.session()

# ==========================================
# 6. UTILISATION DE LA FONCTION COL() POUR FILTRER
# ==========================================

# Requête modifiée : on sélectionne UNIQUEMENT la colonne FRUIT_NAME

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Affichage des données sous forme de tableau interactif dans l'application Streamlit

# st.dataframe(data=my_dataframe, use_container_width=True)


# ==========================================
# 7. AJOUT DU WIDGET MULTISELECT
# ==========================================

# Ajout du champ de sélection multiple
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Affichage brut de la liste (pour comprendre le type de donnée LIST)
# On utilise un bloc IF pour n'afficher la liste QUE si elle n'est pas vide
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # On crée une variable texte vide pour stocker les fruits
    ingredients_string = ''
    
    # On crée une boucle FOR pour parcourir la liste des ingrédients choisis
    for fruit_chosen in ingredients_list:
        # L'opérateur += ajoute le nom du fruit à la suRETAILPULSE_DB.RAW.ORDERS_STREAMite de la chaîne de caractères
        ingredients_string += fruit_chosen 
    
    # On affiche le résultat final (la chaîne de caractères complète)
    st.write(ingredients_string)

    # Création de la requête LA REQUÊTE (avec ingredients ET name_on_order)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

            
    # Affichage de la requête pour vérifier qu'elle est bien formatée
    # st.write(my_insert_stmt)



    # Exécution de la requête SQL via la session active (uniquement si ingredients_string n'est pas vide)
    
    # if ingredients_string:
        # session.sql(my_insert_stmt).collect()
        
        # Affichage d'un beau message de succès vert
        # st.success('Your Smoothie is ordered!', icon="✅")



# Création du bouton de soumission
    time_to_insert = st.button('Submit Order')

    # Exécution de la requête UNIQUEMENT si le bouton est cliqué
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")



smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

    



