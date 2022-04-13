import pandas as pd

def to_df(excel_file):
  return pd.read_csv(excel_file)

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

def group_by_cluster(df):
    return group_by_column_count(df, "cluster_label")

def add_cluster(region_df):
  repart = region_df.loc[:, ['Nom', 'Valeur', 'Groupe']]
  clusters = {i: [] for i in range(1, 5)}  # dict de nos clusters
  for index, row in repart.iterrows():
    clusters[row['Groupe']].append(row['Nom'])

  clusters["Sud"] = clusters[1]
  clusters["Centre"] = clusters[2]
  clusters["Nord"] = clusters[3]
  clusters["Montréal"] = clusters[4]
  del clusters[1]
  del clusters[2]
  del clusters[3]
  del clusters[4]

  return clusters

def get_key(d, val):
    for k, v in d.items():
      if val in v:
        return k


def add_clusters(df,clusters):
  groups = list()
  for index, row in df.iterrows():
    groups.append(get_key(clusters, row['region']))
  df['groupe'] = groups
  return  df


def group_by_column2_count(df, column, col2):
  return df.groupby([column, col2])[column].count()


def group_by_year_month(df, chosenYear, chosenMonth):
  #print('2222222222222222222222222222222222222222222222222222222222222222222222222')
  #print(sorted(df["year"].unique()) )
  newDf = df[df.year == chosenYear]
  #print(newDf)
  #print('2222222222222222222222222222222222222222222222222222222222222222222222222')
  #print(sorted(df["ye
  newDFMonth = newDf[newDf.month == chosenMonth]
  if newDFMonth.empty:
    print('22222222222222222222222DataFrame is empty!')
  #print(newDFMonth)
  return newDFMonth

def group_by_month(df, chosenMonth):
  newDFMonth = df[df.month == chosenMonth]
  print(newDFMonth)
  return newDFMonth
  
