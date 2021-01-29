import pandas as pd
import numpy as np

class Prepare():
    def __init__(self):
        self.name = 'Prepare'
    
    def prepared(self,Poblacion_desocupada,Poblacion_mayor,Poblacion_ocupada,Poblacion_subocupada):
        
        desocupada_df = Poblacion_desocupada
        desocupada_df.rename(columns = {"poblacion_total":"desocupada"}, inplace = True)
        desocupada_df = desocupada_df[['anio','periodo','entidad','desocupada']]

        ocupada_df = Poblacion_ocupada
        ocupada_df.rename(columns = {"poblacion_total":"ocupada"}, inplace = True)
        ocupada_df = ocupada_df[['anio','periodo','entidad','ocupada']]

        subocupada_df = Poblacion_subocupada
        subocupada_df.rename(columns = {"poblacion_subocupada":"subocupada"}, inplace = True)
        subocupada_df = subocupada_df[['anio','periodo','entidad','subocupada']]

        mayor_df = Poblacion_mayor
        mayor_df.rename(columns = {"poblacion_mayor":"mayor"}, inplace = True)
        mayor_df = mayor_df[['anio','periodo','entidad','mayor']]

        result = pd.merge(desocupada_df,ocupada_df, how="inner", on=['anio','periodo','entidad'],sort=True)
        result = pd.merge(result,subocupada_df, how="inner", on=['anio','periodo','entidad'],sort=True)
        result = pd.merge(result,mayor_df, how="inner", on=['anio','periodo','entidad'],sort=True)
        result["pea"] = result["ocupada"]+result["desocupada"]
        result["npea"]=-1
        result["trabajadores_independientes"]=-1
        result["tasa_desempleo"] = result["desocupada"]/result["pea"]
        result["tasa_participacion"] = result["pea"]/result["mayor"]
        result["tasa_subocupada"] = result["subocupada"]/result["pea"]
        result.index.name = 'id'

        return result
