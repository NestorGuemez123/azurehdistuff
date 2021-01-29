import requests
import json
import pandas as pd
import numpy as np
import time

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class PoblacionSubocupada():

    def __init__(self):
        self.name="PoblacionSubocuoada"
    
    def execute(self,Poblacion_subocupada_total_hombres,Poblacion_subocupada_total_mujeres,url_scraping,path_file):
        df_total_hombres = self._total_hombres(Poblacion_subocupada_total_hombres)
        df_total_mujeres = self._total_mujeres(Poblacion_subocupada_total_mujeres)
        df_scrap_prepared = self._scrap_prepared(path_file)
        df_Poblacion_Subocupada = self._poblacion_subocupada(df_total_hombres,df_total_mujeres,df_scrap_prepared)

        return df_Poblacion_Subocupada

    def _total_hombres(self,Poblacion_subocupada_total_hombres):
        response= requests.get(Poblacion_subocupada_total_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_subocupada_total_hombres = pd.DataFrame(data)

        Poblacion_subocupada_total_hombres = Poblacion_subocupada_total_hombres.rename(columns = {'OBS_VALUE' : 'total_hombres', 'COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_subocupada_total_hombres = Poblacion_subocupada_total_hombres.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_subocupada_total_hombres['entidad'] = Poblacion_subocupada_total_hombres['entidad'].replace('00','Nacional')

        return Poblacion_subocupada_total_hombres
    
    def _total_mujeres(self,Poblacion_subocupada_total_mujeres):

        response = requests.get(Poblacion_subocupada_total_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_subocupada_total_mujeres = pd.DataFrame(data)

        Poblacion_subocupada_total_mujeres = Poblacion_subocupada_total_mujeres.rename(columns = {'OBS_VALUE' : 'total_mujeres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_subocupada_total_mujeres = Poblacion_subocupada_total_mujeres.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_subocupada_total_mujeres['entidad'] = Poblacion_subocupada_total_mujeres['entidad'].replace('00','Nacional')
        
        return Poblacion_subocupada_total_mujeres
    
    def _scrap_prepared(self,path_file):
        inegiDf = pd.read_csv(path_file, header=0, skiprows=4,encoding='ISO-8859-1', sep=',')
        inegi_df = inegiDf.drop([61])

        #rename and delete some unnecessary columns
        inegi_df = inegi_df.rename(columns = {'Unnamed: 0' : 'anio', 'Total':'poblacion_subocupada' ,'Hombre':'total_hombres','Mujer':'total_mujeres'} )
        inegi_df = inegi_df.drop(['Unnamed: 4'], axis=1)

        #start to prepare the dataframe to obtain column anio and Periodo
        inegi_df[['periodo', 'drop1','drop2','anio']] = inegi_df.anio.str.split(expand=True)
        inegi_df= inegi_df.drop(['drop1','drop2'], axis=1)

        #split other columns and drop unnecessary data
        inegi_df['poblacion_subocupada'] = inegi_df.poblacion_subocupada.str.split('|', n=0, expand = True)
        inegi_df['total_hombres'] = inegi_df.total_hombres.str.split('|', n=0, expand = True)
        inegi_df['total_mujeres'] = inegi_df.total_mujeres.str.split('|', n=0, expand = True)

        #reorganization and normalization
        inegi_df = inegi_df[['anio','periodo','poblacion_subocupada','total_hombres','total_mujeres']]
        inegi_df['periodo'] = inegi_df['periodo'].replace('Primer','Trimestre 1')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Segundo','Trimestre 2')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Tercer','Trimestre 3')
        inegi_df['periodo'] = inegi_df['periodo'].replace('Cuarto','Trimestre 4')

        inegi_df['entidad'] = 'Puebla'

        return inegi_df

    def _poblacion_subocupada(self,df_total_hombres,df_total_mujeres,df_scrap_prepared):
        Poblacion_Subocupada = df_total_hombres.merge(df_total_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])

        Poblacion_Subocupada[['anio', 'periodo']] = Poblacion_Subocupada.anio.str.split("/",n=1, expand=True)


        Poblacion_Subocupada['periodo'] = Poblacion_Subocupada['periodo'].replace('01','Trimestre 1')
        Poblacion_Subocupada['periodo'] = Poblacion_Subocupada['periodo'].replace('02','Trimestre 2')
        Poblacion_Subocupada['periodo'] = Poblacion_Subocupada['periodo'].replace('03','Trimestre 3')
        Poblacion_Subocupada['periodo'] = Poblacion_Subocupada['periodo'].replace('04','Trimestre 4')

        
        #Poblacion_Subocupada['periodo'] = Poblacion_Subocupada['periodo'].astype('string')
        Poblacion_Subocupada['total_hombres'] = Poblacion_Subocupada['total_hombres'].apply(np.float)
        Poblacion_Subocupada['total_hombres'] = Poblacion_Subocupada['total_hombres'].apply(np.int)
        Poblacion_Subocupada['total_mujeres'] = Poblacion_Subocupada['total_mujeres'].apply(np.float)
        Poblacion_Subocupada['total_mujeres'] = Poblacion_Subocupada['total_mujeres'].apply(np.int)
        Poblacion_Subocupada['entidad'] = Poblacion_Subocupada['entidad'].astype('string')

        Poblacion_Subocupada['poblacion_subocupada'] = Poblacion_Subocupada['total_hombres'] + Poblacion_Subocupada['total_mujeres']
        Poblacion_Subocupada = Poblacion_Subocupada[['anio','periodo','poblacion_subocupada','total_hombres','total_mujeres', 'entidad']]

        Poblacion_Subocupada = pd.concat([Poblacion_Subocupada, df_scrap_prepared], ignore_index=True, sort=False)

        Poblacion_Subocupada['anio'] = Poblacion_Subocupada['anio'].astype('int')
        Poblacion_Subocupada['poblacion_subocupada'] = Poblacion_Subocupada['poblacion_subocupada'].astype('int')

        return Poblacion_Subocupada











