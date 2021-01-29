from Poblacion_Ocupada import Poblacion_ocupada

class MainOcupada ():

    def __init__(self):
        self.name='MainOcupada'
    def ocupada(self):
        
        #Call the IENGI API Poblacion Ocupada
        Poblacion_ocupada_total_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093950/es/0700/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_ocupada_total_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093956/es/0700/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_ocupada_puebla_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093950/es/07000021/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_ocupada_puebla_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093956/es/07000021/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        
        poblacion_ocupada = Poblacion_ocupada.PoblacionOcupada()
        
        Poblacion_Ocupada_df = poblacion_ocupada.excecute(Poblacion_ocupada_total_hombres,Poblacion_ocupada_total_mujeres,Poblacion_ocupada_puebla_hombres,Poblacion_ocupada_puebla_mujeres)
        
        return Poblacion_Ocupada_df
        # End of code