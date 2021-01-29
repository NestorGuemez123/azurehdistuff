import requests
import json
import pandas as pd
import numpy as np


class PoblacionOcupada ():

    def __init__ (self):
        self.name ="PoblacionOcupada"

    def excecute(self, Poblacion_ocupada_total_hombres,Poblacion_ocupada_total_mujeres,Poblacion_ocupada_puebla_hombres,Poblacion_ocupada_puebla_mujeres):
        df_total_hombres = self._total_hombres(Poblacion_ocupada_total_hombres)
        df_total_mujeres = self._total_mujeres(Poblacion_ocupada_total_mujeres)
        df_puebla_hombres = self._puebla_hombres(Poblacion_ocupada_puebla_hombres)
        df_puebla_mujeres = self._puebla_mujeres(Poblacion_ocupada_puebla_mujeres)
        df_poblacion_ocupada = self._poblacion_ocupada(df_total_hombres, df_total_mujeres,df_puebla_hombres,df_puebla_mujeres)

        return df_poblacion_ocupada

    def _total_hombres (self, Poblacion_ocupada_total_hombres):
        response= requests.get(Poblacion_ocupada_total_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_ocupada_total_hombres_df = pd.DataFrame(data)

        Poblacion_ocupada_total_hombres_df = Poblacion_ocupada_total_hombres_df.rename(columns = {'OBS_VALUE' : 'total_hombres', 'COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_ocupada_total_hombres_df = Poblacion_ocupada_total_hombres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_ocupada_total_hombres_df['entidad'] = Poblacion_ocupada_total_hombres_df['entidad'].replace('0700','Nacional')

        return Poblacion_ocupada_total_hombres_df    
    
    def _total_mujeres(self, Poblacion_ocupada_total_mujeres):
        response = requests.get(Poblacion_ocupada_total_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_ocupada_total_mujeres_df = pd.DataFrame(data)

        Poblacion_ocupada_total_mujeres_df = Poblacion_ocupada_total_mujeres_df.rename(columns = {'OBS_VALUE' : 'total_mujeres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_ocupada_total_mujeres_df = Poblacion_ocupada_total_mujeres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_ocupada_total_mujeres_df['entidad'] = Poblacion_ocupada_total_mujeres_df['entidad'].replace('0700','Nacional')

        return Poblacion_ocupada_total_mujeres_df
    
    def _puebla_hombres (self, Poblacion_ocupada_puebla_hombres):
        response = requests.get(Poblacion_ocupada_puebla_hombres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_ocupada_puebla_hombres_df = pd.DataFrame(data)

        Poblacion_ocupada_puebla_hombres_df = Poblacion_ocupada_puebla_hombres_df.rename(columns = {'OBS_VALUE' : 'total_hombres','COBER_GEO':'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_ocupada_puebla_hombres_df = Poblacion_ocupada_puebla_hombres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_ocupada_puebla_hombres_df['entidad'] = Poblacion_ocupada_puebla_hombres_df['entidad'].replace('07000021','Puebla')

        return Poblacion_ocupada_puebla_hombres_df

    def _puebla_mujeres (self, Poblacion_ocupada_puebla_mujeres):
        response = requests.get(Poblacion_ocupada_puebla_mujeres)
        status = response.status_code 

        if status != 200:

            print("Error en la consulta , condigo {}".format(status))

        raw_data = response.json()
        data = raw_data['Series'][0]['OBSERVATIONS']
        Poblacion_ocupada_puebla_mujeres_df = pd.DataFrame(data)

        Poblacion_ocupada_puebla_mujeres_df = Poblacion_ocupada_puebla_mujeres_df.rename(columns = {'OBS_VALUE' : 'total_mujeres', 'COBER_GEO' : 'entidad','TIME_PERIOD' : 'anio'} )
        Poblacion_ocupada_puebla_mujeres_df = Poblacion_ocupada_puebla_mujeres_df.drop(columns = {'OBS_EXCEPTION','OBS_STATUS','OBS_SOURCE','OBS_NOTE'})
        Poblacion_ocupada_puebla_mujeres_df['entidad'] = Poblacion_ocupada_puebla_mujeres_df['entidad'].replace('07000021','Puebla')

        return Poblacion_ocupada_puebla_mujeres_df

    def _poblacion_ocupada (self,df_total_hombres, df_total_mujeres,df_puebla_hombres,df_puebla_mujeres):
        
        poblacion_ocupada_total = df_total_hombres.merge(df_total_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])
        poblacion_ocupada_puebla = df_puebla_hombres.merge(df_puebla_mujeres.set_index('anio', 'entidad'), on=['anio', 'entidad'])

        poblacion_ocupada_df = pd.concat([poblacion_ocupada_total, poblacion_ocupada_puebla], ignore_index=True, sort=False)

        poblacion_ocupada_df[['anio', 'periodo']] = poblacion_ocupada_df.anio.str.split("/",n=1, expand=True)


        poblacion_ocupada_df['periodo'] = poblacion_ocupada_df['periodo'].replace('01','Trimestre 1')
        poblacion_ocupada_df['periodo'] = poblacion_ocupada_df['periodo'].replace('02','Trimestre 2')
        poblacion_ocupada_df['periodo'] = poblacion_ocupada_df['periodo'].replace('03','Trimestre 3')
        poblacion_ocupada_df['periodo'] = poblacion_ocupada_df['periodo'].replace('04','Trimestre 4')

        poblacion_ocupada_df['anio'] = poblacion_ocupada_df['anio'].astype('int')
        poblacion_ocupada_df['total_hombres'] = poblacion_ocupada_df['total_hombres'].apply(np.float)
        poblacion_ocupada_df['total_hombres'] = poblacion_ocupada_df['total_hombres'].apply(np.int)
        poblacion_ocupada_df['total_mujeres'] = poblacion_ocupada_df['total_mujeres'].apply(np.float)
        poblacion_ocupada_df['total_mujeres'] = poblacion_ocupada_df['total_mujeres'].apply(np.int)

        poblacion_ocupada_df['poblacion_total'] = poblacion_ocupada_df['total_hombres'] + poblacion_ocupada_df['total_mujeres']
        poblacion_ocupada_df = poblacion_ocupada_df[['anio','periodo','poblacion_total','total_hombres','total_mujeres', 'entidad']]

        return poblacion_ocupada_df