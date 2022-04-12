import pandas as pd

def to_df(excel_file):
    return pd.read_excel(excel_file)

df = to_df("df.xlsx")

rep = to_df("repartition-region.xlsx")
repartition = rep.loc[:, ['Nom', 'Valeur','Groupe']]

def to_df_cluster(df_file):
    new_df = to_df(df_file)
    return new_df.loc[:, ['Nom', 'Valeur','Groupe']]

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

def create_cluster(df):
    """
    Returns a dictionnary with key = cluster id and value = list of regions included in the cluster.
    """
    clusters={i:[] for i in range(1,5)} #dict de nos clusters
    for index, row in df.iterrows():
        clusters[row['Groupe']].append(row['Nom'])
    clusters["Sud"] = clusters[1]
    clusters["Centre"] = clusters[2]
    clusters["Nord"] = clusters[3]
    clusters["Montréal"]=clusters[4]
    del clusters[1]
    del clusters[2]
    del clusters[3]
    del clusters[4]
    return clusters

#add new clusters to df
def get_key(d, val):
    for k, v in d.items(): 
        if val in v:
            return k

def add_clusters(df):
    groups =list()
    for index, row in df.iterrows():
        groups.append(get_key(clusters, row['region']))
    df['groupe']=groups

add_clusters(df)

def group_by_column2_count(df, column, col2):
  return df.groupby([column, col2])[column].count()

#clus_cat_data=group_by_column2_count(df, 'groupe','categorie')

