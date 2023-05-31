#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: Louis Herry 
"""

import pandas as pd 
import yaml
import sys
import csv
import matplotlib

def receive_data(file_name:str, airline_name:str, airport_name:str, routes_name:str, q_name:str, graph_type:str):
    """
    this function will take all the data in  the argv and name them according to what its sotred.
    and then the function will filter out all the unwanted data.

    the filtered data will be stored in different variables and pass to the function data_process
               
    """
    airline = airline_name.split("=")[1]
    airport = airport_name.split("=")[1]
    routes = routes_name.split("=")[1]
    question = q_name.split("=")[1]
    graph = graph_type.split("=")[1]
 

    data_process(file_name, airline, airport, routes, question,  graph)

def data_process(file_name:str, airline_name:str, airport_name:str, routes_name:str, q_name:str, graph_type:str):
    """
    this function will open all the yaml based on the names that is passed by the "receive_data" function 
    then the function will load all the yaml function. It will turn into a json standard so that Pandas(dataframe) can be used in the program

    then the program will pass the data according the the "q_name".
    """
        
    with open(airline_name,"r") as airlines:
        airline_loaded = yaml.safe_load(airlines)
        airline_loaded = airline_loaded["airlines"]
        airline_data = pd.json_normalize(airline_loaded)
        
    with open(airport_name,"r") as airports:
        airport_loaded = yaml.safe_load(airports)
        airport_loaded = airport_loaded["airports"]
        airport_data = pd.json_normalize(airport_loaded)

    


    with open(routes_name,"r") as routes:
        routes_loaded = yaml.safe_load(routes)
        routes_loaded = routes_loaded["routes"]
        routes_data = pd.json_normalize(routes_loaded)

      
    if(q_name=="q1"):
        q1(airline_data, airport_data, routes_data, graph_type)
    elif(q_name=="q2"):
        q2(airline_data, airport_data, routes_data, graph_type)
    elif(q_name=="q3"):
        q3(airline_data, airport_data, routes_data, graph_type)
    elif(q_name=="q4"):
        q4(airline_data, airport_data, routes_data, graph_type)
    else:
        q5(airline_data, airport_data, routes_data, graph_type)


def q1(airline:str , airport:str , routes:str, graph:str):
    """
    find the top 20 airlines that offer the greatest number of routes with destination 
    country as Canada
    """
    routes = routes.rename(columns={"route_airline_id":"airline_id","route_to_airport_id":"airport_id"})
    airline.drop(['airline_country'],axis=1, inplace = True)
   
    #sort out the canadian airport
    airport = airport[airport['airport_country']=="Canada"]
    #combine two dataframe to get routes that has Canada s destination
    first_comp = pd.merge(airport , routes,how="left")
    second_comp = pd.merge(first_comp , airline,how="left")
    second_comp["airline_name"] = second_comp["airline_name"].astype(str)+" ("+second_comp["airline_icao_unique_code"]+")"

    #group them up according to their size, then in alphabetical order
    answer: pd.DataFrame = second_comp.groupby(["airline_name"],as_index=False).size().sort_values(by=["size","airline_name"],ascending=[False,True]).head(20)
    answer: answer = answer.rename(columns={'airline_name':'subject'})
    answer: answer = answer.set_index("subject")
    
   
    answer.to_csv("q1.csv",header=["statistic"])
    if (graph=="bar"):
        plot = answer.plot(kind = graph)
        plot.get_figure().savefig("q1.pdf",format="pdf")
        
    else:
        
        plot = answer.plot(kind = graph,y="size")
        plot.get_figure().savefig("q1.pdf",format="pdf")

def q2(airline:str , airport:str , routes:str, graph:str):
    """
    find the top 30 countries with least appearances as destination country on the
    routes data
    
    
    """
    routes = routes.rename(columns={"route_airline_id":"airline_id","route_to_airport_id":"airport_id"})
    routes.drop(['route_from_aiport_id'],axis=1, inplace=True)
    first_comp = pd.merge(airport, routes,on="airport_id",how="inner")
    first_comp["airport_country"] = first_comp["airport_country"].str.strip(" ")
    
    #group them according to the size.
    answer: pd.DataFrame = first_comp.groupby(["airport_country"],as_index=False).size().sort_values(by=["size","airport_country"],ascending=[True,True]).head(30)
    answer: answer = answer.rename(columns={'airport_country':'subject'})
    answer: answer = answer.set_index("subject")
   
    answer.to_csv("q2.csv",header=["statistic"])
    
    
    if (graph=="bar"):
        plot = answer.plot(kind = graph)
        plot.get_figure().savefig("q2.pdf",format="pdf")
        
    else:
        
        plot = answer.plot(kind = graph,y="size")
        plot.get_figure().savefig("q2.pdf",format="pdf")

        

def q3(airline:str , airport:str , routes:str, graph:str):
    """
    find the top 10 destination airports
    
    """
    #get the information of each routes, including the destinations
    routes = routes.rename(columns={"route_airline_id":"airline_id","route_to_airport_id":"airport_id"})
    routes.drop(['route_from_aiport_id'],axis=1, inplace=True)
    first_comp = pd.merge(airport, routes,on="airport_id",how="inner")
    first_comp["airport_name"] = first_comp["airport_name"].astype(str)+" ("+first_comp["airport_icao_unique_code"]+")"+", "+first_comp["airport_city"]+", "+first_comp["airport_country"]
    
    #group them according to the size
    answer: pd.DataFrame = first_comp.groupby(["airport_name"],as_index=False).size().sort_values(by=["size","airport_name"],ascending=[False,True]).head(10)
    answer: answer = answer.rename(columns={'airport_name':'subject'})
    answer: answer = answer.set_index("subject")
    answer.to_csv("q3.csv",header=["statistic"])
    
    
    if (graph=="bar"):
        plot = answer.plot(kind = graph)
        plot.get_figure().savefig("q3.pdf",format="pdf")
        
    else:
        
        plot = answer.plot(kind = graph,y="size")
        plot.get_figure().savefig("q3.pdf",format="pdf")

def q4(airline:str , airport:str , routes:str, graph:str):
    """
    find the top 15 destination cities
    pretty similar to what i did on q4
    """
    routes = routes.rename(columns={"route_airline_id":"airline_id","route_to_airport_id":"airport_id"})
    routes.drop(['route_from_aiport_id'],axis=1, inplace=True)
    first_comp = pd.merge(airport, routes,on="airport_id",how="inner")
    first_comp["airport_city"] = first_comp["airport_city"].astype(str)+", "+first_comp["airport_country"]

    answer: pd.DataFrame = first_comp.groupby(["airport_city"],as_index=False).size().sort_values(by=["size","airport_city"],ascending=[False,True]).head(15)
    answer: answer = answer.rename(columns={'airport_city':'subject'})
    answer: answer = answer.set_index("subject")
    answer.to_csv("q4.csv",header=["statistic"])
    
    
    if (graph=="bar"):
        plot = answer.plot(kind = graph)
        plot.get_figure().savefig("q4.pdf",format="pdf")
        
    else:
        
        plot = answer.plot(kind = graph,y="size")
        plot.get_figure().savefig("q4.pdf",format="pdf")

def q5(airline:str , airport:str , routes:str, graph:str):
    """
    the unique top 10 Canadian routes (i.e., if CYYJ-CYVR is included, CYVR-CYYJ 
    should not) with most difference between the destination altitude and the origin altitude
    """
    #from which airport
    airport1 = airport[airport['airport_country']=="Canada"]
    airport1 = airport1.rename(columns={"airport_id":"From_airport_id"})
    routes1 = routes.rename(columns={"route_from_aiport_id":"From_airport_id","route_to_airport_id":"To_airport_id"})
    routes1.drop(['route_airline_id'],axis=1, inplace=True)
    from_first_comp = pd.merge(airport1, routes1,on="From_airport_id",how="left")
    #from_first_comp = from_first_comp.dropna()
    
    #to which airport 
    airport2 = airport[airport['airport_country']=="Canada"]
    airport2 = airport2.rename(columns={"airport_id":"To_airport_id"})
    routes2 = routes.rename(columns={"route_to_airport_id":"To_airport_id",'route_from_aiport_id':'From_airport_id'})
    routes2.drop(['route_airline_id'],axis=1, inplace=True)
    dest_second_comp = pd.merge(airport2, routes2,on="To_airport_id",how="left")
   
    #combine two dataframes above to the all the informations of thosee unique canadian routes
    final_comp = pd.merge(from_first_comp, dest_second_comp,on=["From_airport_id","To_airport_id"],how="inner")
    final_comp = final_comp.drop_duplicates(subset=["airport_city_x","airport_city_y"],keep="first")
   
    #add a column that represents the altitude difference
    final_comp["alt_diff"] = (final_comp["airport_altitude_x"].astype(float)-final_comp["airport_altitude_y"].astype(float)).abs()
    final_comp = final_comp.dropna()
    
    
    final_comp["airport_icao_unique_code_x"] = (final_comp["airport_icao_unique_code_x"].astype(str)+"-"+final_comp["airport_icao_unique_code_y"].astype(str))
    final_comp = final_comp.drop(["From_airport_id","airport_name_x","airport_city_x","airport_country_x","airport_altitude_x","To_airport_id","airport_name_y","airport_city_y","airport_country_y","airport_icao_unique_code_y","airport_altitude_y"],axis=1)
   
    answer : final_comp = final_comp.sort_values(by="alt_diff",ascending=False).head(10)
    answer: answer = answer.rename(columns={'airport_icao_unique_code_x':'subject'})
    answer: answer = answer.set_index("subject")
    
    
    answer.to_csv("q5.csv",header=["statistic"])
    

    if (graph=="bar"):
        plot = answer.plot(kind = graph)
        plot.get_figure().savefig("q5.pdf",format="pdf")
        
    else:
        plot = answer.plot(kind = graph,y="alt_diff")
        plot.get_figure().savefig("q5.pdf",format="pdf")
    
    
    

    

def sample_function(input: str) -> str:
    """Sample function (removable) that illustrations good use of documentation.
            Parameters
            ----------
                input : str, required
                    The input message.

            Returns
            -------
                str
                    The text returned.
    """
    return input.upper()


def main():
    """Main entry point of the program."""

    '''
    send all the data in the argv into the function called receive_data to do further procss
    '''
    # calling the sample function
    receive_data(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    

   


if __name__ == '__main__':
    main()
