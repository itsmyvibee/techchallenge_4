# Importar bibliotecas
import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

@st.cache_data
def predict_engine(data):
    # Coleta informação direto do IPEA
    url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"

    from io import BytesIO

    # Ler tabela pelo html
    tables = pd.read_html(url)[2][1:]

    df_origin = tables.rename(columns={tables.columns[0]: 'data', tables.columns[1]: 'preco'})

    # Criar um buffer em memória para simular o arquivo Excel (Por algum motivo trazer diretamente para pandas não está funcionando as conversões)
    excel_buffer = BytesIO()

    # Salvar o DataFrame no buffer como arquivo Excel
    df_origin.to_excel(excel_buffer, index=False, engine='openpyxl')

    # Retornar ao início do buffer
    excel_buffer.seek(0)

    # Agora, você pode usar esse buffer como se fosse um arquivo Excel
    # Por exemplo, carregá-lo de volta para outro DataFrame
    df = pd.read_excel(excel_buffer, parse_dates=['data'])
    df['preco'] = df['preco']/100
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')

    # Ordenação de datas
    df_sorted = df.sort_values(by='data', ascending=True)
    df_sorted = df_sorted.reset_index(drop=True)

    df_test = df_sorted

    #Renomear colunas para ds (DataSeries) e y (Valor para predict)
    df_test = df_test.rename(columns={'data': 'ds', 'preco': 'y'})

    df_test.head()

    model = Prophet()
    model.fit(df_test)

    # Verifica data que será utilizada para previsão e gera a lista de todos os dias até a data alvo
    data_futura = data
    periodos_futuros = (pd.to_datetime(data_futura) - df_test['ds'].max()).days

    # DFs
    future = model.make_future_dataframe(periods=periodos_futuros)
    forecast = model.predict(future)

    # Visualização
    fig1 = model.plot(forecast)
    #fig2 = model.plot_components(forecast)
    plt.show()

    # Previsão
    forecast_alvo = forecast[forecast['ds'] == data_futura]
    if not forecast_alvo.empty:
        preco_predict = forecast_alvo['yhat'].values[0]
        return f"Preço previsto para a data ({data_futura}): US$ {preco_predict:.2f}", model, forecast
    else:
        return f"Data incorreta", model, forecast


# ------------------------------------------------------
# StreamLit

# Criar abas
tab1, tab2, tab3, tab4 = st.tabs(["Eventos de impacto", "Predictor", "Fontes", "Code"])

# Conteúdo da aba 1
with tab1:
    st.header("Eventos de impacto")

    #PRIMAVERA ARABE
    st.write("""
    ### Primavera Árabe
    2010 e 2011
    \nA Primavera Árabe foi uma série de protestos, revoluções e movimentos populares que ocorreram no Oriente Médio e no Norte da África a partir de dezembro de 2010. Esses eventos impactaram significativamente o mercado de petróleo devido à instabilidade política na região, que é um dos maiores produtores de petróleo do mundo.
    \nInstabilidades políticas afetam diretamente a produção e o fornecimento de petróleo, causando volatilidade nos preços globais. 
    \nEm 2011, o preço do barril de petróleo Brent ultrapassou US$ 120, refletindo o aumento das tensões e a incerteza sobre a produção futura.
    """)

    st.image("https://i.ibb.co/gj9LRkV/primavera.png", caption="Período da Primavera Árabe", use_container_width =True)

    st.write("""
     Países consumidores diversificaram suas fontes de energia para reduzir a dependência do petróleo da região. Essa é uma forma de se proteger de possíveis flutuações vindas de instabilidades políticas""")

    # Kuwait
    st.write("""
        ### A invasão do Kuwait pelo Iraque
        1990
        \nA invasão do Kuwait pelo Iraque em 1990 foi um evento marcante na geopolítica do Oriente Médio e teve impactos significativos no mercado global de petróleo.
        \nEm 2 de agosto de 1990, o Iraque, liderado por Saddam Hussein, invadiu o Kuwait, alegando disputas territoriais e acusações de que o Kuwait estava extraindo petróleo de campos iraquianos além de manipular os preços globais ao aumentar sua produção.
        \nO Kuwait, um pequeno país no Golfo Pérsico, era um dos maiores produtores de petróleo do mundo e possuía cerca de 10% das reservas globais de petróleo.
        \nA invasão do Kuwait e o subsequente embargo ao Iraque e ao Kuwait retiraram do mercado cerca de 4,3 milhões de barris por dia (mais de 6% da oferta global).
        \nO preço do barril de petróleo dobrou em poucos meses, subindo de cerca de 20 doláres para mais de 40 doláres.
        """)

    st.image("https://i.ibb.co/7WF1CFT/kuwait.png", caption="A invasão do Kuwait pelo Iraque", use_container_width=True)

    st.write("""
         Muitos países consumidores, especialmente os EUA, intensificaram seus esforços para reduzir a dependência do petróleo do Oriente Médio.\n
    Isso incluiu investimentos em fontes alternativas de energia e o desenvolvimento de campos de petróleo em outras regiões, como o Mar do Norte e o Alasca.""")

    # Crise asiativa
    st.write("""
            ### Crise Econômica Asiatica
            1997
            \nA crise financeira asiática de 1997 foi um evento econômico marcante que teve repercussões significativas em diversas economias emergentes e também impactou o mercado global de petróleo, ainda que de forma indireta.
            \nA crise começou na Tailândia e rapidamente se espalhou por outros países da Ásia, incluindo Indonésia, Coreia do Sul, Malásia, Filipinas, e Hong Kong.
            \nA crise foi desencadeada pela desvalorização da moeda tailandesa (baht) em julho de 1997, após pressões especulativas e problemas com dívidas externas excessivas.
            \nRapidamente, outras economias asiáticas enfrentaram desvalorizações cambiais, recessões e colapsos em seus mercados financeiros.
            \nA Ásia estava em uma fase de rápido crescimento econômico, sendo uma das principais regiões de expansão da demanda global por petróleo e o impacto econômico causou uma queda significativa na demanda de produto na região.
            
            \n\nEm 1998, o preço do barril de petróleo Brent caiu para cerca de US$ 10, o menor nível em mais de uma década.
            
            """)

    st.image("https://i.ibb.co/jhLqHKC/asia.png", caption="Crise Econômica Asiatica", use_container_width=True)

    st.write("""
             Com a recuperação gradual das economias asiáticas no final dos anos 1990, a demanda por petróleo voltou a crescer, e os preços começaram a se estabilizar.""")

    # COVID19
    st.write("""
            ### COVID-19
            2020
            \nA pandemia de COVID-19, que começou em dezembro de 2019, trouxe impactos drásticos ao mercado global de petróleo. Com a desaceleração econômica mundial, interrupções no transporte e mudanças significativas nos padrões de consumo, o setor de energia enfrentou uma das maiores crises de sua história.
            \nCom lockdowns globais, restrições de viagens e desaceleração na atividade econômica, a demanda global por petróleo caiu drasticamente.
            \nNo auge da crise, em abril de 2020, a demanda global caiu cerca de 30% em relação ao normal, reduzindo o consumo diário de petróleo em cerca de 30 milhões de barris.
            \nEm abril de 2020, os preços do WTI (West Texas Intermediate), referência nos EUA, ficaram negativos pela primeira vez na história, atingindo -US$ 37,63 por barril.
            \nIsso ocorreu porque a capacidade de armazenamento nos EUA estava próxima do limite, e os vendedores precisavam pagar para que alguém retirasse o petróleo.
            \n\nO Brent, referência global, caiu abaixo de US$ 20 por barril, níveis não vistos em décadas.

            """)

    st.image("https://i.ibb.co/YpkwySS/covid.png", caption="COVID-19", use_container_width=True)

    st.write("""
             A pandemia destacou a vulnerabilidade do mercado de petróleo a crises globais, incentivando muitos governos a acelerar investimentos em energias renováveis.
            \nEmpresas de petróleo diversificaram suas operações, com várias major oils (como BP, Shell e Total) anunciando planos para investir em energia limpa.
            \nMuitos países reforçaram suas reservas estratégicas de petróleo para mitigar riscos futuros de choques na oferta.""")

# Conteúdo da aba 2
with tab2:
    st.header("Predictor")

    # Interface Streamlit
    st.write("""
        O motor preditivo utiliza o histórico de preços para gerar previsões futuras por meio do modelo Prophet.
        \nEste motor processa os dados históricos, identificando tendências de longo prazo, padrões sazonais anuais, semanais e outros componentes cíclicos que influenciam os preços.
        \nCom base no histórico, o motor fornece previsões detalhadas para datas futuras específicas, possibilitando insights valiosos para tomadas de decisão estratégica.
        """)  # Markdown

    # Criar um campo de entrada para selecionar uma data
    data = st.date_input("Escolha uma data futura para previsão:")
    data = data.strftime('%Y-%m-%d')

    # Botão para executar a função e exibir gráficos
    if st.button("Realizar previsão"):
        resultado, model, forecast = predict_engine(data)
        st.success(f"{resultado}")

        st.pyplot(plt)

        st.pyplot(model.plot_components(forecast))

        st.write(
        """Trend (Tendência):\n Mostra o comportamento geral da série ao longo do tempo (ex.: crescimento ou queda a longo prazo).   
        \n\nWeekly (Sazonalidade Semanal):\n Indica como a série varia ao longo de uma semana (ex.: aumento nos fins de semana, queda nos domingos).
        \n\nYearly (Sazonalidade Anual):\n Mostra padrões que se repetem ao longo de um ano (ex.: alta no verão, queda no inverno).""")


# Conteúdo da aba 3
with tab3:
    st.header("Fontes")
    st.write("""https://educareforma.com.br/guerra-do-golfo-datas-causas-combatentes
             \nhttps://www.bbc.com/portuguese/articles/clje1p1p63wo
             \nhttps://g1.globo.com/economia/noticia/2024/10/02/guerra-no-oriente-medio-entenda-o-papel-e-o-tamanho-do-ira-na-producao-de-petroleo-no-mundo.ghtml
             \nhttps://brasilescola.uol.com.br/geografia/primavera-Arabe.htm
             \nhttps://www.brasildefato.com.br/2021/02/24/da-euforia-a-realidade-os-descaminhos-da-primavera-arabe-dez-anos-depois
             \nhttps://brasilescola.uol.com.br/guerras/guerra-golfo.htm
             \nhttps://pt.wikipedia.org/wiki/Crise_financeira_asi%C3%A1tica_de_1997
             \nhttps://iwofr.org/crise-financeira-asi%C3%A1tica/
             \nhttps://www.ibp.org.br/observatorio-do-setor/analises/covid-19-e-os-impactos-sobre-o-mercado-de-petroleo/
             \nhttps://www.worldbank.org/pt/news/press-release/2020/10/22/impact-of-covid-19-on-commodity-markets-heaviest-on-energy-prices-lower-oil-demand-likely-to-persist-beyond-2021
             \nhttps://g1.globo.com/mundo/noticia/2020/08/02/o-que-mudou-no-kuwait-30-anos-depois-da-invasao-do-iraque-por-saddam-hussein.ghtml
             \nhttps://www.bbc.com/portuguese/noticias/2015/12/151203_conflitos_mundiais_petroleo_lgb_gch
             \nhttps://sumario-periodicos.espm.br/xxi/article/view/90
             \nhttps://pt.wikipedia.org/wiki/Invas%C3%A3o_do_Kuwait
             \nhttps://pt.wikipedia.org/wiki/Derramamento_de_petr%C3%B3leo_durante_a_Guerra_do_Golfo
             \nhttps://www.redalyc.org/journal/4517/451755941004/451755941004.pdf
             
             \n\nhttps://facebook.github.io/prophet/docs/quick_start.html
             
             \n            
             """)

with tab4:
    st.header("Code")

    code = """
    # Coleta informação direto do IPEA
    url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"

    from io import BytesIO

    # Ler tabela pelo html
    tables = pd.read_html(url)[2][1:]

    df_origin = tables.rename(columns={tables.columns[0]: 'data', tables.columns[1]: 'preco'})

    # Criar um buffer em memória para simular o arquivo Excel (Por algum motivo trazer diretamente para pandas não está funcionando as conversões)
    excel_buffer = BytesIO()

    # Salvar o DataFrame no buffer como arquivo Excel
    df_origin.to_excel(excel_buffer, index=False, engine='openpyxl')

    # Retornar ao início do buffer
    excel_buffer.seek(0)

    # Agora, você pode usar esse buffer como se fosse um arquivo Excel
    # Por exemplo, carregá-lo de volta para outro DataFrame
    df = pd.read_excel(excel_buffer, parse_dates=['data'])
    df['preco'] = df['preco']/100
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')

    # Ordenação de datas
    df_sorted = df.sort_values(by='data', ascending=True)
    df_sorted = df_sorted.reset_index(drop=True)

    df_test = df_sorted

    #Renomear colunas para ds (DataSeries) e y (Valor para predict)
    df_test = df_test.rename(columns={'data': 'ds', 'preco': 'y'})

    df_test.head()

    model = Prophet()
    model.fit(df_test)

    # Verifica data que será utilizada para previsão e gera a lista de todos os dias até a data alvo
    data_futura = data
    periodos_futuros = (pd.to_datetime(data_futura) - df_test['ds'].max()).days

    # DFs
    future = model.make_future_dataframe(periods=periodos_futuros)
    forecast = model.predict(future)

    # Visualização
    fig1 = model.plot(forecast)
    #fig2 = model.plot_components(forecast)
    plt.show()

    # Previsão
    forecast_alvo = forecast[forecast['ds'] == data_futura]
    if not forecast_alvo.empty:
        preco_predict = forecast_alvo['yhat'].values[0]
        return f"Preço previsto para a data ({data_futura}): US$ {preco_predict:.2f}", model, forecast
    else:
        return f"Data incorreta", model, forecast
    """

    st.code(code, language='python')




