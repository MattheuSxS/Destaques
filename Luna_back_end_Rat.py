import pandas as pd
import numpy as np
from datetime import datetime, timedelta  # Usado para manipular as "Datas"


def base_rat(baseanalise, df):

    resultado_aud = pd.DataFrame(columns=['Praça', 'Programas', 'Data_D-1', 'Posição', 'Repetição', 'Qtd_Exibicoes',
                                          'MédiaDoAno', '+pts_%', 'RecordeAno', 'Qtd_Vezes', 'Data', '|',
                                          'P_DiaDaSemana', 'R_DiaDaSemana', 'M_DiaSemana', 'DS_pts_%', 'R_Absoluto'])

    qtd_exibicoes, count, count1, count2, count3, audxtdur, audxtdur1, tvrxdur, tvrxdur1, maior, qtd_vezes, repeticao, repeticaoday, rank, rankday, pts, pts1, pts2, pts3 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # Variáveis para cálculos.

    for index, row in baseanalise.iterrows():
        # Quantidade de Exibições!
        for j in df['Programas']:
            if row['Programas'] == j:
                qtd_exibicoes += 1

        # Média do ano e Recorde do Ano.
        for index1, row1 in df.loc[(df['Programas'] == row['Programas'])].iterrows():
            count += row1['RAT']
            count1 += 1
            audxtdur += row1['AudxTDur']
            tvrxdur += row1['TvrxDur']
            if row1['RAT'] >= maior:
                maior = round(row1['RAT'])

        # Quantidade de vezes que repetiu aquele recorde
        for index2, row2 in df.loc[(df['Programas'] == row['Programas'])].iterrows():
            if maior == round(row2['RAT']):
                qtd_vezes += 1
                if qtd_vezes == 1:
                    data = row2['Data']

        # Quantidade de vezes que repetiu aquele posição
        lista = list(set(np.array(round(df.loc[(df['Programas'] == row['Programas'])]['RAT']))))
        lista.sort(reverse=True)
        for i in lista:
            if i == round(row['RAT']):
                rank = lista.index(i)  # Rankeamento
                for j in np.array(round(df.loc[(df['Programas'] == row['Programas'])]['RAT'])):
                    if j == i:
                        repeticao += 1

        # =============================== Dia da Semana ===============================
        for index3, row3 in df.loc[
            (df['Programas'] == row['Programas']) & (df['Diadasemana'] == row['Diadasemana'])].iterrows():
            count2 += row3['RAT']
            count3 += 1
            audxtdur1 += row3['AudxTDur']
            tvrxdur1 += row3['TvrxDur']

        lista = list(set(np.array(
            round(df.loc[(df['Programas'] == row['Programas']) & (df['Diadasemana'] == row['Diadasemana'])]['RAT']))))
        lista.sort(reverse=True)
        for i in lista:
            if i == round(row['RAT']):
                rankday = lista.index(i)
                for j in np.array(round(
                        df.loc[(df['Programas'] == row['Programas']) & (df['Diadasemana'] == row['Diadasemana'])]['RAT'])):
                    if j == i:
                        repeticaoday += 1

        mediaano = count / count1
        mediaano1 = (audxtdur / tvrxdur) * 100
        mediasemanal = count2 / count3
        mediasemanal1 = (audxtdur1 / tvrxdur1) * 100

        # ================== Anual ==========================
        pts = round(row['RAT']) - round(mediaano)
        if pts > 0:
            pts1 = (pts / mediaano) * 100
            res = str(pts) + ' pts' + ' (+' + str(round(pts1)) + '%)'
        else:
            res = ' '

        # ================== Dia da Semana ==========================
        pts2 = round(row['RAT']) - round(mediasemanal)
        if pts2 > 0:
            pts3 = (pts / mediasemanal) * 100
            res1 = str(pts2) + ' pts' + ' (+' + str(round(pts3)) + '%)'
        else:
            res1 = ' '

        # ================== Recorde Absoluto ========================== #
        if round(row['RAT']) == maior and round(row['RAT']) > 0:
            abs_record = 'Sim'
        else:
            abs_record = ' '

        # ================================= Resultado =================================
        resultado_aud = resultado_aud.append({'Programas': row['Programas'], 'Posição': rank + 1,
                                              'Repetição': str(repeticao) + 'x', 'Qtd_Exibicoes': qtd_exibicoes,
                                              'MédiaDoAno': str(round(mediaano)) + ' pts' + ' (' + str(
                                                  round(mediaano1)) + '%)', '+pts_%': res,
                                              'RecordeAno': str(maior) + ' pts',
                                              'Qtd_Vezes': str(qtd_vezes) + ' x', 'Data': data,
                                              '|': ' ', 'P_DiaDaSemana': rankday + 1,
                                              'R_DiaDaSemana': str(repeticaoday) + 'x',
                                              'M_DiaSemana': str(round(mediasemanal)) + ' pts' + ' (' + str(
                                                  round(mediasemanal1)) + '%)', 'DS_pts_%': res1,
                                              'R_Absoluto': abs_record}, ignore_index=True)

        # Reseta os valores das variáveis cada vez que entra no loop.
        qtd_exibicoes, count, count1, count2, count3, audxtdur, audxtdur1, tvrxdur, tvrxdur1, maior, qtd_vezes, repeticao, repeticaoday, rank, rankday, pts, pts1, pts2, pts3 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # Variáveis para cálculos.

    resultado_aud['Data_D-1'] = list(baseanalise['Data'])
    resultado_aud['Praça'] = list(baseanalise['Praca'])

    resultado_aud['Data_D-1'] = pd.to_datetime(resultado_aud['Data_D-1'], format='%d/%m/%Y')

    rat = 'CGCOM_' + str((datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')) + ' ' + df['Praca'].iloc[
        -1] + '.xlsx'  # CONCATENAR varias variáveis para geraro nome do arquivo excel

    resultado_aud.to_excel(rat, sheet_name=df['Praca'].iloc[-1], na_rep='', float_format=None, columns=None,
                           header=True, index=False, index_label=None, startrow=0, startcol=0, engine=None,
                           merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)

    return resultado_aud
