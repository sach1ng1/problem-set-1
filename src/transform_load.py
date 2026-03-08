'''
PART 2: Merge and transform the data
- Read in the two datasets from /data into two separate dataframes
- Profile, clean, and standardize date fields for both as needed
- Merge the two dataframe for the date range 10/1/2024 - 10/31/2025
- Conduct EDA to understand the relationship between weather and transit ridership over time
-- Create a line plot of daily transit ridership and daily average temperature over the whole time period
-- For February 2025, create a scatterplot of daily transit ridership vs. precipitation
-- Create a correlation heatmap of all numeric features in the merged dataframe
-- Load the merged dataframe as a CSV into /data
-- In a print statement, summarize any interesting trends you see in the merged dataset

'''
from src.extract import extract_transit_data
from src.extract import extract_weather_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def read_df():
    tr_df=extract_transit_data()
    print(tr_df.head())
    print (tr_df.info())
    print(tr_df.describe())

    #wthr_df=extract_weather_data()

    #wthr_df.to_csv("chicago_weather_data.csv",index=False)

    new_wthr_df=pd.read_csv("chicago_weather_data.csv")
    print(new_wthr_df.head())
    print(new_wthr_df.info())
    print(new_wthr_df.describe())
    return tr_df,new_wthr_df

#function that cleans data and standarizes columns

def clean_df(tr_df, new_wthr_df):
    tr_df.columns=[column.strip().lower() for column in tr_df.columns]
    new_wthr_df.columns=[column.strip().lower() for column in new_wthr_df.columns]
    tr_df["service_date"]=pd.to_datetime(tr_df["service_date"])
    new_wthr_df["datetime"]=pd.to_datetime(new_wthr_df["datetime"])
    new_tr_df=tr_df.rename(columns={"service_date":"datetime"})
    return new_tr_df,new_wthr_df

def merge_df(new_tr_df, new_wthr_df):
    tr_wthr= pd.merge(new_tr_df,new_wthr_df,on="datetime", how="inner")
    new_tr_wthr= tr_wthr[(tr_wthr["datetime"]>="2024-10-01") & (tr_wthr["datetime"]<="2025-10-31")]
    new_tr_wthr=new_tr_wthr.reset_index(drop=True)
    print(new_tr_wthr.head())
    return new_tr_wthr

def create_visuals(new_tr_wthr):
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=new_tr_wthr, x="temp", y="total_rides")
    plt.xlabel("Temperature")
    plt.ylabel("Total Ridership")
    plt.show()
    
    agg_viz_data=new_tr_wthr.groupby("datetime").agg({"total_rides":"sum", "temp":"mean", "precip":"sum"}).reset_index()
    plt.figure(figsize=(10,8))
    sns.lineplot(data=agg_viz_data, x="datetime", y="total_rides", color="red")
    sns.lineplot(data=agg_viz_data, x="datetime", y= "temp", color="blue")
    plt.xlabel("Date")
    plt.title("Daily Transit Ridership and Daily Avg Temp Over Time (Oct 2024-Oct 2025)")
    plt.show()
    
    
    feb_df= agg_viz_data[(agg_viz_data["datetime"]>="2025-02-01") & (agg_viz_data["datetime"]<="2025-02-28")]
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=feb_df, x="total_rides", y="precip")
    plt.xlabel("Daily Total Ridership")
    plt.ylabel("Daily Precipation")
    plt.title("Feb 2025 Daily Transit Ridership vs. Precipitation")
    plt.show()
    
    plt.figure(figsize=(10,8))
    sns.heatmap(agg_viz_data[["total_rides", "temp", "precip"]].corr(), annot=True)
    plt.show()
    
    agg_viz_data.to_csv("src/agg_viz_data.csv", index=False)
    
    print("Trends Summary: ")
    print("Total Ridership seems to vary as there is not a clear correlation seen with Temperature for the whole time period.")
    print("Average temperature does not seem to affect the daily ridership over time.")
    print("In February 2025, there is a weak relationship between daily ridership and precipitation, other factors may need to be considered.")
    print("Out of the 3 variables temperature and total rides has the higher correlation but it is still considered weak as it 0.31.")
    

    
    
    
    
    
    
    









