import requests
import json
import pandas as pd
import numpy as np
import time

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class PoblacionMayor():
    
    def  __init__(self):
        self.name = "PoblacionMayor"
    
    def execute (self,Poblacion_mayor_total_mujeres,Poblacion_mayor_total_hombres, path_file):
        df_total_hombres = self._total_hombres(Poblacion_mayor_total_hombres)
        df_total_mujeres = self._total_mujeres(Poblacion_mayor_total_mujeres)
        df_scrap_prepared = self._scrap_prepared(path_file)
        df_poblacion_mayor = self._poblacion_mayor(df_total_hombres,df_total_mujeres,df_scrap_prepared)

        return df_poblacion_mayor

    def _total_hombres (self,Poblacion_mayor_total_hombres):  #Prepare Total_Hombres
        response = requests.get(Poblacion_mayor_total_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta Total_hombres, condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        df_poblacion_mayor_total_hombres = pd.DataFrame(data)

        df_poblacion_mayor_total_hombres = df_poblacion_mayor_total_hombres.rename(columns = {'OBS_VALUE' : 'total_hombres', 'COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        df_poblacion_mayor_total_hombres = df_poblacion_mayor_total_hombres.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        df_poblacion_mayor_total_hombres['entidad'] = df_poblacion_mayor_total_hombres['entidad'].replace('00','Nacional')
        
        return df_poblacion_mayor_total_hombres

    def _total_mujeres(self,Poblacion_mayor_total_mujeres): #Prepare Total_Mujeres
        response = requests.get(Poblacion_mayor_total_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        df_poblacion_mayor_total_mujeres = pd.DataFrame(data)

        df_poblacion_mayor_total_mujeres = df_poblacion_mayor_total_mujeres.rename(columns = {'OBS_VALUE' : 'total_mujeres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        df_poblacion_mayor_total_mujeres = df_poblacion_mayor_total_mujeres.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        df_poblacion_mayor_total_mujeres['entidad'] = df_poblacion_mayor_total_mujeres['entidad'].replace('00','Nacional')

        return df_poblacion_mayor_total_mujeres
    
    def _scrap_prepared(self,path_file): #web scaping prepared to join with other dataframes

        inegiDf = pd.read_csv(path_file, header=0, skiprows=4,encoding='ISO-8859-1', sep=',')
        inegiDf = inegiDf.drop([61])

        inegi_df = inegiDf.rename(columns = {'Unnamed: 0' : 'anio', 'Total':'poblacion_mayor' ,'Hombre':'total_hombres','Mujer':'total_mujeres'})
        inegi_df = inegi_df.drop(['Unnamed: 4'], axis=1)
        
        #start to prepare the dataframe to obtain column Anio and Periodo
        inegi_df[['periodo', 'drop1','drop2','anio']] = inegi_df.anio.str.split(expand=True)
        inegi_df= inegi_df.drop(['drop1','drop2'], axis=1)

        #split other columns and drop unnecessary data
        inegi_df['poblacion_mayor'] = inegi_df.poblacion_mayor.str.split('|', n=0, expand = True)
        inegi_df['total_hombres'] = inegi_df.total_hombres.str.split('|', n=0, expand = True)
        inegi_df['total_mujeres'] = inegi_df.total_mujeres.str.split('|', n=0, expand = True)

        #reorganization and normalization
        inegi_df = inegi_df[['anio','periodo','poblacion_mayor','total_hombres','total_mujeres']]
        inegi_df['periodo'] = inegi_df['periodo'].replace('Primer','Trimestre 1')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Segundo','Trimestre 2')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Tercer','Trimestre 3')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Cuarto','Trimestre 4')

        inegi_df['entidad'] = 'Puebla'

        return inegi_df

    def _poblacion_mayor(self,df_total_hombres,df_total_mujeres,df_scrap_prepared):
        poblacion_mayor = df_total_hombres.merge(df_total_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])

        poblacion_mayor[['anio', 'periodo']] = poblacion_mayor.anio.str.split("/",n=1, expand=True)

        poblacion_mayor['periodo'] = poblacion_mayor['periodo'].replace('01','Trimestre 1')
        poblacion_mayor['periodo'] = poblacion_mayor['periodo'].replace('02','Trimestre 2')
        poblacion_mayor['periodo'] = poblacion_mayor['periodo'].replace('03','Trimestre 3')
        poblacion_mayor['periodo'] = poblacion_mayor['periodo'].replace('04','Trimestre 4')

        
        #poblacion_mayor['periodo'] = poblacion_mayor['periodo'].astype('string')
        poblacion_mayor['total_hombres'] = poblacion_mayor['total_hombres'].apply(np.float)
        poblacion_mayor['total_hombres'] = poblacion_mayor['total_hombres'].apply(np.int)
        poblacion_mayor['total_mujeres'] = poblacion_mayor['total_mujeres'].apply(np.float)
        poblacion_mayor['total_mujeres'] = poblacion_mayor['total_mujeres'].apply(np.int)
        poblacion_mayor['entidad'] = poblacion_mayor['entidad'].astype('string')

        poblacion_mayor['poblacion_mayor'] = poblacion_mayor['total_hombres'] + poblacion_mayor['total_mujeres']
        poblacion_mayor = poblacion_mayor[['anio','periodo','poblacion_mayor','total_hombres','total_mujeres', 'entidad']]

        poblacion_mayor = pd.concat([poblacion_mayor, df_scrap_prepared], ignore_index=True, sort=False)

        poblacion_mayor['anio'] = poblacion_mayor['anio'].astype('int')
        poblacion_mayor['poblacion_mayor'] = poblacion_mayor['poblacion_mayor'].astype('int')

        return poblacion_mayor
