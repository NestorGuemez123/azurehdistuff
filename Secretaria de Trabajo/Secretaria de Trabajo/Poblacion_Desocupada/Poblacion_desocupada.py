import requests
import json
import pandas as pd
import numpy as np


class PoblacionDesocupada ():

    def __init__ (self):
        self.name ="PoblacionDesocupada"

    def excecute (self,Poblacion_desocupada_total_hombres,Poblacion_desocupada_total_mujeres,Poblacion_desocupada_puebla_hombres,Poblacion_desocupada_puebla_mujeres):
        df_total_hombres = self._total_hombres(Poblacion_desocupada_total_hombres)
        df_total_mujeres = self._total_mujeres(Poblacion_desocupada_total_mujeres)
        df_puebla_hombres = self._puebla_hombres(Poblacion_desocupada_puebla_hombres)
        df_puebla_mujeres = self._puebla_mujeres(Poblacion_desocupada_puebla_mujeres)
        df_poblacion_desocupada = self._poblacion_desocupada(df_total_hombres, df_total_mujeres,df_puebla_hombres,df_puebla_mujeres)
        
        return df_poblacion_desocupada

    def _total_hombres (self, Poblacion_desocupada_total_hombres):
        response= requests.get(Poblacion_desocupada_total_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_desocupada_total_hombres_df = pd.DataFrame(data)

        Poblacion_desocupada_total_hombres_df = Poblacion_desocupada_total_hombres_df.rename(columns = {'OBS_VALUE' : 'total_hombres', 'COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_desocupada_total_hombres_df = Poblacion_desocupada_total_hombres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_desocupada_total_hombres_df['entidad'] = Poblacion_desocupada_total_hombres_df['entidad'].replace('0700','Nacional')
        
        return Poblacion_desocupada_total_hombres_df
    
    def _total_mujeres (self, Poblacion_desocupada_total_mujeres):
        response = requests.get(Poblacion_desocupada_total_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_desocupada_total_mujeres_df = pd.DataFrame(data)

        Poblacion_desocupada_total_mujeres_df = Poblacion_desocupada_total_mujeres_df.rename(columns = {'OBS_VALUE' : 'total_mujeres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_desocupada_total_mujeres_df = Poblacion_desocupada_total_mujeres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_desocupada_total_mujeres_df['entidad'] = Poblacion_desocupada_total_mujeres_df['entidad'].replace('0700','Nacional')

        return Poblacion_desocupada_total_mujeres_df

    def _puebla_hombres (self, Poblacion_desocupada_puebla_hombres):
        response = requests.get(Poblacion_desocupada_puebla_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_desocupada_puebla_hombres_df = pd.DataFrame(data)

        Poblacion_desocupada_puebla_hombres_df = Poblacion_desocupada_puebla_hombres_df.rename(columns = {'OBS_VALUE' : 'total_hombres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_desocupada_puebla_hombres_df = Poblacion_desocupada_puebla_hombres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_desocupada_puebla_hombres_df['entidad'] = Poblacion_desocupada_puebla_hombres_df['entidad'].replace('07000021','Puebla')

        return Poblacion_desocupada_puebla_hombres_df
    
    def _puebla_mujeres (self, Poblacion_desocupada_puebla_mujeres):
        response = requests.get(Poblacion_desocupada_puebla_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_desocupada_puebla_mujeres_df = pd.DataFrame(data)

        Poblacion_desocupada_puebla_mujeres_df = Poblacion_desocupada_puebla_mujeres_df.rename(columns = {'OBS_VALUE' : 'total_mujeres', 'COBER_GEO' : 'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_desocupada_puebla_mujeres_df = Poblacion_desocupada_puebla_mujeres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_desocupada_puebla_mujeres_df['entidad'] = Poblacion_desocupada_puebla_mujeres_df['entidad'].replace('07000021','Puebla')

        return Poblacion_desocupada_puebla_mujeres_df
    
    def _poblacion_desocupada(self,df_total_hombres, df_total_mujeres,df_puebla_hombres,df_puebla_mujeres):
        poblacion_desocupada_total = df_total_hombres.merge(df_total_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])
        poblacion_desocupada_puebla = df_puebla_hombres.merge(df_puebla_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])

        poblacion_desocupada_df = pd.concat([poblacion_desocupada_total, poblacion_desocupada_puebla], ignore_index=True, sort=False)

        poblacion_desocupada_df[['anio', 'periodo']] = poblacion_desocupada_df.anio.str.split("/",n=1, expand=True)


        poblacion_desocupada_df['periodo'] = poblacion_desocupada_df['periodo'].replace('01','Trimestre 1')
        poblacion_desocupada_df['periodo'] = poblacion_desocupada_df['periodo'].replace('02','Trimestre 2')
        poblacion_desocupada_df['periodo'] = poblacion_desocupada_df['periodo'].replace('03','Trimestre 3')
        poblacion_desocupada_df['periodo'] = poblacion_desocupada_df['periodo'].replace('04','Trimestre 4')

        poblacion_desocupada_df['anio'] = poblacion_desocupada_df['anio'].astype('int')
        poblacion_desocupada_df['total_hombres'] = poblacion_desocupada_df['total_hombres'].apply(np.float)
        poblacion_desocupada_df['total_hombres'] = poblacion_desocupada_df['total_hombres'].apply(np.int)
        poblacion_desocupada_df['total_mujeres'] = poblacion_desocupada_df['total_mujeres'].apply(np.float)
        poblacion_desocupada_df['total_mujeres'] = poblacion_desocupada_df['total_mujeres'].apply(np.int)

        poblacion_desocupada_df['poblacion_total'] = poblacion_desocupada_df['total_hombres'] + poblacion_desocupada_df['total_mujeres']
        poblacion_desocupada_df = poblacion_desocupada_df[['anio','periodo','poblacion_total','total_hombres','total_mujeres', 'entidad']]

        return poblacion_desocupada_df