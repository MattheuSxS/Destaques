from PySimpleGUI import PySimpleGUI as Sg
from Luna_back_end import qtd_dias
from Luna_back_end import resultado_aud as rat
from Luna_back_end import resultado_shr as shr


'''def qtd_dias():
    Sg.theme('Reddit')

    layout = [
        [Sg.Text('Obrigado Por Usar a Macro Luna!!!')],
        [Sg.Text('Deseja o resultado de quantos dias?', size=(26, 0)), Sg.Input(size=(5, 0), key='nday')],
        [Sg.Button('Enviar'), Sg.Button('Sair')],
    ]
    return Sg.Window('Macro Luna (o.O)', layout=layout, finalize=True)'''


def janela_opcao():
    Sg.theme('Reddit')

    layout = [
        [Sg.Text('Obrigado Por Usar a Macro Luna!!!')],
        [Sg.Text('Quais resultados deseja vê?')],
        [Sg.Checkbox('Audiência', key='aud'),
         Sg.Checkbox('Share', key='shr'),
         Sg.Checkbox('Audiência e Share', key='AudShare')],
        [Sg.Button('Enviar'), Sg.Button('Voltar'), Sg.Button('Sair')],
    ]
    return Sg.Window('Macro Luna (o.O)', layout=layout, finalize=True)


def janela_rat():

    header_list = [i for i in rat().columns.values]
    # Drops the first row in the table (otherwise the header names and the first row will be the same)
    data = rat().values.tolist()

    layout = [
        [Sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))],
        [Sg.Button('Voltar'), Sg.Button('Fechar', key='fechar1')]
    ]
    return Sg.Window('Macro Luna (o.O) - Audiência', layout=layout, finalize=True)


def janela_shr():

    header_list = [i for i in shr().columns.values]
    # Drops the first row in the table (otherwise the header names and the first row will be the same)
    data = rat().values.tolist()

    layout = [
        [Sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))],
        [Sg.Button('Voltar'), Sg.Button('Fechar', key='fechar2')]
    ]
    return Sg.Window('Macro Luna (o.O) - Share', layout=layout, finalize=True)


# Criar as janelas inicias
qtd_dias, opcao, result_rat, result_shr = qtd_dias(), None, None, None

# Criar um loop de leitura de eventos
while True:
    window, event, values = Sg.read_all_windows()
    # Quando janela for fechada
    if window == qtd_dias and (event == Sg.WINDOW_CLOSED or event == 'Sair'):
       break

    elif window == opcao and (event == Sg.WINDOW_CLOSED or event == 'Sair'):
        break

    # Quando queremos ir para próxima janela
    if window == qtd_dias and event == 'Enviar':
        qtd_dias.hide()
        opcao = janela_opcao()

    elif window == opcao and event == 'Enviar' and values['aud'] == True and values['shr'] == False:
        result_rat = janela_rat()
        opcao.close()
    elif window == opcao and event == 'Enviar' and values['shr'] == True and values['aud'] == False:
        result_shr = janela_shr()
        opcao.close()

    elif window == opcao and event == 'Enviar' and (
            (values['aud'] == True and values['shr'] == True) or values['AudShare'] == True):
        result_rat = janela_rat()
        result_shr = janela_shr()
        #opcao.hide()

    # Fechar abas
    elif window == result_rat and (event == 'fechar1' or event == Sg.WINDOW_CLOSED):
        result_rat.close()

    elif window == result_shr and (event == 'fechar2' or event == Sg.WINDOW_CLOSED):
        result_shr.close()

    elif window == result_rat and event == "fechar1" and window == result_shr and event == "fechar2":
        break

    if window == result_rat and event == "Voltar":
        result_rat.close()
        opcao = janela_opcao()

    elif window == result_shr and event == "Voltar":
        result_shr.close()
        opcao = janela_opcao()

    elif window == opcao and event == 'Voltar':
        opcao.close()
        qtd_dias.un_hide()

