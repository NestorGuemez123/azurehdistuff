import linecache
import sys

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

try:
    from Poblacion_Desocupada import mainDesocupada
    from Poblacion_Mayor import mainMayor
    from Poblacion_Ocupada import mainOcupada
    from Poblacion_Subocupada import mainSubocupada
    from prepare import Prepare

    def main():
        desocupada = mainDesocupada.MainDesocupada()
        mayor = mainMayor.MainMayor()
        ocupada = mainOcupada.MainOcupada()
        subocupada = mainSubocupada.MainSubocupada()
        prepare = Prepare()

        Poblacion_desocupada = desocupada.desocupada()
        Poblacion_mayor = mayor.mayor()
        Poblacion_ocupada = ocupada.ocupada()
        Poblacion_subocupada = subocupada.subocupada()

        df = prepare.prepared(
            Poblacion_desocupada, Poblacion_mayor, Poblacion_ocupada, Poblacion_subocupada)
        
        csv_path = os.path.abspath('DataPuebla.csv')
        df.to_csv(csv_path, encoding='utf-8')
        print(csv_path)
        sys.exit(0)

    if __name__ == '__main__':
        main()

except Exception as e:
    PrintException()
    sys.exit(1)
