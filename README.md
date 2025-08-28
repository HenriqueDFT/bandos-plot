# BANDOS-PLOT

---

## 🚀 Sobre o Projeto

O **BANDOS-PLOT** é um programa em Python para a visualização e análise de estruturas de bandas eletrônicas e densidade de estados (DOS). Ele foi desenvolvido para simplificar o pós-processamento de dados de cálculos de Estrutura Eletrônica por Teoria do Funcional da Densidade (DFT), especialmente os gerados por pacotes como o **SIESTA**.

A principal função do BANDOS-PLOT é gerar gráficos combinados de bandas e DOS, com:
* Marcação automática dos pontos de alta simetria na primeira zona de Brillouin;
* Ajuste automático ao nível de Fermi;
* Autoescala dos gráficos para facilitar a impressão e divulgação científica.

---

## ✨ Recursos Principais

* **Plotagem Combinada**: Bandas eletrônicas e DOS no mesmo gráfico.
* **Identificação de Pontos de Alta Simetria**: Rótulos automáticos (ex: `Γ`, `K`, `M`, `X`) no eixo k.
* **Nível de Fermi**: Ajuste e marcação de \( E_F = 0 \).
* **Customização de Cores**: Altere as cores dos gráficos diretamente pela interface.
* **Seleção de Intervalo de Energia**: Defina os limites do eixo Y para focar em uma região específica.
* **Interface Gráfica (GUI)**: Intuitiva e desenvolvida com `tkinter`.
* **Exportação de Gráficos**: Salve os gráficos em PNG ou PDF com alta qualidade.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* [`matplotlib`](https://matplotlib.org/) — Para a geração de gráficos
* [`Pillow`](https://python-pillow.org/) — Para o tratamento de imagens (logos)
* [`re`](https://docs.python.org/3/library/re.html) — Para a extração de dados
* [`tkinter`](https://docs.python.org/3/library/tkinter.html) — Para a interface gráfica

---

## 📥 Instalação e Uso

Para começar, siga estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```
    *(**Nota**: Recomenda-se usar o comando `git clone` em vez de baixar o arquivo `.zip` para facilitar futuras atualizações.)*

2.  **Instale as dependências:**
    A forma mais simples e recomendada é usar um ambiente virtual para isolar as dependências do projeto.
    - Crie e ative um ambiente virtual:
      ```bash
      python -m venv venv
      # No Windows:
      venv\Scripts\activate
      # No macOS/Linux:
      source venv/bin/activate
      ```
    - Instale as bibliotecas necessárias:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Execute o programa:**
    Com o ambiente ativado, execute o script principal:
    ```bash
    python3 bandos-plot.py
    ```

**Importante:** Os arquivos de logo (`gnc(1).png`, `ufpi.png`, `qr(1)(1).png`) devem estar na mesma pasta do script principal para serem carregados corretamente na interface.

---

## 🧭 Fluxo de Uso

Para um guia de execução mais detalhado, visite a [Wiki do Projeto](https://github.com/HenriqueDFT/bandos-plot/wiki/03.-Como-usar%3F).

Em resumo, na interface do programa:

* **Selecione os Arquivos:**
    * `*.bands`: Nível de Fermi e pontos de alta simetria.
    * `bands.dat`: Dados da estrutura de bandas.
    * `dos.dat`: Dados da densidade de estados.
* **Defina o Intervalo de Energia (Opcional).**
* **Clique em "Gerar Gráfico":** Uma nova janela com os gráficos será exibida.
* **Personalize e Salve:** Mude as cores e exporte os gráficos em PNG ou PDF.

---

## 📚 Estrutura dos Arquivos de Entrada

Os arquivos de dados devem seguir o formato padrão de saída dos códigos DFT (como SIESTA ou Quantum ESPRESSO):

* `*.bands`: Primeira linha com o nível de Fermi; últimas linhas com as coordenadas k e os rótulos dos pontos de alta simetria.
* `bands.dat`: Duas colunas - (coordenada k, energia).
* `dos.dat`: Duas colunas - (energia, densidade de estados).

---

## 📝 Autoria e Contato

Este software foi desenvolvido por:

**Henrique Lago**
Bacharel em Física pela Universidade Federal do Piauí (UFPI).
Projeto de Iniciação Científica Voluntária sob orientação do **Prof. Dr. Ramon Sampaio Ferreira** no Grupo de Nanofísica Computacional (GNC) - UFPI.

### 📧 Email: henrique.liberato@ufpi.edu.br

---

## 🔗 Conheça o GNC

Escaneie o QR Code incluído na interface do programa para saber mais sobre o Grupo de Nanofísica Computacional.

---

## ⚖️ Licença

Distribuído sob a [Licença MIT](https://github.com/HenriqueDFT/bandos-plot/blob/main/LICENSE).
Veja o arquivo `LICENSE` para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para sugerir melhorias, relatar bugs ou adicionar novos recursos, por favor, abra uma [issue](https://github.com/HenriqueDFT/bandos-plot/issues) ou envie um [pull request](https://github.com/HenriqueDFT/bandos-plot/pulls).