import os
import pdfkit
import pypdf
from caminhos import PASTA_DADOS, PASTA_ASSETS, PASTA_OUTPUT
from formatacao_de_dados import pegar_template_renderizado

# Configurações do relatório
CONFIG = {
    'mes_referencia': '2023-02',
    'pasta_dados': PASTA_DADOS,
    'arquivo_excel': 'dados.xlsx',
    'pasta_assets': PASTA_ASSETS,
    'arquivo_template': 'template.jinja',
    'arquivo_css': 'style.css',
    'pasta_output': PASTA_OUTPUT,
    'arquivo_layout': 'layout_relatorio.pdf'
}

def main(mes_referencia, pasta_dados, arquivo_excel, pasta_assets, arquivo_template, arquivo_css, pasta_output, arquivo_layout) -> None:
    """
    Função principal para gerar o relatório PDF.

    Args:
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        pasta_dados (Path): Caminho para o diretório de dados.
        arquivo_excel (str): Nome do arquivo Excel.
        pasta_assets (Path): Caminho para o diretório de assets.
        arquivo_template (str): Nome do arquivo de template.
        arquivo_css (str): Nome do arquivo CSS.
        pasta_output (Path): Caminho para o diretório de output.
        arquivo_layout (str): Nome do arquivo de layout do relatório.
    """
    print('Iniciando geração de relatório...')
    pasta_output.mkdir(exist_ok=True, parents=True)

    # Renderiza o template HTML com os dados
    string_html = pegar_template_renderizado(
        mes_referencia=mes_referencia,
        pasta_dados=pasta_dados,
        arquivo_excel=arquivo_excel,
        pasta_assets=pasta_assets,
        arquivo_template=arquivo_template,
        arquivo_css=arquivo_css,
    )
    # Gera o relatório PDF a partir do HTML renderizado
    caminho_relatorio = gerar_relatorio(
        string_html=string_html,
        mes_referencia=mes_referencia,
        pasta_output=pasta_output,
    )

    # Adiciona o layout ao relatório PDF
    caminho_layout = pasta_assets / arquivo_layout
    adicionar_layout_a_relatorio(caminho_relatorio=caminho_relatorio, caminho_layout=caminho_layout)
    print(f'Relatório gerado no caminho: {caminho_relatorio}')

def gerar_relatorio(string_html, mes_referencia, pasta_output):
    """
    Gera o relatório PDF a partir do HTML renderizado.

    Args:
        string_html (str): HTML renderizado.
        mes_referencia (str): Mês de referência no formato 'YYYY-MM'.
        pasta_output (Path): Caminho para o diretório de output.

    Returns:
        Path: Caminho do relatório PDF gerado.
    """
    nome_relatorio = f'Relatório Mensal - {mes_referencia}.pdf'
    caminho_relatorio = pasta_output / nome_relatorio
    if os.name == 'nt':  # Em Windows, é preciso passar o caminho
        caminho_exec = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=caminho_exec)
        pdfkit.from_string(
            string_html,
            output_path=str(caminho_relatorio),
            configuration=config,
        )
    else:
        pdfkit.from_string(string_html, output_path=str(caminho_relatorio))
    return caminho_relatorio

def adicionar_layout_a_relatorio(caminho_relatorio, caminho_layout):
    """
    Adiciona o layout ao relatório PDF.

    Args:
        caminho_relatorio (Path): Caminho do relatório PDF gerado.
        caminho_layout (Path): Caminho do arquivo de layout do relatório.
    """
    layout_pdf = pypdf.PdfReader(caminho_layout).pages[0]
    pdf = pypdf.PdfWriter(clone_from=caminho_relatorio)
    pdf.pages[0].merge_page(layout_pdf, over=True)
    pdf.write(caminho_relatorio)

if __name__ == '__main__':
    main(**CONFIG)
