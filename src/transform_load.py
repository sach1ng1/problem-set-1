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
    """ 
    Reads the transit and weather Dateframes from the extract file

    Returns:
    tr_df:
    dataframe weather data
    new_wthr_df:
    dataframe transit data
    """    
    tr_df=extract_transit_data()
    tr_df.head()
    tr_df.info()
    tr_df.describe()

    #wthr_df=extract_weather_data()

    #wthr_df.to_csv("chicago_weather_data.csv",index=False)

    new_wthr_df=pd.read_csv("chicago_weather_data.csv")
    new_wthr_df.head()
    new_wthr_df.info()
    new_wthr_df.describe()
    return tr_df,new_wthr_df


def clean_df(tr_df, new_wthr_df):
    """
    Cleans the Transit and Weather Dataframes for the data types and standardizing the columns

    Parameters:
    tr_df: dataframe
        The transit dataframe
    new_wthr_df: dataframe
        The weather dataframe 

    Returns:
    new_tr_df:
        clean transit dataframe 
    new_wthr_df:
        clean weather dataframe
    """    
    tr_df.columns= [column.strip().lower() for column in tr_df.columns]
    new_wthr_df.columns= [column.strip().lower() for column in new_wthr_df.columns]
    tr_df["service_date"]= pd.to_datetime(tr_df["service_date"])
    new_wthr_df["datetime"]= pd.to_datetime(new_wthr_df["datetime"])
    new_tr_df=tr_df.rename(columns={"service_date":"datetime"})
    return new_tr_df,new_wthr_df

def merge_filter_df(new_tr_df, new_wthr_df):
    """
    Merges the clean transit and weather dataframes and filters them from Oct 2024 to Oct 2025

    Parameters:
    new_tr_df: dataframe
        The cleaned transit dataframe
    new_wthr_df: dataframe
        The cleaned weather dataframe

    Returns:
    new_tr_wthr:
        The merged and filtered dataframe for transit and weather data
    """    
    tr_wthr= pd.merge(new_tr_df,new_wthr_df,on="datetime", how="inner")
    new_tr_wthr= tr_wthr[(tr_wthr["datetime"]>="2024-10-01") & (tr_wthr["datetime"]<="2025-10-31")]
    new_tr_wthr= new_tr_wthr.reset_index(drop=True)
    new_tr_wthr.head()
    new_tr_wthr.info()
    return new_tr_wthr

def create_viz(new_tr_wthr):
    """
    Creates Visualizations like pairplot, lineplot, scatterplot, and correlation heatmap for the merged transit and weather dataframe

    Parameters:
    new_tr_wthr:dataframe
        The merged transit and weather dataframe
    """    

    sns.pairplot(new_tr_wthr[["total_rides", "temp", "precip"]])
    plt.show()
    
    daily_avg= new_tr_wthr.groupby("datetime")[["temp", "total_rides", "precip"]].mean()
    daily_avg=daily_avg.reset_index()
    plt.figure(figsize=(10,8))
    sns.lineplot(data=daily_avg, x="datetime", y="total_rides", color="pink")
    sns.lineplot(data=daily_avg, x="datetime", y= "temp", color="green")
    plt.title("Daily Transit Ridership and Daily Avg Temp Over Time (Oct 2024 to Oct 2025)")
    plt.show()
    
    plt.figure(figsize=(10,8))
    feb_viz_df= daily_avg[(daily_avg["datetime"]>="2025-02-01") & (daily_avg["datetime"]<="2025-02-28")]
    sns.scatterplot(data=feb_viz_df, x="total_rides", y="precip")
    plt.title("Feb 2025 Daily Ridership vs. Precipitation")
    plt.show()
    
    plt.figure(figsize=(10,8))
    agg_columns=["total_rides", "temp", "precip"]
    agg_correlation= daily_avg[agg_columns].corr()
    sns.heatmap(agg_correlation, annot=True)
    plt.show()
    
    daily_avg.to_csv("src/agg_tr_wth.csv", index=False)
    
    print("Summary of what I saw for trends: ")
    print("The avg temp does not seem to significantly affect ridership")
    print("Feb 2025 shows that there is a weak relationship between ridership and temp")
    print("the Temperature and total rides correlation is 0.31 which is a weak relatiosnhip")
    

    
    
    
    
    
    
    









