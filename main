import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

acoes = ['SBSP3.SA','AAPL','MSFT','GOOGL','NVDA','KO','PG',"NESN.SW","ULVR.L","OR.PA","SAP.DE","DGE.L","MC.PA","SIE.DE","AIR.PA","RDSA.AS","ASML.AS","NOVN.SW","ROG.SW","SAN.PA","BN.PA","BAS.DE","VOW3.DE","BMW.DE","ENEL.MI","IBE.MC","PHIA.AS","SU.PA","AD.AS","ABI.BR","CS.PA","LHA.DE","ALV.DE","AXA.PA","BP.L","AZN.L","GSK.L",'PEP','WMT','JPM','V','MA','JNJ','PFE','UNH','XOM','CVX','NEE','MMM','HON','BA','PG','XOM','CVX','BLK','MSFT','AAPL','O','SPG','T','RF','ALLY','NXST','WEN','FIBK', 'STNG','CRI','VRTS','DHT','MO','BTI', 'PEAK','VZ','T', 'KMI','MMM','DVN','WHR','PFE','NEE','ADBE', 'TSLA', 'META', 'CSCO', 'ORCL', 'INTC', 'CRM', 'QCOM', 'SNOW', 'PANW','ABBV', 'TMO', 'MDT', 'SYK', 'CI', 'HUM', 'REGN', 'VRTX', 'BMY', 'AMGN','COST', 'MCD', 'DIS', 'TGT', 'HD', 'LOW', 'NKE', 'WBA', 'KR', 'DG','SLB', 'EOG', 'HAL', 'PXD', 'MPC', 'VLO', 'BKR', 'FANG', 'PSX', 'ENB','GS', 'C', 'AXP', 'BAC', 'USB', 'MS', 'BK', 'TFC', 'AIG', 'CME','VIVT3.SA','BCE.TO', 'T.TO', 'RCI-B.TO', 'ENB.TO', 'TRP.TO', 'PPL.TO', 'IPL.TO', 'FTS.TO', 'EMA.TO', 'AQN.TO', 'CU.TO', 'BIP-UN.TO', 'BEP-UN.TO', 'CPX.TO', 'TA.TO', 'SU.TO', 'CNQ.TO', 'IMO.TO', 'TRI.TO', 'MFC.TO', 'SLF.TO', 'GWO.TO', 'BNS.TO', 'TD.TO', 'RY.TO', 'CM.TO', 'NA.TO', 'MRU.TO', 'L.TO', 'SAP.TO','BBSE3.SA','RDOR3.SA','MDIA3.SA', 'SLCE3.SA', 'BRAP4.SA', 'RAIL3.SA', 'ARZZ3.SA', 'HAPV3.SA', 'FLRY3.SA', 'PARD3.SA', 'QUAL3.SA','PSSA3.SA','TIMS3.SA','ITUB4.SA','BBDC4.SA','BBAS3.SA','SANB11.SA','SAPR4.SA','CSMG3.SA','ABEV3.SA', 'KLBN11.SA', 'SUZB3.SA', 'MRFG3.SA', 'BRFS3.SA','BBSE3.SA','VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ITSA4.SA', 'SANB11.SA', 'SANB4.SA','SANB3.SA','SAPR4.SA','TAEE4.SA','TAEE11.SA','ISAE4.SA','SAPR11.SA','VINO11.SA','HGLG11.SA','TAEE11.SA','EGIE3.SA','CMIG4.SA','TRPL4.SA','CPLE6.SA','ENBR3.SA', 'ALUP11.SA', 'NEOE3.SA', 'ENGI11.SA', 'CEEB3.SA']
acoes = list(set(acoes)) 

hoje = datetime.now()
inicio = hoje - timedelta(days=6*365)  # Últimos 6 anos

minhas_acoes = [ 'RAIL3.SA', 'ARZZ3.SA','PEP','WMT','ENB.TO', 'TRP.TO',"ASML.AS","NOVN.SW"]

dy_por_moeda = {
        "BRL": 6,
        "USD": 3,
        "CAD": 4,
        "EUR": 2.5
    }

# Função para coletar dados históricos e calcular indicadores
def calcular_indicadores_historicos(acoes, inicio, hoje):
    resultados = []
    for acao in acoes:
        try:
            ticker = yf.Ticker(acao)
            hist = ticker.history(start=inicio, end=hoje)
            pais = ticker.info['currency']

            # Verificar se 'Dividends' está presente no DataFrame
            if 'Dividends' not in hist.columns:
                print(f"Sem dados de dividendos para {acao}. Pulando.")
                continue

            # Dividendos e número de pagamentos por ano
            dividendos = hist['Dividends'].resample('YE').sum()  # Soma dos dividendos por ano

            # Preço atual e preço médio
            preco_atual = round(hist['Close'].iloc[-1], 2)  # Último preço
            preco_medio = round(hist['Close'].mean(), 2)   # Preço médio no período

            # Informações financeiras
            infos = ticker.info
            lpa = infos.get('trailingEps', 0)  # Lucro por Ação
            vpa = infos.get('bookValue', 0)    # Valor Patrimonial por Ação
            setor = infos.get('sector', 'Não informado')
            nome_empresa = infos.get('longName', 'Não informado')


            # Calcular indicadores usando Preço Médio
            indicadores = pd.DataFrame()
            indicadores['Dividendos'] = dividendos
            indicadores['Preço Médio'] = preco_medio
            indicadores['Preço Atual'] = preco_atual
            indicadores['DY Médio (%)'] = (indicadores['Dividendos'] / preco_medio) * 100
            indicadores['DY Atual (%)'] = (indicadores['Dividendos'] / preco_atual) * 100
            indicadores['P/L Médio'] = preco_medio / lpa if lpa > 0 else None
            indicadores['P/L Atual'] = preco_atual / lpa if lpa > 0 else None
            indicadores['P/VP Médio'] = preco_medio / vpa if vpa > 0 else None
            indicadores['P/VP Atual'] = preco_atual / vpa if vpa > 0 else None
            

            # Filtrar e calcular médias
            indicadores = indicadores.dropna()
            media_dy_medio = indicadores['DY Médio (%)'].mean()
            media_dy_atual = indicadores['DY Atual (%)'].mean()
            media_pl_medio = indicadores['P/L Médio'].mean() if 'P/L Médio' in indicadores else None
            media_pl_atual = indicadores['P/L Atual'].mean() if 'P/L Atual' in indicadores else None
            media_pvp_medio = indicadores['P/VP Médio'].mean() if 'P/VP Médio' in indicadores else None
            media_pvp_atual = indicadores['P/VP Atual'].mean() if 'P/VP Atual' in indicadores else None
            Dividendos = (indicadores['Dividendos'].sum())/6

            def get_sifrao(moeda):
                simbolos = {
                    'BRL': 'R$',
                    'USD': '$',
                    'EUR': '€',
                    'GBP': '£',
                    'CAD': 'C$',
                    'JPY': '¥',
                    'GBP': '£',
                    'CHF': 'Fr.',
                    'SEK': 'kr',
                    'NOK': 'kr',
                    'DKK': 'kr',
                    'PLN': 'zł',
                    'CZK': 'Kč',
                    'HUF': 'Ft',
                    'ISK': 'kr'
                }
                return simbolos.get(moeda, moeda)  # Se não encontrar, retorna o código mesmo

            moeda = get_sifrao(pais)

            # Adicionar resultados ao DataFrame final
            resultados.append({
                "Ticker": acao,
                "Nome da Empresa": nome_empresa,
                "Setor Atuante": setor,
                "Pais" : pais,
                "Moeda": moeda,
                "Preço Atual": preco_atual,
                "Preço Médio": preco_medio,
                "Valor Teto": None,
                "Dividendos": Dividendos,
                "DY Médio (%)": media_dy_medio,
                "DY Atual (%)": media_dy_atual,
                "P/L Médio": media_pl_medio,
                "P/L Atual": media_pl_atual,
                "P/VP Médio": media_pvp_medio,
                "P/VP Atual": media_pvp_atual
            })


        except Exception as e:
            print(f"Erro ao processar {acao}: {e}")
            resultados.append({
                "Ticker": acao,
                "Nome da Empresa": None,
                "Setor Atuante": None,
                "Pais" : None,
                "Moeda": None,
                "Preço Atual": None,
                "Preço Médio": None,
                "Valor Teto": None,
                "DY Médio (%)": None,
                "DY Atual (%)": None,
                "P/L Médio": None,
                "P/L Atual": None,
                "P/VP Médio": None,
                "P/VP Atual": None,
            })
    return pd.DataFrame(resultados)
def grafico(grafico):
    plt.figure(figsize=(14, 8))
    
    largura_barras = 0.4 
    x = range(len(grafico))

    # Barras de DY Atual (azul)
    barras_dy_atual = plt.bar(
        [i - largura_barras / 2 for i in x], 
        grafico['DY Atual (%)'], 
        width=largura_barras, 
        label='DY Atual (%)', 
        color='blue', alpha=0.6
    )

    # Barras de DY Médio (vermelho)
    barras_dy_medio = plt.bar(
        [i + largura_barras / 2 for i in x], 
        grafico['DY Médio (%)'], 
        width=largura_barras, 
        label='DY Médio (%)', 
        color='red', alpha=0.6
    )

    # Adicionar texto dentro das barras de DY Atual
    for barra in barras_dy_atual:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # Centro da barra
            altura / 2,                             # Meio da barra
            f"{altura:.2f}%",                       # Texto formatado como porcentagem
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )

    for barra in barras_dy_medio:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # Centro da barra
            altura / 2,                             # Meio da barra
            f"{altura:.2f}%",                       # Texto formatado como porcentagem
            ha='center', va='center', color='white', fontsize=10, fontweight='bold'
        )
    
    # Configurações do gráfico
    plt.xticks(x, grafico['Ticker'], rotation=45)
    plt.ylabel("Dividend Yield (%)")
    plt.title("Comparação do Dividend Yield (DY) - Atual x Médio")
    plt.legend()
    plt.tight_layout()
    plt.show()
def grafico_2(grafico):
    plt.figure(figsize=(14, 8))
    
    largura_barras = 0.25 
    x = range(len(grafico))

    # Barras de DY Atual (azul)
    barras_dy_atual = plt.bar(
        [i - largura_barras for i in x], 
        grafico['Preço Atual'], 
        width=largura_barras, 
        label='Preço Atual', 
        color='blue', alpha=0.6
    )

    # Barras de DY Médio (vermelho)
    barras_dy_medio = plt.bar(
        [i for i in x], 
        grafico['Preço Médio'], 
        width=largura_barras, 
        label='Preço Médio', 
        color='red', alpha=0.6
    )

    # Barras adicionais (verde)
    barras_extra = plt.bar(
        [i + largura_barras for i in x], 
        grafico['Valor Teto'], 
        width=largura_barras, 
        label='Valor Teto', 
        color='green', alpha=0.6
    )
    
    def barras(barras_plot):
        for i, barra in enumerate(barras_plot):
            altura = barra.get_height()
            if not pd.isna(altura):
                moeda = grafico.iloc[i]['Moeda']  # Pega a moeda da linha correspondente
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    altura / 2,
                    f"{moeda}{altura:.2f}",
                    ha='center', va='center',
                    color='black', fontsize=10,
                    fontweight='bold', rotation=90
                )
    barras(barras_dy_atual)
    barras(barras_dy_medio)
    barras(barras_extra)
    
    # Configurações do gráfico
    plt.xticks(x, grafico['Ticker'], rotation=45)
    plt.ylabel("Preço")
    plt.title("Comparação do Preço - Atual x Médio x Teto")
    plt.legend()
    plt.tight_layout()
    plt.show()    
def media_geral (acoes):
    DY = acoes['DY Atual (%)'].mean()
    DY_m = acoes["DY Médio (%)"].mean()
    PL = acoes['P/L Atual'].mean()
    PL_m = acoes['P/L Médio'].mean()
    PVP = acoes['P/VP Atual'].mean()
    PVP_m = acoes['P/VP Médio'].mean()
    print(f'DY {DY:.2f}, P/L {PL:.2f},P/VP {PVP:.2f}')
    print(f'DY {DY_m:.2f}, P/L {PL_m:.2f},P/VP {PVP_m:.2f}')
def calcular_valor_teto(df):
    return df.apply(
        lambda row: round(
            row["Dividendos"] / (dy_por_moeda.get(row["Pais"], 5) / 100),
            2,
        ),
        axis=1,
    )
# Caso procure por alguma ação para comprar
def comparar_precos (resultado):
    resultado["DY Atual (%)"] = pd.to_numeric(resultado["DY Atual (%)"], errors='coerce')
    resultado = resultado.dropna(subset=['DY Atual (%)', 'P/L Médio', 'P/VP Médio'])
    resultado["DY Mínimo"] = resultado["Pais"].map(dy_por_moeda).fillna(5)
    filtro_barsi = resultado[
    (resultado['DY Atual (%)'] > resultado["DY Mínimo"] ) & 
    (resultado['P/L Médio'] < 15) & 
    (resultado['P/VP Médio'] < 2)
    ].copy()
    filtro_barsi["Valor Teto"] = calcular_valor_teto(filtro_barsi)
    filtro_barsi = filtro_barsi.sort_values(by="Dividendos",ascending=False).reset_index(drop=True)
    grafico(filtro_barsi)
    grafico_2(filtro_barsi)
    filtro_barsi = filtro_barsi.drop(columns=["DY Atual (%)", "P/L Médio", "P/L Atual","P/VP Médio","P/VP Atual","DY Médio (%)"])
    print(filtro_barsi)
    return filtro_barsi
# Caso jà tenha comprado alguma ação
def acoes_compradas (resultado):
    resultado["DY Atual (%)"] = pd.to_numeric(resultado["DY Atual (%)"], errors='coerce')
    resultado = resultado.dropna(subset=['DY Atual (%)', 'P/L Médio', 'P/VP Médio'])
    resultado["Valor Teto"] = calcular_valor_teto(resultado)
    resultado = resultado.sort_values(by="Dividendos",ascending=False).reset_index(drop=True)
    resultado["DY Mínimo"] = resultado["Pais"].map(dy_por_moeda).fillna(5)
    grafico(resultado)
    grafico_2(resultado)
    resultado = resultado.drop(columns=["DY Atual (%)", "P/L Médio", "P/L Atual","P/VP Médio","P/VP Atual","DY Médio (%)"])
    print(resultado)
    return resultado

resultado_meu = calcular_indicadores_historicos(minhas_acoes, inicio, hoje)
resultado_meu = acoes_compradas(resultado_meu)

resultado = calcular_indicadores_historicos(acoes, inicio, hoje)
resultado = comparar_precos (resultado)

IR_por_pais = {
        "BRL": 0.15,
        "USD": 0.15,
        "CAD": 0.3,
        "EUR": 0.28  # varia por pais mas o maior é portugal com 28% por isso ele
    }
Valor = 500 # valor que você tem para usar
pais = 'BRL' # qual pais você vai comprar

def compra(resultado):
    Final = pd.DataFrame()
    resultado = resultado[resultado['Pais'] == pais]
    Final['Ticker'] = resultado['Ticker']
    Final['Nome da Empresa'] = resultado['Nome da Empresa']
    Final['Numero de Acoes'] = round((Valor / resultado['Preço Atual']))
    Final['Total de Dividendo'] = round(Final['Numero de Acoes'] * (resultado["Dividendos"] * (1 - resultado["Pais"].map(IR_por_pais).fillna(5))), 2)
    Final = Final.sort_values(by="Total de Dividendo",ascending=False).reset_index(drop=True)
    
    print(Final)

compra(resultado_meu)
compra(resultado)
