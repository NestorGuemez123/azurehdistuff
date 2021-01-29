from Poblacion_Mayor import Poblacion_mayor
from Poblacion_Mayor import read_file
from Poblacion_Mayor import scrap_ 

class MainMayor ():

    def __init__ (self):
        self.name = 'MainMayor'
    
    def mayor(self):
        
        #Call the IENGI API Poblacion Ocupada
        Poblacion_mayor_total_mujeres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/446911/es/0700/false/BIE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        Poblacion_mayor_total_hombres = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/446737/es/0700/false/BIE/2.0/5e7385c4-b4eb-74a0-067d-bed192198099?type=json'
        url_scraping= 'https://www.inegi.org.mx/sistemas/olap/proyectos/bd/encuestas/hogares/enoe/2010_pe_ed15/p15.asp?s=est&proy=enoe_pe_ed15_pmay&p=enoe_pe_ed15'

        scrap = scrap_.WebScrap()
        leer_archivo = read_file.ReadFile()
        poblacion_mayor = Poblacion_mayor.PoblacionMayor()
        
        scrap.scrap(url_scraping) 
        path_file = leer_archivo.readFile()
        Poblacion_Mayor_df = poblacion_mayor.execute(Poblacion_mayor_total_mujeres,Poblacion_mayor_total_hombres,path_file)
        
        return Poblacion_Mayor_df
        # End of code