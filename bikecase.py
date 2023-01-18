# %% import and read the files
from pathlib import Path
import os
from dotenv import load_dotenv
import pandas as pd
import glob
import numpy as np
env_path = Path('./.env')
load_dotenv(env_path)

path = os.getenv('path')
all_files=glob.glob(path+"/"+"*.csv")

lista=[pd.read_csv(filename, index_col=None, header=0)for filename in all_files]

#%% Changing column names 

df= pd.concat(lista, axis=0, ignore_index=True).rename(columns={
        "rideable_type": "bike_type",
        "started_at" :"start_date",
        "ended_at": "end_date",
        "member_casual":"customer_type",
        "start_station_name":"start_station",
        "end_station_name":"end_station"
    })
df.info()
#%% changing the type of data for date
df.start_date = pd.to_datetime(df.start_date) 
df.end_date = pd.to_datetime(df.end_date) 
df.head()
#%% add columns giving format to the date

df["start_hour"]=df["start_date"].dt.hour
df["year"]=df["start_date"].dt.year
df["month"]=df["start_date"].dt.month_name()
df["day"]=df["start_date"].dt.day_name()
df["trip_duration"]=(df["end_date"]-df["start_date"]).dt.total_seconds().div(60).astype(float)
#%% DROP trips less than 1 min and more than 12 hrs
df.columns
df["customer_type"].value_counts(dropna=False)
duration_trips=(len(df[df['trip_duration']<=0])) 
duration_trips
index_duration=df[df["trip_duration"]<1].index
index_duration2=df[df["trip_duration"]>720].index
df1=df.drop(index_duration)
df2=df1.drop(index_duration2)
#%%                    
df2.drop(['year','end_lat', 'end_lng'],axis=1,inplace=True)

#%% duplicated to know if we have duplicated values
df3=df2.duplicated()
df3.value_counts()
#%%Exploring trip duration
trip_duration=df2.groupby(["trip_duration"]).size().sort_values(ascending=False)
trip_duration.describe


#%%exploring
mode_day=df2.groupby("customer_type")["day"].agg(pd.Series.mode)
mode_station_to=df2.groupby("customer_type")["end_station"].agg(pd.Series.mode)
mode_station_from=df2.groupby("customer_type")["start_station"].agg(pd.Series.mode)
ask = pd.to_numeric(df['trip_duration'], errors='coerce').isna()
a=ask.sum()
ask

# %%# %% statistical analysis:
analysis_time=df2.groupby("customer_type")["trip_duration"].describe()

monthly_avg=df2.pivot_table(index='month', columns='customer_type',
                    aggfunc={'trip_duration':"mean"}) #average mothly

daily_avg=df2.pivot_table(index='day', columns='customer_type',
                    aggfunc={'trip_duration':'mean'}) #average dayly
##%
dif_daily= daily_avg.sum() 
# member-casual/casual*100
dif_d=dif_daily({dif_daily.casual-dif_daily.member})/dif_daily.member 
##%            
monthly_totalmin=df2.pivot_table(index='month', columns='customer_type',
                    aggfunc={'trip_duration':"count"})# total min montly                    

daily_totalmin=df2.pivot_table(index='day', columns='customer_type',
                    aggfunc={'trip_duration':'count'}) #total min dayly
dif_daily= daily_avg.sum()
popular_hours=df2.pivot_table( index="start_hour", columns="customer_type", 
aggfunc={"start_hour":"count"})
hourly_ticks = np.arange(24)

popular_bike=df2.pivot_table(index="bike_type", columns="customer_type", 
            aggfunc={"bike_type":"count"}) 



# %%
