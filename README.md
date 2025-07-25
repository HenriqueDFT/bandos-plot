# BANDOS-PLOT

## 🚀 Sobre o Projeto

O **BANDOS-PLOT** é um programa desenvolvido em Python para a visualização e análise de estruturas de bandas eletrônicas e densidade de estados (DOS).  
Ele foi criado para facilitar o pós-processamento de dados obtidos de cálculos de Estrutura Eletrônica por Teoria do Funcional da Densidade (DFT), especialmente aqueles gerados por pacotes como o **SIESTA**.

A principal funcionalidade do BANDOS-PLOT é gerar gráficos combinados de bandas eletrônicas e DOS, com:
- Marcação automática dos pontos de alta simetria na primeira zona de Brillouin;
- Ajuste ao nível de Fermi;
- Autoescala dos gráficos para facilitar a impressão e divulgação científica.

---

## ✨ Recursos Principais

- **Plotagem Combinada**: Bandas eletrônicas e DOS lado a lado.
- **Identificação de Pontos de Alta Simetria**: Marcação automática dos símbolos (e.g., `Γ`, `K`, `M`, `X`) no eixo k.
- **Nível de Fermi**: Ajuste e marcação automática de \( E_F = 0 \).
- **Customização de Cores**: Cores personalizáveis diretamente na interface.
- **Seleção de Intervalo de Energia**: Defina os limites do eixo Y para foco em regiões específicas.
- **Interface Gráfica Intuitiva (GUI)**: Desenvolvido com `tkinter`.
- **Exportação de Gráficos**: Salva em PNG e PDF com alta qualidade.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- [`matplotlib`](https://matplotlib.org/) — geração de gráficos científicos
- [`tkinter`](https://docs.python.org/3/library/tkinter.html) — construção da interface gráfica
- [`Pillow`](https://python-pillow.org/) — carregamento e redimensionamento de imagens
- [`re`](https://docs.python.org/3/library/re.html) — extração de dados com expressões regulares

---

## ⚙️ Como Usar

### ✅ Pré-requisitos

Certifique-se de ter o Python 3.x instalado.  
Instale as dependências necessárias com o comando:


pip install -r requirements.txt

Ou, manualmente:

pip install matplotlib pillow

## ▶️ Executando o Programa

    Baixe ou clone este repositório:

git clone https://github.com/HenriqueDFT/BANDOS-PLOT.git
cd BANDOS-PLOT

    Certifique-se de que os arquivos de logo e QR code estejam na mesma pasta do script principal:

gnc(1).png
ufpi.png
qr(1)(1).png

    Execute o script principal:

bandos-plot.py

    Substitua bandos-plot.py pelo nome do arquivo que contém a classe App e o trecho if __name__ == "__main__".

# 🧭 Fluxo de Uso

    Selecione os Arquivos:

        *.bands → contém o nível de Fermi e os pontos de alta simetria

        bands.dat → contém os dados da estrutura de bandas

        dos.dat → contém os dados da densidade de estados

    Defina o Intervalo de Energia (opcional)

    Clique em "Gerar Gráfico":
    Uma nova janela abrirá com os gráficos combinados.

    Personalize e Salve:
    Altere as cores, exporte em PNG ou PDF conforme necessário.

#  📚 Arquivos de Exemplo

Os arquivos devem seguir a estrutura padrão de saída dos códigos DFT (como SIESTA ou Quantum ESPRESSO):

    *.bands:

        Primeira linha: nível de Fermi (float)

        Últimas  linhas: coordenadas k e os rótulos dos pontos de alta simetria

    bands.dat:
    Arquivo de duas colunas → (coordenada k, energia)

    dos.dat:
    Arquivo de duas colunas → (energia, densidade de estados)

# 📝 Atribuição e Contato

Este software foi desenvolvido por:

Henrique Lago
Bacharel em Física pela Universidade Federal do Piauí (UFPI)
Durante sua Iniciação Científica Voluntária.

Orientador: Prof. Dr. Ramon Sampaio Ferreira
Instituição: Grupo de Nanofísica Computacional (GNC) – UFPI
### 📧 Email: henrique.liberato@ufpi.edu.br
## 🔗 Conheça o GNC

Escaneie o QR Code incluído na interface do programa para saber mais sobre o Grupo de Nanofísica Computacional.





# ⚖️ Licença

Distribuído sob a licença MIT.
Veja o arquivo LICENSE para mais informações.


---


## 🤝 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões, relatar bugs ou quiser adicionar novos recursos, por favor, abra uma issue ou envie um pull request.

```bash
