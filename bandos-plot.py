import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
import os

# --- Configuração Global da Fonte para Matplotlib (Times New Roman) ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif', 'serif']
plt.rcParams['font.weight'] = 'normal' # Definido como normal para não forçar todo o texto
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 18

# Configurações para texto matemático (para o Gamma em negrito)
plt.rcParams['mathtext.fontset'] = 'cm' # Usa Computer Modern para texto matemático (padrão LaTeX)

class PlotWindow(tk.Toplevel):
    def __init__(self, master, fig, ax_bands, ax_dos, bands_data, dos_energies, dos_densities, k_points_high_symmetry_values, k_points_high_symmetry_labels, fermi_level, y_limits):
        super().__init__(master)
        self.master = master # Referência ao objeto App
        self.title("Gráfico de Estrutura de Bandas e DOS")
        self.geometry("1200x800")
        self.configure(bg="#F0F0F0") # Cor de fundo da janela

        self.fig = fig
        self.ax_bands = ax_bands
        self.ax_dos = ax_dos
        self.bands_data = bands_data
        self.dos_energies = dos_energies
        self.dos_densities = dos_densities
        self.k_points_high_symmetry_values = k_points_high_symmetry_values
        self.k_points_high_symmetry_labels = k_points_high_symmetry_labels # Armazena os rótulos
        self.fermi_level = fermi_level
        self.y_limits = y_limits # Armazena os limites Y definidos

        # Cores padrão para os gráficos
        self.bands_current_color = '#8A2BE2' # Roxo Azulado para Bandas
        self.dos_current_color = '#DA70D6'   # Orquídea para DOS

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Frame para controles de cor e salvar ---
        control_frame = tk.Frame(self, bg="#E0E0E0", bd=2, relief=tk.RAISED)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

        # Botão Salvar Gráfico
        tk.Button(control_frame, text="Salvar Gráfico", command=self.save_plot, font=("Times New Roman", 12, "bold"), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=15, pady=5)

        # Opção de cor para o gráfico de Bandas
        bands_color_frame = tk.LabelFrame(control_frame, text="Cor das Bandas", font=("Times New Roman", 10, "bold"), bg="#E0E0E0")
        bands_color_frame.pack(side=tk.LEFT, padx=10, pady=5)
        self.bands_color_button = tk.Button(bands_color_frame, text="Escolher", command=self.choose_bands_color, font=("Times New Roman", 9))
        self.bands_color_button.pack(side=tk.LEFT, padx=5)
        self.bands_color_display = tk.Label(bands_color_frame, text="", bg=self.bands_current_color, width=3, relief=tk.SUNKEN, bd=1)
        self.bands_color_display.pack(side=tk.LEFT, padx=5)

        # Opção de cor para o gráfico de DOS
        dos_color_frame = tk.LabelFrame(control_frame, text="Cor do DOS", font=("Times New Roman", 10, "bold"), bg="#E0E0E0")
        dos_color_frame.pack(side=tk.LEFT, padx=10, pady=5)
        self.dos_color_button = tk.Button(dos_color_frame, text="Escolher", command=self.choose_dos_color, font=("Times New Roman", 9))
        self.dos_color_button.pack(side=tk.LEFT, padx=5)
        self.dos_color_display = tk.Label(dos_color_frame, text="", bg=self.dos_current_color, width=3, relief=tk.SUNKEN, bd=1)
        self.dos_color_display.pack(side=tk.LEFT, padx=5)

        # Atualiza a exibição das cores iniciais
        self.update_color_display(self.bands_color_display, self.bands_current_color)
        self.update_color_display(self.dos_color_display, self.dos_current_color)

    def update_color_display(self, label_widget, color_hex):
        """Atualiza a cor do label para refletir a cor escolhida."""
        label_widget.config(bg=color_hex)

    def choose_bands_color(self):
        color_code = colorchooser.askcolor(title="Escolha a Cor das Bandas")[1]
        if color_code:
            self.bands_current_color = color_code
            self.update_color_display(self.bands_color_display, self.bands_current_color)
            self.replot_bands()

    def choose_dos_color(self):
        color_code = colorchooser.askcolor(title="Escolha a Cor do DOS")[1]
        if color_code:
            self.dos_current_color = color_code
            self.update_color_display(self.dos_color_display, self.dos_current_color)
            self.replot_dos()

    def replot_bands(self):
        """Redesenha apenas o gráfico de bandas com a nova cor."""
        self.ax_bands.clear() # Limpa o eixo de bandas
        # Passa os rótulos e valores corretos para plot_bands
        self.master.plot_bands(self.ax_bands, self.bands_data, self.k_points_high_symmetry_values, self.k_points_high_symmetry_labels, self.fermi_level, self.bands_current_color)
        # Garante que os limites Y sejam mantidos
        self.ax_bands.set_ylim(self.y_limits) # Reutiliza os limites Y armazenados
        # Removido: fig.autofmt_xdate(rotation=45, ha='right')
        self.fig.tight_layout(rect=[0, 0.05, 1, 0.96]) # Reaplicar o layout para garantir espaço
        self.canvas.draw_idle() # Redesenha o canvas eficientemente

    def replot_dos(self):
        """Redesenha apenas o gráfico de DOS com a nova cor."""
        self.ax_dos.clear() # Limpa o eixo do DOS
        self.master.plot_dos(self.ax_dos, self.dos_energies, self.dos_densities, self.dos_current_color)
        # Garante que os limites Y sejam mantidos
        self.ax_dos.set_ylim(self.y_limits) # Reutiliza os limites Y armazenados
        self.fig.tight_layout(rect=[0, 0.05, 1, 0.96]) # Reaplicar o layout para garantir espaço
        self.canvas.draw_idle() # Redesenha o canvas eficientemente

    def save_plot(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filepath:
            try:
                # Usa bbox_inches='tight' para ajustar o conteúdo à imagem salva
                self.fig.savefig(filepath, bbox_inches='tight', dpi=300)
                messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar o gráfico:\n{e}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Leitor e Plotador de Estrutura de Bandas e DOS")
        self.geometry("800x600")
        self.configure(bg="#F0F0F0") # Cor de fundo da janela principal

        self.bands_file = None
        self.bands_dat_file = None
        self.dos_dat_file = None
        self.fermi_level = None
        self.k_points_high_symmetry_values = [] # Novo atributo para os valores numéricos dos k-pontos
        self.k_points_high_symmetry_labels = [] # Novo atributo para os rótulos formatados dos k-pontos
        self.k_points_original_labels = [] # NOVO: Armazena os rótulos originais para o messagebox
        self.plot_y_limits = None # Atributo para armazenar os limites Y

        # Configurações de fonte para a interface Tkinter
        self.tk_font_default = ("Times New Roman", 10)
        self.tk_font_bold = ("Times New Roman", 10, "bold")
        self.tk_font_button = ("Times New Roman", 10)
        self.tk_font_title = ("Times New Roman", 14, "bold")

        self.setup_ui()

    def setup_ui(self):
        self.load_logos()

        file_selection_frame = tk.Frame(self, bg="#F0F0F0")
        file_selection_frame.pack(pady=70)

        tk.Button(file_selection_frame, text="Selecionar arquivo .bands", command=self.selecionar_bands, font=self.tk_font_button).grid(row=0, column=0, padx=5, pady=5)
        self.label_bands_info = tk.Label(file_selection_frame, text="Nenhum arquivo .bands selecionado", wraplength=250, font=self.tk_font_default, bg="#F0F0F0")
        self.label_bands_info.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(file_selection_frame, text="Selecionar arquivo bands.dat", command=self.selecionar_bands_dat, font=self.tk_font_button).grid(row=1, column=0, padx=5, pady=5)
        self.label_bands_dat_info = tk.Label(file_selection_frame, text="Nenhum arquivo bands.dat selecionado", wraplength=250, font=self.tk_font_default, bg="#F0F0F0")
        self.label_bands_dat_info.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(file_selection_frame, text="Selecionar arquivo dos.dat", command=self.selecionar_dos_dat, font=self.tk_font_button).grid(row=2, column=0, padx=5, pady=5)
        self.label_dos_dat_info = tk.Label(file_selection_frame, text="Nenhum arquivo dos.dat selecionado", wraplength=250, font=self.tk_font_default, bg="#F0F0F0")
        self.label_dos_dat_info.grid(row=2, column=1, padx=5, pady=5)

        energy_interval_frame = tk.LabelFrame(self, text="Intervalo de Energia (eV)", font=self.tk_font_bold, bg="#F0F0F0")
        energy_interval_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(energy_interval_frame, text="Mínimo:", font=self.tk_font_default, bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.min_energy_entry = tk.Entry(energy_interval_frame, width=10, font=self.tk_font_default)
        self.min_energy_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.min_energy_entry.insert(0, "-5")

        tk.Label(energy_interval_frame, text="Máximo:", font=self.tk_font_default, bg="#F0F0F0").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.max_energy_entry = tk.Entry(energy_interval_frame, width=10, font=self.tk_font_default)
        self.max_energy_entry.grid(row=0, column=3, padx=5, pady=2, sticky="ew")
        self.max_energy_entry.insert(0, "5")

        energy_interval_frame.grid_columnconfigure(1, weight=1)
        energy_interval_frame.grid_columnconfigure(3, weight=1)

        tk.Button(self, text="Gerar Gráfico", command=self.gerar_grafico, font=self.tk_font_title, bg="#4CAF50", fg="white").pack(pady=20)

        tk.Button(self, text="Sobre", command=self.show_about_info, font=self.tk_font_button, bg="#D3D3D3", fg="#333").place(relx=0.02, rely=0.98, anchor=tk.SW)

    def load_logos(self):
        try:
            img1 = Image.open("gnc(1).png").resize((100, 100), Image.LANCZOS)
            self.logo1_tk = ImageTk.PhotoImage(img1)
            tk.Label(self, image=self.logo1_tk, bg="#F0F0F0").place(relx=0.5, rely=0.02, anchor=tk.N)

            img2 = Image.open("ufpi.png").resize((80, 80), Image.LANCZOS)
            self.logo2_tk = ImageTk.PhotoImage(img2)
            tk.Label(self, image=self.logo2_tk, bg="#F0F0F0").place(relx=0.98, rely=0.98, anchor=tk.SE)
        except FileNotFoundError:
            messagebox.showwarning("Logos Ausentes", "Certifique-se de que os arquivos de logo (gnc(1).png, ufpi.png) estão na mesma pasta do script.")
            placeholder_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            self.logo1_tk = ImageTk.PhotoImage(placeholder_img)
            self.logo2_tk = ImageTk.PhotoImage(placeholder_img)

    def show_about_info(self):
        about_window = tk.Toplevel(self)
        about_window.title("Sobre o Programa")
        about_window.geometry("600x600")
        about_window.configure(bg="#F0F0F0")

        about_font_text = ("Times New Roman", 10)
        about_font_email = ("Times New Roman", 10, "underline")

        text_content = """O programa "BANDOS-PLOT" foi desenvolvido em Python com o objetivo
de gerar gráficos de bandas eletrônicas e densidade de estados (DOS), já contendo os pontos de alta
simetria devidamente marcados. Essa ferramenta visa facilitar a visualização e impressão dos resultados
obtidos em cálculos de Estrutura de Bandas por Teoria do Funcional da Densidade (DFT).

Este software foi criado por Henrique Lago, físico formado pela Universidade Federal do Piauí (UFPI),
durante sua Iniciação Científica Voluntária, sob orientação do Professor Dr. Ramon Sampaio Ferreira.
O desenvolvimento ocorreu no âmbito do Grupo de Nanofísica Computacional (GNC) da UFPI.

Conheça mais sobre o grupo escaneando o QR Code abaixo:
"""
        tk.Label(about_window, text=text_content, font=about_font_text, wraplength=550, justify=tk.LEFT, bg="#F0F0F0").pack(padx=20, pady=10)

        try:
            img_qrcode = Image.open("qr(1)(1).png")
            img_qrcode = img_qrcode.resize((200, 200), Image.LANCZOS)
            self.qrcode_tk = ImageTk.PhotoImage(img_qrcode)
            tk.Label(about_window, image=self.qrcode_tk, bg="#F0F0F0").pack(pady=5)
        except FileNotFoundError:
            tk.Label(about_window, text="[Arquivo qr(1)(1).png não encontrado]", font=about_font_text, fg="red", bg="#F0F0F0").pack(pady=5)
            messagebox.showwarning("QR Code Ausente", "O arquivo 'qr(1)(1).png' não foi encontrado na pasta do script.")

        tk.Label(about_window, text="e-mail: henrique.liberato@ufpi.edu.br", font=about_font_email, bg="#F0F0F0").pack(pady=10)

    def selecionar_bands(self):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivo .bands", "*.bands")])
        if not filepath: return
        self.bands_file = filepath
        self.label_bands_info.config(text=f"Arquivo .bands selecionado:\n{os.path.basename(filepath)}") # Mostra só o nome do arquivo

        try:
            # A função extrair_fermi_e_k agora retorna os rótulos LaTeX E os originais
            self.fermi_level, self.k_points_high_symmetry_values, self.k_points_high_symmetry_labels, self.k_points_original_labels = self.extrair_fermi_e_k(filepath)

            # Para o messagebox, usamos os rótulos originais, sem formatação LaTeX
            k_labels_str = ", ".join(self.k_points_original_labels)
            messagebox.showinfo("Informação", f"Nível de Fermi: {self.fermi_level:.4f}\nPontos k de alta simetria: {self.k_points_high_symmetry_values}\nRótulos: {k_labels_str}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo .bands:\n{e}")
            self.bands_file = None
            # Resetar as variáveis para evitar uso de dados antigos em caso de erro
            self.fermi_level = None
            self.k_points_high_symmetry_values = []
            self.k_points_high_symmetry_labels = []
            self.k_points_original_labels = [] # Resetar também os originais

    def selecionar_bands_dat(self):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivo de Dados (.dat)", "*.dat")])
        if not filepath: return
        self.bands_dat_file = filepath
        self.label_bands_dat_info.config(text=f"Arquivo bands.dat selecionado:\n{os.path.basename(filepath)}") # Mostra só o nome do arquivo

    def selecionar_dos_dat(self):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivo de Dados (.dat)", "*.dat")])
        if not filepath: return
        self.dos_dat_file = filepath
        self.label_dos_dat_info.config(text=f"Arquivo dos.dat selecionado:\n{os.path.basename(filepath)}") # Mostra só o nome do arquivo

    def extrair_fermi_e_k(self, filepath):
        with open(filepath, 'r') as f:
            linhas = f.readlines()

        fermi_level = None
        if linhas: # Garante que o arquivo não está vazio
            first_line = linhas[0].strip()
            match = re.search(r"[-+]?\d*\.\d+|\d+", first_line) # Procura por qualquer número (float ou int)
            if match:
                fermi_level = float(match.group(0))
            else:
                raise ValueError("Não foi possível extrair o nível de Fermi da primeira linha. Nenhuma número encontrado.")
        else:
            raise ValueError("O arquivo .bands está vazio, não foi possível extrair o nível de Fermi.")

        num_k_points_expected = 0
        k_points_raw_data = [] # Para armazenar {value: float, label: str}

        # 1. Encontrar o número de pontos de auto-simetria (o número isolado)
        found_num_points_line_idx = -1
        for i in range(len(linhas) - 1, -1, -1):
            line = linhas[i].strip()
            if re.fullmatch(r"[-+]?\d+", line):
                try:
                    num_k_points_expected = int(line)
                    found_num_points_line_idx = i
                    break
                except ValueError:
                    continue

        if num_k_points_expected <= 0 or found_num_points_line_idx == -1:
            raise ValueError("Não foi possível determinar o número de pontos de auto-simetria ou o número é inválido (<= 0).")

        # 2. Ler as linhas que são os pontos de auto-simetria
        start_reading_idx = found_num_points_line_idx + 1
        end_reading_idx = start_reading_idx + num_k_points_expected

        if end_reading_idx > len(linhas):
            raise ValueError(f"O arquivo .bands indica {num_k_points_expected} pontos de auto-simetria, mas não há linhas suficientes após o número. Faltam {end_reading_idx - len(linhas)} linhas.")

        # NOVO: Lista para armazenar os rótulos originais
        original_labels_for_display = []

        for i in range(start_reading_idx, end_reading_idx):
            line = linhas[i].strip()
            parts = line.split(maxsplit=1)

            if len(parts) >= 2:
                try:
                    value = float(parts[0])
                    label = parts[1].strip().replace("'", "")
                    k_points_raw_data.append({'value': value, 'label': label})
                    original_labels_for_display.append(label) # Adiciona o rótulo original aqui
                except ValueError:
                    messagebox.showwarning("Erro de Leitura", f"Linha do ponto k mal formatada ignorada: '{line}'")
                    continue
            else:
                messagebox.showwarning("Erro de Leitura", f"Linha do ponto k incompleta ignorada: '{line}'")
                continue

        if len(k_points_raw_data) != num_k_points_expected:
            raise ValueError(f"O número de pontos de auto-simetria esperados ({num_k_points_expected}) não corresponde ao número de pontos lidos ({len(k_points_raw_data)}).")

        k_point_values = [p['value'] for p in k_points_raw_data]
        k_point_labels_with_symbols = self.map_k_point_symbols(k_points_raw_data)

        # RETORNA AGORA 4 VALORES: fermi_level, valores, rótulos LaTeX, rótulos originais
        return fermi_level, k_point_values, k_point_labels_with_symbols, original_labels_for_display

    def map_k_point_symbols(self, k_points_raw_data):
        """
        Mapeia os rótulos de string dos pontos k para seus símbolos LaTeX correspondentes.
        """
        symbol_map = {
            # Letras gregas comuns em LaTeX (negrito)
    'Alpha': r"$\mathbf{\Alpha}$",
    'Beta': r"$\mathbf{\Beta}$",
    'Gamma': r"$\mathbf{\Gamma}$",
    'Delta': r"$\mathbf{\Delta}$",
    'Epsilon': r"$\mathbf{\Epsilon}$",
    'Zeta': r"$\mathbf{\Zeta}$",
    'Eta': r"$\mathbf{\Eta}$",
    'Theta': r"$\mathbf{\Theta}$",
    'Iota': r"$\mathbf{\Iota}$",
    'Kappa': r"$\mathbf{\Kappa}$",
    'Lambda': r"$\mathbf{\Lambda}$",
    'Mu': r"$\mathbf{\Mu}$",
    'Nu': r"$\mathbf{\Nu}$",
    'Xi': r"$\mathbf{\Xi}$",
    'Omicron': r"$\mathbf{\Omicron}$",
    'Pi': r"$\mathbf{\Pi}$",
    'Rho': r"$\mathbf{\Rho}$",
    'Sigma': r"$\mathbf{\Sigma}$",
    'Tau': r"$\mathbf{\Tau}$",
    'Upsilon': r"$\mathbf{\Upsilon}$",
    'Phi': r"$\mathbf{\Phi}$",
    'Chi': r"$\mathbf{\Chi}$",
    'Psi': r"$\mathbf{\Psi}$",
    'Omega': r"$\mathbf{\Omega}$",

    # Letras gregas minúsculas (para nomes minúsculos)
    'alpha': r"$\mathbf{\alpha}$",
    'beta': r"$\mathbf{\beta}$",
    'gamma': r"$\mathbf{\gamma}$",
    'delta': r"$\mathbf{\delta}$",
    'epsilon': r"$\mathbf{\epsilon}$",
    'zeta': r"$\mathbf{\zeta}$",
    'eta': r"$\mathbf{\eta}$",
    'theta': r"$\mathbf{\theta}$",
    'iota': r"$\mathbf{\iota}$",
    'kappa': r"$\mathbf{\kappa}$",
    'lambda': r"$\mathbf{\lambda}$",
    'mu': r"$\mathbf{\mu}$",
    'nu': r"$\mathbf{\nu}$",
    'xi': r"$\mathbf{\xi}$",
    'omicron': r"$\mathbf{o}$",  # não existe \omicron no LaTeX
    'pi': r"$\mathbf{\pi}$",
    'rho': r"$\mathbf{\rho}$",
    'sigma': r"$\mathbf{\sigma}$",
    'tau': r"$\mathbf{\tau}$",
    'upsilon': r"$\mathbf{\upsilon}$",
    'phi': r"$\mathbf{\phi}$",
    'chi': r"$\mathbf{\chi}$",
    'psi': r"$\mathbf{\psi}$",
    'omega': r"$\mathbf{\omega}$",

    # Alfabeto latino (maiúsculas)
    'A': r"$\mathbf{A}$",
    'B': r"$\mathbf{B}$",
    'C': r"$\mathbf{C}$",
    'D': r"$\mathbf{D}$",
    'E': r"$\mathbf{E}$",
    'F': r"$\mathbf{F}$",
    'G': r"$\mathbf{G}$",
    'H': r"$\mathbf{H}$",
    'I': r"$\mathbf{I}$",
    'J': r"$\mathbf{J}$",
    'K': r"$\mathbf{K}$",
    'L': r"$\mathbf{L}$",
    'M': r"$\mathbf{M}$",
    'N': r"$\mathbf{N}$",
    'O': r"$\mathbf{O}$",
    'P': r"$\mathbf{P}$",
    'Q': r"$\mathbf{Q}$",
    'R': r"$\mathbf{R}$",
    'S': r"$\mathbf{S}$",
    'T': r"$\mathbf{T}$",
    'U': r"$\mathbf{U}$",
    'V': r"$\mathbf{V}$",
    'W': r"$\mathbf{W}$",
    'X': r"$\mathbf{X}$",
    'Y': r"$\mathbf{Y}$",
    'Z': r"$\mathbf{Z}$",

    # Alfabeto latino (minúsculas)
    'a': r"$\mathbf{a}$",
    'b': r"$\mathbf{b}$",
    'c': r"$\mathbf{c}$",
    'd': r"$\mathbf{d}$",
    'e': r"$\mathbf{e}$",
    'f': r"$\mathbf{f}$",
    'g': r"$\mathbf{g}$",
    'h': r"$\mathbf{h}$",
    'i': r"$\mathbf{i}$",
    'j': r"$\mathbf{j}$",
    'k': r"$\mathbf{k}$",
    'l': r"$\mathbf{l}$",
    'm': r"$\mathbf{m}$",
    'n': r"$\mathbf{n}$",
    'o': r"$\mathbf{o}$",
    'p': r"$\mathbf{p}$",
    'q': r"$\mathbf{q}$",
    'r': r"$\mathbf{r}$",
    's': r"$\mathbf{s}$",
    't': r"$\mathbf{t}$",
    'u': r"$\mathbf{u}$",
    'v': r"$\mathbf{v}$",
    'w': r"$\mathbf{w}$",
    'x': r"$\mathbf{x}$",
    'y': r"$\mathbf{y}$",
    'z': r"$\mathbf{z}$",
        }

        mapped_labels = []
        for point_data in k_points_raw_data:
            original_label = point_data['label']
            # Usa .get() para retornar o original se não encontrar no mapa
            mapped_label = symbol_map.get(original_label, original_label)

            # Para rótulos que não são símbolos gregos conhecidos no mapa,
            # mas são uma única letra, formatamos como LaTeX em negrito.
            if original_label not in symbol_map and len(original_label) == 1 and original_label.isalpha():
                mapped_label = r"$\mathbf{" + original_label.upper() + "}$"

            mapped_labels.append(mapped_label)

        return mapped_labels

    def ler_bands_dat(self, filepath):
        bands_data, current_band = [], []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Considera linhas vazias, comentários ou linhas que começam com 'k' ou '-' como separadores
                if not line or line.startswith(('#', '-', 'k', 'K')):
                    if current_band:
                        bands_data.append(current_band)
                    current_band = []
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        current_band.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        continue
            if current_band: # Adiciona a última banda se houver dados
                bands_data.append(current_band)
        return bands_data

    def ler_dos_dat(self, filepath, fermi_level):
        energies, densities = [], []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        energies.append(float(parts[0]) - fermi_level) # Subtrai o nível de Fermi
                        densities.append(float(parts[1]))
                    except ValueError:
                        continue
        return energies, densities

    def gerar_grafico(self):
        # Validação dos arquivos
        if not all([self.bands_file, self.bands_dat_file, self.dos_dat_file, self.fermi_level is not None, self.k_points_high_symmetry_values]):
            messagebox.showwarning("Arquivos Ausentes", "Por favor, selecione todos os arquivos necessários (.bands, bands.dat, dos.dat) antes de gerar o gráfico.")
            return

        try:
            bands_data = self.ler_bands_dat(self.bands_dat_file)
            dos_energies, dos_densities = self.ler_dos_dat(self.dos_dat_file, self.fermi_level)

            if not bands_data:
                messagebox.showwarning("Dados Incompletos", "O arquivo bands.dat não contém dados válidos para plotar.")
                return
            if not dos_energies or not dos_densities:
                messagebox.showwarning("Dados Incompletos", "O arquivo dos.dat não contém dados válidos para plotar.")
                return

            min_energy, max_energy = self.get_energy_range()
            if min_energy is not None and max_energy is not None and min_energy >= max_energy:
                messagebox.showwarning("Intervalo Inválido", "O valor mínimo de energia deve ser menor que o valor máximo.")
                return

            # Cria a figura e os eixos
            # Aumentar um pouco a largura da figura pode ajudar a evitar sobreposição sem inclinar.
            fig, (ax_bands, ax_dos) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [3, 1]}, sharey=True)
            fig.suptitle("Estrutura de Bandas e Densidade de Estados (DOS)", fontsize=18, fontweight='bold')

            # Define a cor inicial para os gráficos (cores padrão da PlotWindow)
            initial_bands_color = '#8A2BE2' # Exemplo de roxo
            initial_dos_color = '#DA70D6'   # Exemplo de orquídea

            # Plota as bandas e DOS inicialmente
            self.plot_bands(ax_bands, bands_data, self.k_points_high_symmetry_values, self.k_points_high_symmetry_labels, self.fermi_level, initial_bands_color)
            self.plot_dos(ax_dos, dos_energies, dos_densities, initial_dos_color)

            # Define os limites Y e armazena-os
            if min_energy is not None and max_energy is not None:
                self.plot_y_limits = (min_energy, max_energy)
            else:
                all_bands_energies = [p[1] for band in bands_data for p in band]
                all_energies = all_bands_energies + dos_energies
                self.plot_y_limits = (min(all_energies) - 0.5, max(all_energies) + 0.5) if all_energies else (-5, 5)

            ax_bands.set_ylim(self.plot_y_limits)
            ax_dos.set_ylim(self.plot_y_limits)

            # --- REMOVIDO: fig.autofmt_xdate(rotation=45, ha='right') ---
            # Para manter os rótulos retos, removemos esta linha.

            # Ajusta o layout para evitar sobreposição (mantendo o suptitle visível)
            # O valor 0.05 no 'rect' do bottom é mantido para garantir um espaço mínimo para os rótulos,
            # mesmo que retos. Se eles se sobrepuserem, a solução será a largura da figura ou o tamanho da fonte.
            plt.tight_layout(rect=[0, 0.05, 1, 0.96])

            # Abre a nova janela de plotagem, passando todos os dados, eixos e os limites Y
            PlotWindow(self, fig, ax_bands, ax_dos, bands_data, dos_energies, dos_densities, self.k_points_high_symmetry_values, self.k_points_high_symmetry_labels, self.fermi_level, self.plot_y_limits)

        except Exception as e:
            messagebox.showerror("Erro ao Gerar Gráfico", f"Ocorreu um erro ao gerar o gráfico:\n{e}")
            if hasattr(self, 'fig') and self.fig: # Fecha a figura se ela foi criada mas houve erro
                plt.close(self.fig)

    def get_energy_range(self):
        try:
            min_e = float(self.min_energy_entry.get()) if self.min_energy_entry.get() else None
            max_e = float(self.max_energy_entry.get()) if self.max_energy_entry.get() else None
            return min_e, max_e
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira valores numéricos válidos para o intervalo de energia.")
            return None, None

    def plot_bands(self, ax, bands_data, k_points_high_symmetry_values, k_point_labels_with_symbols, fermi_level, plot_color):
        """Função para plotar o gráfico de Bandas."""
        ax.set_title("Estrutura de Bandas", fontsize=16, fontweight='bold')
        ax.set_ylabel("Energia (eV)", fontsize=12)
        ax.set_xlabel("pontos-k", fontsize=12, fontweight='bold')
        ax.axhline(0, color='red', linestyle='--', linewidth=1.5, label="Nível de Fermi ($E_F=0$)")

        for band in bands_data:
            ax.plot([p[0] for p in band], [p[1] for p in band], color=plot_color, linewidth=1.5)

        # Linhas verticais nos pontos de alta simetria
        for k_coord in k_points_high_symmetry_values:
            ax.axvline(x=k_coord, color='black', linestyle=':', linewidth=1.0, zorder=0) # zorder para garantir que esteja atrás das bandas

        ax.set_xticks(k_points_high_symmetry_values)
        ax.set_xticklabels(k_point_labels_with_symbols, fontsize=12, fontweight='bold')
        ax.set_xlim(k_points_high_symmetry_values[0], k_points_high_symmetry_values[-1])
        ax.grid(False)
        ax.legend(loc='lower left', fontsize=10)

    def plot_dos(self, ax, dos_energies, dos_densities, plot_color):
        """Função para plotar o gráfico de DOS."""
        ax.set_title("Densidade de Estados (DOS)", fontsize=16, fontweight='bold')
        ax.set_xlabel("DOS", fontsize=12)
        ax.axhline(0, color='red', linestyle='--', linewidth=1.5)
        ax.plot(dos_densities, dos_energies, color=plot_color, linewidth=1.5)

        dos_max = max(dos_densities) if dos_densities else 1
        ax.set_xlim(0, dos_max * 1.1)

        ax.tick_params(axis='x', labelbottom=False)
        ax.tick_params(axis='y', labelleft=False)
        ax.grid(False)

if __name__ == "__main__":
    app = App()
    app.mainloop()
