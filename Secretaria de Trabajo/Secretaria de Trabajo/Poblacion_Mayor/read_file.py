import os
import re
import datetime
import pandas as pd

class ReadFile():

    def __init__(self):
        self.name = "ReadFile"
   
    def readFile(self):

        file_path = os.getcwd()+"\\data"
        listArc = os.listdir(file_path)
        val = str(datetime.date.today()).split('-')
        date_name=''.join(val)
        file_name = "INEGI_Exporta_"+date_name


        last_file_name =listArc[len(listArc)-1]
        #print(last_file_name)
        if last_file_name.startswith(file_name):
            path_file=file_path+"\\"+last_file_name
        
        return path_file

