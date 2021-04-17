import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Calcul cout BUT')

def cout_semestre(volume_td, volume_tp, volume_cours, heures_reelles=False):
    return volume_tp *  2/3 + volume_td + volume_cours * 1.5

def cout_annee(volume_total, coeff_tp, coeff_td):
    if coeff_td + coeff_tp > 100:
        return -1
    td = (coeff_td * volume_total)/100
    tp = (coeff_tp * volume_total)/ 100
    cours = volume_total - td -tp
    return cout_semestre(td, tp, cours)

volume_total_3A = 2000

recommendation_volumes = [ 850, 700, 450]

repartition_annees = st.slider("Répartition des heures par année", 0, 2000, (recommendation_volumes[0], recommendation_volumes[0] + recommendation_volumes[1]), 10)
vol = [ repartition_annees[0], repartition_annees[1] - repartition_annees[0], 2000-repartition_annees[1]]

def compare_recommendation(nb1,nb2):
    if nb2>nb1:
        return str(nb1 - nb2) + "h par rapport à la recommendation"
    if nb1 == nb2:
        return "identique recommendation"
    return "+" + str(nb1 - nb2) + "h par rapport à la recommendation"

md = ""
for i in range(3):

    md+="* Volume Cours %sA : %sh (%s)"%(i+1,vol[i], compare_recommendation(vol[i], recommendation_volumes[i]))
    md+="\n"

st.markdown(md)
recommendation_td_tp = [25,25,50]

repartition_td_tp= st.slider("Répartition CM - TD - TP", 0, 100, (recommendation_td_tp[0], recommendation_td_tp[0] + recommendation_td_tp[1]), 5)
CM,TD,TP= [ repartition_td_tp[0], repartition_td_tp[1] - repartition_td_tp[0], 100-repartition_td_tp[1]]




df = pd.DataFrame({"Annee": [1,2,3], "CM":[ vol[x]*CM/100 for x in range(3)], "TD":[ vol[x] * TD/100 for x in range(3)], "TP":[ vol[x]*TP/100 for x in range(3)]})
df["projet"] = 260
df["Cout"] = round(df["CM"]*1.5 + df["TD"] * 4 + df["TP"]*8*(2/3)) + df["projet"]
df["Heures réelles"] = round(df["CM"]*1.5 + df["TD"] * 4 + df["TP"]*8)
df.loc["TOTAL"] = df.sum()
details = st.checkbox("Afficher détails ?")
if details:
    st.dataframe(df)
else:
    st.dataframe(df[["Cout", "Heures réelles"]])

