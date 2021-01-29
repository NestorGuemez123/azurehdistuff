from Poblacion_Desocupada import Poblacion_desocupada


class MainDesocupada():

    def __init__(self):
        self.name ='MainDesocupada'

    def desocupada(self):

        # Call the IENGI API Poblacion Desocupada
        Poblacion_desocupada_total_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093974/es/0700/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_desocupada_total_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093975/es/0700/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_desocupada_puebla_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093974/es/07000021/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_desocupada_puebla_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200093975/es/07000021/false/BISE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'

        poblacion_desocupada = Poblacion_desocupada.PoblacionDesocupada()

        Poblacion_desocupada_df = poblacion_desocupada.excecute(
            Poblacion_desocupada_total_hombres, Poblacion_desocupada_total_mujeres, Poblacion_desocupada_puebla_hombres, Poblacion_desocupada_puebla_mujeres)

        return Poblacion_desocupada_df
