import plotly.express as px

def barchart_gratuit(df):


	fig = px.bar(df, x='groupe', y=["événements_gratuits", "événement_payant"] )

	fig.update_layout(
		#title="Barchart pour les événements gratuits et payants.",
		xaxis_title="Régions du Québec",
		yaxis_title="Nombre d'évènements",

	)
	return fig




def barchart_filtrage(df):



	fig = px.bar(df, x='categorie', y=['seuil1','seuil2','seuil3'] )

	fig.update_layout(
		#title="Barchart pour les événements gratuits et payants.",
		xaxis_title="Catégories",
		yaxis_title="Nombre d'évènements",

	)
	#fig.show()
	return fig



















	#total = df.value_counts()
	#df=df.groupby(['groupe'])['est_gratuit'].count()
	#print(groupe_by_temp)
	#print(groupe_by_est_gratuit)

	#temp_df=clus_est_gratuit_data.loc[['Centre'][0]]
	# print("clus_est_region",clus_est_region)
	# print("clus_est_gratuit",clus_est_gratuit)

	# print("data is \n",clus_est_gratuit_data)
	# print("\n #####type of data",type(clus_est_gratuit_data))


	# values = list()
	#print(x_df)
	# temp_df=clus_est_gratuit_data.to_frame()
	# print("#####toframe is",temp_df)
	# print("\ntype of toframe is",type(temp_df))
	# print("colomn of toframe is",temp_df.columns)

	# for row in clus_est_gratuit:
	# 	values.append(row)


	#print(values)
	#test=[values[i]  for i in range(len(values))]
	#print("this is test",test)
	# true_false_centre=values[0]+values[1]
	# true_false_montreal=values[2]+values[3]
	# true_false_nord=values[4]+values[5]
	# true_false_sud=values[5]+values[6]
	#
	# print(x_df[0],true_false_centre)
	# print(x_df[1],true_false_montreal)
	# print(x_df[2],true_false_nord)
	# print(x_df[3],true_false_sud)
	#print(values)
	#temp=clus_est_gratuit_data[clus_est_gratuit_data['groupe']=='Centre']
	#print("temp",temp)

	# temp=clus_est_gratuit_data.loc[('Centre', True)]
	#fig = px.bar(clus_est_gratuit_data, x="groupe", y="est_gratuit",
	# color="est_gratuit", title="Long-Form Input"
	#)
	#fig.show()

	#print("This is clus_est_gratuit_data\n",clus_est_gratuit_data.loc['groupe'])


	# fig = px.bar(df, x="groupe", y="count",
	#             # color="medal",
	#              title="THis is a test")