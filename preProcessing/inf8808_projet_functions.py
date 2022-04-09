import pandas as pd
import json
import plotly.express as px
import os


def to_df(excel_file):
  return pd.read_excel(excel_file)

df_file = "df.xlsx"
df = to_df(df_file)

df

print(list(df.columns.values))

def group_by_column_count(df, column):
  return df.groupby([column])[column].count()

def group_by_region(df):
  return group_by_column_count(df, "region")

def group_by_subregion(df):
  return group_by_column_count(df, "sub_region")

def group_by_category(df):
  return group_by_column_count(df, "categorie")

def group_by_subcategory(df):
  return group_by_column_count(df, "sousCategorie")

df_count_by_region = group_by_region(df)
df_count_by_region

df_count_by_subregion = group_by_subregion(df)
df_count_by_subregion

df_count_by_category = group_by_category(df)
df_count_by_category

df_count_by_subcategory = group_by_subcategory(df)
df_count_by_subcategory

