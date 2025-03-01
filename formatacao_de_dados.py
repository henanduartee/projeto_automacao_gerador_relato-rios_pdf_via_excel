import locale
from datetime import datetime

from jinja2 import FileSystemLoader, Environment

from processamento_de_dados import carregar_tabelas


def pegar_template_renderizado(
        mes_referencia,
        pasta_dados,
        arquivo_excel,
        pasta_assets,
        arquivo_template,
        arquivo_css,
):
    """
    Renderiza o template HTML com os dados processados.

    Args:
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        pasta_dados (Path): Caminho para o diretório de dados.
        arquivo_excel (str): Nome do arquivo Excel.
        pasta_assets (Path): Caminho para o diretório de assets.
        arquivo_template (str): Nome do arquivo de template.
        arquivo_css (str): Nome do arquivo CSS.

    Returns:
        str: HTML renderizado.
    """
    dict_tabelas = carregar_tabelas(
        mes_referencia=mes_referencia,
        pasta_dados=pasta_dados,
        arquivo_excel=arquivo_excel,
    )
    for nome_tabela, tabela in dict_tabelas.items():
        dict_tabelas[nome_tabela] = tabela.to_html(classes='dataframe', float_format=formatar)

    template = carregar_template(pasta_assets=pasta_assets, arquivo_template=arquivo_template)

    caminho_css = pasta_assets / arquivo_css
    css = carregar_css(caminho_css=caminho_css)

    return renderizar_template_como_html(
        template=template,
        css=css,
        mes_referencia=mes_referencia,
        dict_tabelas=dict_tabelas,
    )


def formatar(valor):
    """
    Formata o valor como moeda brasileira.

    Args:
        valor (float): Valor a ser formatado.

    Returns:
        str: Valor formatado como moeda brasileira.
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Em windows: 'portuguese-brazilian'
    return locale.currency(valor, grouping=True, symbol=True)


def carregar_template(pasta_assets, arquivo_template):
    """
    Carrega o template Jinja2.

    Args:
        pasta_assets (Path): Caminho para o diretório de assets.
        arquivo_template (str): Nome do arquivo de template.

    Returns:
        Template: Template Jinja2 carregado.
    """
    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)
    return template


def carregar_css(caminho_css):
    """
    Carrega o conteúdo do arquivo CSS.

    Args:
        caminho_css (Path): Caminho do arquivo CSS.

    Returns:
        str: Conteúdo do arquivo CSS.
    """
    with open(caminho_css) as arquivo:
        css = arquivo.read()
    return css


def renderizar_template_como_html(
        template,
        css,
        mes_referencia,
        dict_tabelas,
):
    """
    Renderiza o template com as variáveis fornecidas.

    Args:
        template (Template): Template Jinja2.
        css (str): Conteúdo do arquivo CSS.
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        dict_tabelas (dict): Dicionário contendo as tabelas de dados.

    Returns:
        str: HTML renderizado.
    """
    agora = datetime.now()
    dia = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M')
    template_vars = {
        'stylesheet': css,
        'mes_referencia': mes_referencia,
        'dia': dia,
        'hora': hora,
    }
    string_html = template.render(**template_vars, **dict_tabelas)
    return string_html


if __name__ == '__main__':  # Testando o código
    from caminhos import PASTA_DADOS, PASTA_ASSETS
    html = pegar_template_renderizado(
        mes_referencia='2023-01',
        pasta_dados=PASTA_DADOS,
        arquivo_excel='dados.xlsx',
        pasta_assets=PASTA_ASSETS,
        arquivo_template='template.jinja',
        arquivo_css='style.css',
    )
    print(html)
    # Conferir o resultado das linhas abaixo abrindo o arquivo em um navegador
    with open('relatorio.html', 'w') as html_file:
        html_file.write(html)
