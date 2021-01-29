from Poblacion_Subocupada import Poblacion_subocupada 
from Poblacion_Mayor import read_file
from Poblacion_Subocupada import scrap_

class MainSubocupada():

    def __init__(self):
        self.name = 'MainSubocupada'
        
    def subocupada(self):

        Poblacion_subocupada_total_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/447025/es/0700/false/BIE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_subocupada_total_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/446845/es/0700/false/BIE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        url_scraping = 'https://www.inegi.org.mx/sistemas/olap/proyectos/bd/encuestas/hogares/enoe/2010_pe_ed15/psub.asp?s=est&proy=enoe_pe_ed15_psub&p=enoe_pe_ed15'
        
        scrap = scrap_.WebScrap()
        leer_archivo = read_file.ReadFile()
        subocupada = Poblacion_subocupada.PoblacionSubocupada()

        scrap.scrap(url_scraping) 
        path_file = leer_archivo.readFile()
        poblacion_subocupada = subocupada.execute(Poblacion_subocupada_total_hombres,Poblacion_subocupada_total_mujeres,url_scraping,path_file)

        return poblacion_subocupada