import pandas as pd

def to_df(excel_file):
  return pd.read_csv(excel_file)

def to_df_from_excel(excel_file):
  return pd.read_excel(excel_file)

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

def add_cluster(region_df, quartier_df):
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

  repart_m = quartier_df.loc[:, ['Nom', 'Valeur','Arrondi']]
  quartiers={i:[] for i in range(1,9)} #dict de nos clusters
  for index, row in repart_m.iterrows():
    quartiers[row['Arrondi']].append(row['Nom'])
  
  quart_list = list()
  for quart in quartiers.values():
    quart_list += quart
  
  clusters['Montréal'] = sorted(quart_list)

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
  #print(sorted(df["year"].unique()) )
  newDf = df[df.year == chosenYear]
  newDFMonth = newDf[newDf.month == chosenMonth]
  print(newDFMonth)
  if newDFMonth.empty:
    print('22222222222222222222222DataFrame is empty!')
  return newDFMonth


def group_by_year_month_price(df, chosenYear, chosenMonth, chosenPrice):
    #print(sorted(df["year"].unique()) )
    newDf = df[df.year == chosenYear]
    newDFMonth = newDf[newDf.month == chosenMonth]
    
    newDFMonth["prix"] = pd.to_numeric(newDFMonth["prix"], downcast="float")
    minPrice = pd.to_numeric(chosenPrice[0], downcast="float")
    maxPrice = pd.to_numeric(chosenPrice[1], downcast="float")
    
    newDFPriceMin = newDFMonth[minPrice <= newDFMonth['prix']]
    newDFPrice = newDFPriceMin[newDFPriceMin['prix'] <= maxPrice]
    print(newDFPrice)
    if newDFPrice.empty:
        print('22222222222222222222222DataFrame is empty!')
    return newDFPrice  
  


def group_by_year_month_region(df, chosenYear, chosenMonth, chosenRegion):
  #print("ggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",chosenRegion)
  newDf = df[df.year == chosenYear]
  newDFMonth = newDf[newDf.month == chosenMonth]
  #print(newDFMonth['updated_region'])
  #print(newDFMonth)
  newDFRegion = newDFMonth[newDFMonth.region == chosenRegion]
  #print(newDFRegion)
  if newDFRegion.empty:
    print('22222222222222222222222DataFrame Region is empty!')
  #print(newDFMonth)
  return newDFRegion


def group_by_year_month_region_price(df, chosenYear, chosenMonth, chosenRegion, chosenPrice):
    # print("ggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",chosenPrice)
    newDf = df[df.year == chosenYear]
    newDFMonth = newDf[newDf.month == chosenMonth]
    newDFRegion = newDFMonth[newDFMonth.region == chosenRegion]
    print("kkooooooooooooooooooooooooooook")
    print(newDFRegion['prix'])

    newDFRegion["prix"] = pd.to_numeric(newDFRegion["prix"], downcast="float")
    minPrice = pd.to_numeric(chosenPrice[0], downcast="float")
    maxPrice = pd.to_numeric(chosenPrice[1], downcast="float")
    print('AFTER=',newDFRegion['prix'])
    newDFPriceMin = newDFRegion[minPrice <= newDFRegion['prix']]
    newDFPrice = newDFPriceMin[newDFPriceMin['prix'] <= maxPrice]
    print(newDFPrice)
    
    if newDFPrice.empty:
        print('22222222222222222222222DataFrame Region is empty!')
    return newDFPrice


def group_by_month(df, chosenMonth):
  newDFMonth = df[df.month == chosenMonth]
  print(newDFMonth)
  return newDFMonth

def data_prepartion_barchart_gratuit(df,cluster):

  regions_list = list(cluster.index.get_level_values('groupe').unique())  # labels
  groupe = {}
  for row in regions_list:
    temp_dt = df.loc[df['groupe'] == row]
    groupe[row] = temp_dt


  array = []
  for item in groupe:
    dict = {
      'groupe': item,
      'événements_gratuits': groupe[item]['est_gratuit'].value_counts()[1],
      'événement_payant': groupe[item]['est_gratuit'].value_counts()[0],
      'total_count':groupe[item]['est_gratuit'].value_counts()[1]+ groupe[item]['est_gratuit'].value_counts()[0]

    }


    array.append(dict)

  df_order = pd.DataFrame.from_dict(array)

  df_order.sort_values(['total_count'],inplace=True, ascending=False)


  return df_order


def data_prepartion_barchart_par_prix(df,region):

  data = df.loc[(df["groupe"] == region)& (df["est_gratuit"] ==False)]


  categorie = data['categorie'].unique().tolist()

  groupe = {}

  for cat in categorie:

    temp_dt = pd.DataFrame()

    temp_dt['prix'] = data.loc[(data["categorie"] == cat) & (data["groupe"] == region),'prix']

    quant = [0, .25, 0.5, .75, 1]
    quartiles = data['prix'].quantile(quant)



    temp_dt['seuil1'] = temp_dt['prix'].apply(lambda x: True if (x >= quartiles[0]) & (x < quartiles[0.5]) else False)
    temp_dt['seuil2'] = temp_dt['prix'].apply(lambda x: True if (x >= quartiles[0.5]) & (x < quartiles[0.75]) else False)
    temp_dt['seuil3'] = temp_dt['prix'].apply(lambda x: True if (x >= quartiles[0.75]) &(x <= quartiles[1]) else False)

    groupe[cat] = temp_dt

    array = []
    for item in groupe:

      dict = {
        'categorie': item,
        'seuil1': groupe[item]['seuil1'].value_counts()[True],
        'seuil2': groupe[item]['seuil2'].value_counts()[True],
        'seuil3': groupe[item]['seuil3'].value_counts()[True],
        'total_count':groupe[item]['seuil3'].value_counts()[True] + groupe[item]['seuil3'].value_counts()[False]



      }
      array.append(dict)
    df_order = pd.DataFrame.from_dict(array)

  df_order.sort_values(['total_count'],inplace=True, ascending=False)

  return df_order
