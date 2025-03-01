# Projeto de Automação: Gerador de Relatórios PDF via Excel

Este projeto gera relatórios mensais em formato PDF a partir de dados em um arquivo Excel. Utiliza templates HTML e CSS para formatar o relatório e a biblioteca `pdfkit` para converter HTML em PDF.

## Estrutura do Projeto

- `assets/`: Contém arquivos de layout, estilo e templates.
- `dados/`: Contém o arquivo Excel com os dados.
- `output/`: Diretório onde os relatórios gerados serão salvos.
- `caminhos.py`: Define os caminhos para os diretórios e arquivos.
- `formatacao_de_dados.py`: Formata os dados e renderiza o template.
- `processamento_de_dados.py`: Processa os dados do Excel.
- `main.py`: Gera o relatório PDF.

## Requisitos

- Python 3.x
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/projeto_automacao_gerador_relatórios_pdf_via_excel.git
    cd projeto_automacao_gerador_relatórios_pdf_via_excel
    ```

2. Crie um ambiente virtual e instale as dependências:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Uso

1. Coloque seus dados no arquivo [`dados/dados.xlsx`](dados/dados.xlsx ).
2. Execute o script [`gerar_relatorio.py`](gerar_relatorio.py ):
    ```sh
    python gerar_relatorio.py
    ```
3. O relatório gerado será salvo no diretório `output/`.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.