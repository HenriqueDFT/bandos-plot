# bandos-plot.py 

pip install -r requirements.txt

BANDOS-PLOT
🚀 Sobre o Projeto

O BANDOS-PLOT é um programa desenvolvido em Python para a visualização e análise de estruturas de bandas eletrônicas e densidade de estados (DOS). Ele foi criado para facilitar o pós-processamento de dados obtidos de cálculos de Estrutura Eletrônica por Teoria do Funcional da Densidade (DFT), especialmente aqueles gerados por pacotes como o SIESTA.

A principal funcionalidade do BANDOS-PLOT é gerar gráficos combinados de bandas eletrônicas e DOS, com a marcação automática dos pontos de alta simetria na primeira zona de Brillouin e o ajuste ao nível de Fermi. Isso otimiza a análise e a apresentação de resultados científicos, além da auto escala dos gráficos com objetivo ja imprimir os gráficos otimizando a divulgação.
✨ Recursos Principais

    Plotagem Combinada: Geração de gráficos de Estrutura de Bandas e Densidade de Estados (DOS) lado a lado.

    Identificação de Pontos de Alta Simetria: Marcação automática e correta dos símbolos dos pontos de alta simetria (e.g., mathbfGamma, mathbfK, mathbfM, mathbfX) no eixo k.

    Nível de Fermi: Ajuste automático e marcação do nível de Fermi (E_F=0) para ambos os gráficos.

    Customização de Cores: Opções para alterar as cores das bandas e do DOS diretamente na interface.

    Seleção de Intervalo de Energia: Controle dos limites de energia (eixo Y) para focar em regiões específicas do espectro.

    Interface Gráfica Intuitiva (GUI): Desenvolvido com tkinter para uma experiência de usuário amigável.

    Exportação de Gráficos: Salva os gráficos gerados em formatos de alta qualidade (PNG, PDF).

🛠️ Tecnologias Utilizadas

    Python 3.x

    matplotlib: Para a geração dos gráficos científicos.

    tkinter: Para a construção da interface gráfica do usuário.

    Pillow (PIL Fork): Para o carregamento e redimensionamento de imagens (logos).

    re (Regular Expressions): Para a extração de dados de arquivos de entrada.

⚙️ Como Usar
Pré-requisitos

Certifique-se de ter o Python 3.x instalado em seu sistema. Você também precisará instalar as bibliotecas necessárias:

pip install matplotlib pillow

Executando o Programa

    Baixe ou clone este repositório:

    git clone https://github.com/seu-usuario/BANDOS-PLOT.git
    cd BANDOS-PLOT

    Certifique-se de que os arquivos de logo e QR code estão na mesma pasta do script principal:

        gnc(1).png

        ufpi.png

        qr(1)(1).png

    Execute o script principal:

    python seu_script_principal.py

    (Substitua seu_script_principal.py pelo nome do arquivo Python que contém a classe App e o if __name__ == "__main__":.)

Fluxo de Uso

    Selecione os Arquivos:

        Arquivo .bands: Contém o nível de Fermi e as coordenadas dos pontos de alta simetria.

        Arquivo bands.dat: Contém os dados de energia da estrutura de bandas.

        Arquivo dos.dat: Contém os dados de densidade de estados.

    Defina o Intervalo de Energia: Insira os valores mínimo e máximo para o eixo Y dos gráficos (opcional).

    Clique em "Gerar Gráfico": Uma nova janela será aberta exibindo os gráficos combinados.

    Personalize e Salve: Na janela do gráfico, você pode alterar as cores e salvar a imagem em diferentes formatos.

📚 Arquivos de Exemplo

Para testar o programa, você precisará de arquivos de dados no formato esperado. Exemplos típicos são gerados por cálculos DFT (como os do Quantum ESPRESSO). Os arquivos .bands, bands.dat e dos.dat devem seguir uma estrutura específica para serem lidos corretamente pelo programa.

    *.bands: A primeira linha deve conter o nível de Fermi. As linhas seguintes, após um número inteiro que indica a quantidade de pontos, devem conter as coordenadas k e os rótulos dos pontos de alta simetria.

    bands.dat: Arquivo de duas colunas (coordenada k, energia da banda).

    dos.dat: Arquivo de duas colunas (energia, densidade de estados).

📝 Atribuição e Contato

Este software foi desenvolvido por Henrique Lago, físico formado pela Universidade Federal do Piauí (UFPI), durante sua Iniciação Científica Voluntária.

Orientador: Professor Dr. Ramon Sampaio Ferreira

Instituição: Grupo de Nanofísica Computacional (GNC), Universidade Federal do Piauí (UFPI).

Entre em contato: henrique.liberato@ufpi.edu.br
🔗 Conheça o GNC

Escaneie o QR Code abaixo para saber mais sobre o Grupo de Nanofísica Computacional:
⚖️ Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
🤝 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões, relatar bugs ou quiser adicionar novos recursos, por favor, abra uma issue ou envie um pull request.
