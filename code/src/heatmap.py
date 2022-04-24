# from plotly_calplot import calplot
from calplot import calplot
from datetime import datetime
import numpy as np
from pandas import read_excel, read_csv
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

##################### Filter function #############################
def filter_years(df, years: list):
  if years == [0]:
    return df
  else: 
    years_to_keep = set(years)
    return df[df.year.isin(years_to_keep)]
  
def filter_category(df, categories: list):
  if categories == ["all"]:
    return df
  else: 
    categories_to_keep = set(categories)
    return df[df.categorie.isin(categories_to_keep)]

def filter_price(df, pricing: str): 
  if pricing == "all": 
    return df
  else:
    if pricing == "free":
      return df[df.est_gratuit]
    elif pricing == "pricy":
      return df[df.est_gratuit == False]

def filter_modality(df, modality: str):
  if modality == "all": 
    return df
  else:
    if modality == "online":
      return df[df.est_enLigne]
    elif modality == "inperson":
      return df[df.est_enLigne == False]

def filter_df(df, years = [0], categories = ["all"], pricing = "all", modality = "all"):
  df1 = filter_modality(df, modality)
  df2 = filter_price(df1, pricing)
  df3 = filter_category(df2, categories)
  return filter_years(df3, years)  

##################### Potting function #############################
def get_dates_count(dates:list):
  count = Counter(dates)
  dates = list(count.keys())
  counts = list(count.values())
  return pd.DataFrame(list(zip(dates, counts)),
               columns =['date', 'count']).sort_values(by='date',ignore_index=True)
  
  
def plot_heatmap(df, title: str):
  dates = pd.to_datetime(df.date_debut).to_list()
  dates_count = get_dates_count(dates)
  dates_count.set_index("date", inplace=True)
  count_data = pd.Series(dates_count["count"])
  n_fig = len(df.year.unique())
  calplot(data=count_data, cmap='Reds', figsize=(18, n_fig*3))
  plt.suptitle(title, y=1.10, fontsize=20)
  
def filter_plot_heatmap(df, years: list, categories: list, pricing: str, modality: str):
  prefiltred_df = filter_df(df, years=years, categories=categories)
  
  if(pricing != "compare"): 
    df_filtred = filter_df(prefiltred_df, pricing=pricing, modality=modality)
    plot_heatmap(df_filtred, title="Cartes de chaleur selon les filtres")

  elif(pricing == "compare"): 
    df_filtred2 = filter_df(prefiltred_df, modality=modality)
    df_free = filter_df(df_filtred2, pricing = "free")
    df_pricy = filter_df(df_filtred2, pricing = "pricy")
    plot_heatmap(df_free, title="Carte(s) de chaleur des évènements gratuits")
    plot_heatmap(df_pricy, title="Carte(s) de chaleur des évènements payants")