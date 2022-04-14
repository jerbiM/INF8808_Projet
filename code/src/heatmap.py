from plotly_calplot import calplot
from datetime import datetime
import numpy as np
from pandas import read_excel, read_csv
import pandas as pd
from collections import Counter


def get_dates_count(dates:list):
  count = Counter(dates)
  dates = list(count.keys())
  counts = list(count.values())
  return pd.DataFrame(list(zip(dates, counts)),
               columns =['date', 'count']).sort_values(by='date',ignore_index=True)


def filter_years(df, years:list):
  data_years = df[df.year.isin(years)].date_debut.to_list()
  return [pd.to_datetime(d) for d in data_years]


def make_heatmap(df, years):
    data_years = filter_years(df, years)
    df_day_count = get_dates_count(data_years)
    fig = calplot(
        df_day_count,
        x="date",
        y="count",
        name="Number of events",
        years_title=True,
        space_between_plots = 0.18,
    )
    fig.update_traces(colorbar=dict(
    title="Nombre d'évènements",
    thicknessmode="pixels", thickness=10,
    lenmode="pixels", len=300,
    yanchor="middle",
    ticks="outside", 
    ticksuffix="",
    dtick=2
    ), showscale = True, selector=dict(type='heatmap'))
    return fig