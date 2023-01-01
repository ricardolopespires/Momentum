from datetime import datetime









def data(publicacao):
    mes = publicacao[2:-4:].replace(' ','')
    dia = publicacao[:2]
    ano = publicacao[-4:]


   
    if mes == 'janeiro':
        mes = '01'
    elif mes == 'fevereiro':
        mes = '02'
    elif mes == 'março':
        mes = '03'
    elif mes == 'abril':
        mes = '04'
    elif mes == 'maio':
        mes = '05'
    elif mes == 'junho':
        mes = '06'
    elif mes == 'julho':
        mes = '07'
    elif mes == 'agosta':
        mes = '08'
    elif mes == 'setembro':
        mes = '09'
    elif mes == 'outubro':
        mes = '10'
    elif mes == 'novembro':
        mes = '11'
    else:
        mes = '12'

    data = (dia+'-'+mes+'-'+ano).replace(' ','')
    print(data)
    
    return datetime.strptime(data, '%d-%m-%Y')
    

    





def porcentagem(valor_anterior, valor_atual):
    porcetagem = 100
    try:
        calculo = porcetagem / int(valor_anterior)
    except:
        calculo = porcetagem / 1
    resultado =  calculo * valor_atual 
    return float("{0:.2f}".format(resultado))