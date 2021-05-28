import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import sys
from collections import Counter
import matplotlib.pyplot as plt

st.title("Web scrapping project : Domaine touristique")
st.markdown('**par Anna NISKOVSKIKH** M2 - TAL - IM, 2020/2021')

st.sidebar.header("Menu de navigation")
st.sidebar.subheader('Application : Eco-friendly hotels')
st.sidebar.markdown('##### **par Anna NISKOVSKIKH** M2 - TAL - IM, 2020/2021')
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.markdown('### Visualisation des informations extraites')
st.sidebar.markdown("*Choisissez ce que vous avez envie de consulter*")
menu = st.sidebar.selectbox(
    "",
    ("Contexte eco", "Intro éco hôtels", "Statistique visualisée", "Conclusion")
)


if menu == "Contexte eco":
    st.header('Contexte eco : eco-friendly hotels')
    image = Image.open('img/ecolo.png')
    st.image(image, 
            caption='The picture taken on @https://www.bioalaune.com',
            width=200,
            layout='wide')
    st.markdown("Comme tout le monde sait, depuis **2016** il existe *un accord sur les changements climatiques* \
                qui s’appelle **l'Accord de Paris**. Son objectif est de **limiter le réchauffement climatique** à un niveau \
                bien inférieur à 2, de préférence à 1,5 degré Celsius, par rapport au niveau préindustriel.")
    st.markdown("Néanmoins, *la mise en œuvre de l'Accord de Paris exige une transformation économique et sociale.* \
                Entre outre, la transformation sociale comprend en elle un **respect du mode de vie plus écologique**. \
                C’est pour cela qu'il est préférable d’investir dans le **logement touristique \
                écologique** - parce que c’est **notre futur**.")

if menu == "Intro éco hôtels":
    st.header('Introduction : eco-friendly hotels')
    image = Image.open('img/ecoHotels.jpg')
    st.image(image, 
            caption='The picture taken on @https://hotel-courchevel1850.com',
            width=200,
            layout='wide')
    st.markdown('Cette partie consiste à explorer une **plateforme touristique** \
    afin de découvrir des **logements écologiques** partout dans le monde et visualiser des résultats pour \
    faciliter une prise de décisions des clients.')
    st.markdown("Le but de notre projet est d’extraire des données nécessaires \
    et les visualiser à l’aide des outils modernes développés sous Python \
    *(selenium, pandas, matplotlib, streamlit)* pour simplifier la perception de l'information.")

if menu == "Statistique visualisée":
    st.header('Eco-friendly hotels : statistique')
    st.subheader('Consultez cette page pour vérifier si un hôtel est ECO')
    image = Image.open('img/index.jpeg')
    st.image(image, 
            caption='The picture taken on @http://employmentnews.gov.in',
            width=200,
            layout='wide')

    # load dataframe from a csv file
    input_csv_file = sys.argv[1]
    csv_file = (input_csv_file)

    """
    Table showing all existing data on hotels
    """
    st.markdown("Le tableau présenté ci-dessous représente des **informations totales** se trouvant sur le site\
         @https://www.nh-hotels.fr.")
    st.markdown("La *première colonne* est l'**id**, la *deuxième* est le **nom de la ville**, la *troisième* - le **nom de l'hôtel** \
        et la *quatrième* est l'information sur le **status ECO** de tel ou tel hôtel.")
    st.markdown("Nous pouvons également **cliquer** sur le nom des colonnes pour les **trier**.")
    st.markdown("*Par exemple, en cliquant sur la deuxième colonne ou troisième colonne des nom de ville ou d'hötel seront triés \
        dans l'ordre alphabétique croissant ou décroissant.")
    st.markdown("En cliquant sur la colonne *Status ECO* le tri sera fait au niveau de **YES/NO**.")
    df = pd.read_csv(csv_file, delimiter='\t')
    df.columns = ((df.columns.str).replace("^ ","")).str.replace(" $","")
    st.dataframe(df)


    st.markdown("Ici, nous pouvons voir le **nombre total des hôtels par ville**.")
    st.dataframe(df.groupby(by=[df.columns[0]]).count()[[df.columns[1]]])


    st.text("")
    st.markdown("Sur le *petit tableau* ci-dessous est résentée l'information sur **la proportion** des hôtels **ECO et non-ECO**.")
    st.dataframe(df.groupby(by=[df.columns[2]]).count()[[df.columns[1]]])

    st.markdown("La même information sur **la proportion ECO - Non-ECO** est présentée sous forme de *diagramme*.")
    pie_chart = px.pie(df.groupby(by=[df.columns[2]]).count()[[df.columns[1]]],
                    title='No total des hôtels: Eco (bleu) vs Non-Eco (rouge) -- Visualisation',
                    values=df.columns[1],
                    names=df.columns[1])

    st.plotly_chart(pie_chart)

    cn_eco_by_city = Counter()
    with open(csv_file, 'r') as input:
        for line in input:
            row = line.split('\t')
            if row[2] == 'YES\n':
                cn_eco_by_city[row[0]] += 1


    st.text("")
    st.markdown("Sur ce tableau, le **nombre total** d'hôtels **ECO** est visualisé, trié **par ville**.")
    dataframe = pd.DataFrame.from_dict(cn_eco_by_city, orient='index').reset_index()
    st.dataframe(dataframe)

    labels = []
    cn = []
    for city in cn_eco_by_city:
        labels.append(city)
        cn.append(cn_eco_by_city[city])

    #mark cities with the biggest number of eco hotels
    explode = (0, 0.1, 0, 0.1, 0, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(cn, explode=explode, labels=labels, 
            autopct='%1.1f%%', startangle=65)
    ax1.axis('equal')  #equal aspect ratio ensures that pie is drawn as a circle.
    st.markdown("Le diagramme suivant démontre **le tri des hôtels ECO par ville**.")
    st.pyplot(plt.show())

if menu == "Conclusion":
    st.header('Conclusion : eco-friendly hotels')
    image = Image.open('img/accordParis.jpg')
    st.image(image, 
            caption='The picture taken on @https://www.actu-environnement.com',
            width=200,
            layout='wide')
    st.markdown("Comme nous pouvons le voir dans la *partie statistique* de nos résultats, la répartition du statut \
                eco-friendly n’est déjà pas égale à ce jour - **62 pourcents de logement *écologique* et 38%** - *non-écologique*, \
                parmi 171 hôtels disponibles, 106 a un service eco-friendly.")
    st.markdown("**Tout le monde** peut consulter l’application créée pour en tirer des conclusions et pour *faire facilement\
                préférence* à des **hôtels écologiques** partout dans le monde grâce à notre visualisation. Les clients seront \
                certainement en mesure de *choisir une ville de sa préférence* dans le tableau présenté sur la **page \
                statistique** de l’application et d’en choisir parmi une liste des hôtels proposés ceux qui \
                correspondraient à ses attentes et sa vision du monde.")