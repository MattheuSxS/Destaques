import PySimpleGUI as Sg
import pandas as pd  # DataFrame
from datetime import datetime, timedelta  # Usado para manipular as "Datas"
import Luna_back_end_Rat as brat
import Luna_back_end_Shr as bshr
# from Luna_front_end import qtd_dias


def audxtdur(Tdur, Rat_Shr):
    tempo = sum(int(i) * 60**index for index, i in enumerate(Tdur.split(":")[::-1]))
    tempo = tempo/1440
    return round(tempo * Rat_Shr, 6)


filename = Sg.popup_get_file(
    'filename to open', no_window=True, file_types=(("CSV Files", "*.csv"),))

df_test = pd.read_csv(filename, sep=';', engine='python', parse_dates=True)

df_test['Data'] = pd.to_datetime(df_test['Data'], format='%d/%m/%Y')  # Muda o formato da data na base
df_test['RAT'] = df_test['RAT'].apply(lambda x: float(x.split()[0].replace(',', '.')))  # Trocar virgula por ponto
df_test['SHR'] = df_test['SHR'].apply(lambda x: float(x.split()[0].replace(',', '.')))  # Trocar virgula por ponto

# Cria a coluna ano
df_test['Ano'] = df_test['Data'].dt.year
# Usa a função audxtdur para calcular Tdur vs RAT
df_test['AudxTDur'] = [audxtdur(df_test['Tdur'][x], df_test['RAT'][x]) for x in range(len(df_test['RAT']))]
# Usa a função audxtdur para calcular Tdur vs SHR
df_test['AudxTDur_Shr'] = [audxtdur(df_test['Tdur'][x], df_test['SHR'][x]) for x in range(len(df_test['SHR']))]
# Cálcula ( RAT / SHR ) * 100, Para gerar o %TVR, o resultado sai com 6 casas decimais
df_test['%TVR'] = round((df_test['RAT'] / df_test['SHR']) * 100, 6)
# Cálcula ( SHR / RAT ) * 100, Para gerar o %TVR, o resultado sai com 6 casas decimais
df_test['%TVR_Shr'] = round((df_test['SHR'] / df_test['RAT']) * 100, 6)
# Usa a função audxtdur para calcular Tdur vs RAT
df_test['TvrxDur'] = [audxtdur(df_test['Tdur'][x], df_test['%TVR'][x]) for x in range(len(df_test['RAT']))]
# Usa a função audxtdur para calcular Tdur vs SHR
df_test['TvrxDur_Shr'] = [audxtdur(df_test['Tdur'][x], df_test['%TVR_Shr'][x]) for x in range(len(df_test['SHR']))]


AntesAbril = str(datetime.today().year) + '-' + '04' + '-' + '01'  # Gera a data para o filtro
AposAbril = str(datetime.today().year) + '-' + '01' + '-' + '01'  # Gera a data para o filtro

# ================================================ xxx ================================================ #
if datetime.today().strftime('%Y-%m-%d') < AntesAbril:  # Compara se a data de hoje é menor que 01/04/(ano atual)
    OneYear = (str(datetime.today().year - 1)+'-01-01')
    df = df_test.loc[df_test['Data'] >= OneYear]  # Caso sim, pegamos os dados de >= 01/01/2020
else:
    df = df_test.loc[df_test['Data'] >= AposAbril]  # Caso não, pegamos os dados de >= 01/01/2021


def leitura():
    return Sg.read_all_windows()


def qtd_dias():
    Sg.theme('Reddit')

    layout = [
        [Sg.Text('Obrigado Por Usar a Macro Luna!!!')],
        #[Sg.Text('Deseja o resultado de quantos dias?', size=(26, 0)), Sg.Input(size=(5, 0), key='nday')],
        [Sg.Text('Quantidade de caracteres'), Sg.Combo(values=list(
            range(1, 11)), key='nday', default_value=1, size=(3, 1))],
        [Sg.Button('Enviar'), Sg.Button('Sair')],
    ]
    return Sg.Window('Macro Luna (o.O)', layout=layout, finalize=True)


def numerodia(numero):
    while True:  # O usuario ficará e um loop infinito até ele digitar o número de dias válidos
        try:
            window, event, values = leitura()
            '''Só aceita números "Inteiros", ou seja, 1,2,3... | Não aceita 1.2 | 1,2 | @!$%¨¨&*()_+ | abcdfer'''
            nday = int(values['nday'])#int(input("Número de dias? "))
            if nday == 0:  # Se o usuário digitar Zero ele entrará em um loop
                print(" Zero não é um dia válido!!")
            else:
                break
        except Exception:
            print("Houve um problema com o número obtido. Tente novamente.")

    return nday


def resultday(day):
    return (datetime.today() - timedelta(days=numerodia(day))).strftime('%Y-%m-%d')


# NumeroDias = resultday(qtd_dias())
BaseAnalise = df.loc[df['Data'] >= resultday(qtd_dias())]  # Range de datas escolhida pelo usuário


def resultado_aud():
    return brat.base_rat(BaseAnalise, df_test)


def resultado_shr():
    return bshr.base_shr(BaseAnalise, df_test)
