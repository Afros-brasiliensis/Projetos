"""
YouTube Downloader - Interface Completa
Autor: Você + Claude
"""

import yt_dlp
import os
from tkinter import filedialog
import shutil
import customtkinter as ctk
from pathlib import Path
import threading

# Configuração tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ============================================================
# CLASSE PRINCIPAL
# ============================================================
class YoutubeDownloaderApp:
    def __init__(self):
        # Janela principal
        self.window = ctk.CTk()
        self.window.title("YouTube Downloader")
        self.window.geometry("650x700")
        self.window.resizable(False, False)
        
        # Pasta padrão
        self.home_dir = str(Path.home() / "Downloads")
        
        # Criar interface
        self.create_interface()
        
        # Verificar FFmpeg
        self.verify_ffmpeg()
    
    # ========================================================
    # VERIFICAR FFMPEG
    # ========================================================
    def verify_ffmpeg(self):
        """Verifica se FFmpeg está instalado no sistema"""
        if shutil.which("ffmpeg"):
            self.status_ffmpeg.configure(
                text="✅ FFmpeg detectado - Qualidade perfeita!",
                text_color=("#00ff00", "#00cc00")
            )
        else:
            self.status_ffmpeg.configure(
                text="⚠️ FFmpeg não encontrado - Qualidade pode ser afetada",
                text_color=("#ffaa00", "#ff8800")
            )
    
    # ========================================================
    # CRIAR INTERFACE
    # ========================================================
    def create_interface(self):
        """Monta toda a interface visual"""
        
        # ====================================================
        # CABEÇALHO
        # ====================================================
        frame_header = ctk.CTkFrame(
            self.window,
            fg_color=("#0c70a6", "#095077"),
            height=150,
            corner_radius=0
        )
        frame_header.pack(fill="x", pady=0)
        frame_header.pack_propagate(False)
        
        # Título
        label_title = ctk.CTkLabel(
            frame_header,
            text="🎥 YouTube Downloader",
            font=("Segoe UI", 36, "bold"),
            text_color="white"
        )
        label_title.pack(pady=(25, 5))
        
        # Subtítulo
        label_subtitle = ctk.CTkLabel(
            frame_header,
            text="Suporta YouTube, Vimeo, TikTok, Twitter, Instagram e 1000+ sites ✨",
            font=("Segoe UI", 12),
            text_color="#f0f0f0"
        )
        label_subtitle.pack(pady=0)
        
        # Status FFmpeg
        self.status_ffmpeg = ctk.CTkLabel(
            frame_header,
            text="🔍 Verificando FFmpeg...",
            font=("Segoe UI", 11),
            text_color="white"
        )
        self.status_ffmpeg.pack(pady=(10, 15))
        
        # ====================================================
        # CORPO PRINCIPAL
        # ====================================================
        frame_content = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        frame_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # ====================================================
        # SEÇÃO: URL
        # ====================================================
        label_url = ctk.CTkLabel(
            frame_content,
            text="📎 URL do Vídeo",
            font=("Segoe UI", 15, "bold"),
            anchor="w"
        )
        label_url.pack(fill="x", pady=(0, 8))
        
        # Input URL
        self.input_url = ctk.CTkEntry(
            frame_content,
            placeholder_text="Cole a URL aqui...",
            height=45,
            font=("Segoe UI", 13),
            border_width=2,
            corner_radius=10
        )
        self.input_url.pack(fill="x", pady=(0, 25))
        
        # Enter para download
        self.input_url.bind("<Return>", lambda e: self.start_download())
        
        # ====================================================
        # SEÇÃO: PASTA
        # ====================================================
        label_folder = ctk.CTkLabel(
            frame_content,
            text="📁 Pasta de Destino",
            font=("Segoe UI", 15, "bold"),
            anchor="w"
        )
        label_folder.pack(fill="x", pady=(0, 8))
        
        # Frame pasta
        frame_folder = ctk.CTkFrame(
            frame_content,
            fg_color="transparent"
        )
        frame_folder.pack(fill="x", pady=(0, 25))
        
        # Label caminho
        self.label_path = ctk.CTkLabel(
            frame_folder,
            text=self.home_dir,
            font=("Segoe UI", 11),
            text_color="gray",
            anchor="w"
        )
        self.label_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botão escolher pasta
        btn_folder = ctk.CTkButton(
            frame_folder,
            text="📂 Escolher",
            command=self.choose_folder,
            width=120,
            height=38,
            font=("Segoe UI", 12, "bold"),
            corner_radius=10
        )
        btn_folder.pack(side="right")
        
        # ====================================================
        # BOTÃO DOWNLOAD
        # ====================================================
        self.btn_download = ctk.CTkButton(
            frame_content,
            text="⬇️ BAIXAR VÍDEO",
            command=self.start_download,
            height=55,
            font=("Segoe UI", 18, "bold"),
            fg_color=("#0c70a6", "#095077"),
            hover_color=("#095077", "#063d4d"),
            corner_radius=12
        )
        self.btn_download.pack(fill="x", pady=(0, 25))
        
        # ====================================================
        # BARRA DE PROGRESSO
        # ====================================================
        self.progress_bar = ctk.CTkProgressBar(
            frame_content,
            height=18,
            corner_radius=10,
            progress_color=("#0c70a6", "#095077")
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # Info progresso
        frame_progress_info = ctk.CTkFrame(
            frame_content,
            fg_color="transparent"
        )
        frame_progress_info.pack(fill="x", pady=(0, 20))
        
        self.label_percent = ctk.CTkLabel(
            frame_progress_info,
            text="0%",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.label_percent.pack(side="left")
        
        self.label_speed = ctk.CTkLabel(
            frame_progress_info,
            text="--",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.label_speed.pack(side="right")
        
        # ====================================================
        # STATUS
        # ====================================================
        self.label_status = ctk.CTkLabel(
            frame_content,
            text="Pronto para baixar! 🚀",
            font=("Segoe UI", 13),
            text_color="gray",
            wraplength=550
        )
        self.label_status.pack(pady=(0, 10))
        
        # ====================================================
        # RODAPÉ
        # ====================================================
        label_footer = ctk.CTkLabel(
            self.window,
            text="Made with ❤️ | Supports 1000+ sites",
            font=("Segoe UI", 10),
            text_color="gray"
        )
        label_footer.pack(side="bottom", pady=20)
    
    # ========================================================
    # ESCOLHER PASTA
    # ========================================================
    def choose_folder(self):
        """Abre diálogo para escolher pasta"""
        folder = filedialog.askdirectory(
            title="Escolha a pasta de destino",
            initialdir=self.home_dir
        )
        
        if folder:
            self.home_dir = folder
            self.label_path.configure(text=folder)
    
    # ========================================================
    # ATUALIZAR STATUS
    # ========================================================
    def update_status(self, message, color="gray"):
        """Atualiza mensagem de status"""
        self.label_status.configure(text=message, text_color=color)
    
    # ========================================================
    # HOOK DE PROGRESSO
    # ========================================================
    def progress_hook(self, d):
        """Callback do yt-dlp para progresso"""
        if d['status'] == 'downloading':
            try:
                # Porcentagem
                percent_str = d.get('_percent_str', '0%').replace('%', '')
                percent = float(percent_str) / 100
                
                # Atualizar barra
                self.progress_bar.set(percent)
                self.label_percent.configure(text=f"{percent_str}%")
                
                # Velocidade
                speed = d.get('_speed_str', 'N/A')
                self.label_speed.configure(text=speed)
                
                # Status
                self.update_status(
                    f"⬇️ Baixando... {percent_str}%",
                    ("#00aaff", "#0088dd")
                )
            except:
                pass
        
        elif d['status'] == 'finished':
            self.update_status(
                "🔧 Processando com FFmpeg...",
                ("#ffaa00", "#ff8800")
            )
    
    # ========================================================
    # DOWNLOAD (THREAD)
    # ========================================================
    def download_video(self):
        """Executa download em background"""
        url = self.input_url.get().strip()
        
        # Validar URL
        if not url:
            self.update_status(
                "❌ Insira uma URL válida!",
                ("#ff0000", "#cc0000")
            )
            self.btn_download.configure(state="normal")
            return
        
        # Verificar se começa com http
        if not url.startswith(('http://', 'https://')):
            self.update_status(
                "❌ URL deve começar com http:// ou https://",
                ("#ff0000", "#cc0000")
            )
            self.btn_download.configure(state="normal")
            return
        
        # Criar pasta se não existir
        if not os.path.exists(self.home_dir):
            os.makedirs(self.home_dir)
        
        # Opções yt-dlp
        options = {
            'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]',
            'outtmpl': f'{self.home_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [self.progress_hook],
            'postprocessors': [
                {
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ],
            'postprocessor_args': {
                'ffmpeg': [
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-movflags', '+faststart',
                    '-strict', '-2',
                ]
            },
        }
        
        try:
            # Buscar info
            self.update_status(
                "📊 Obtendo informações...",
                ("#00aaff", "#0088dd")
            )
            
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Desconhecido')
                
                self.update_status(
                    f"⬇️ Baixando: {title[:40]}...",
                    ("#00aaff", "#0088dd")
                )
                
                ydl.download([url])
            
            # Sucesso
            self.progress_bar.set(1)
            self.label_percent.configure(text="100%")
            self.update_status(
                "✅ Download concluído!",
                ("#00ff00", "#00cc00")
            )
            
        except Exception as e:
            # Erro
            self.progress_bar.set(0)
            self.label_percent.configure(text="0%")
            self.label_speed.configure(text="--")
            self.update_status(
                f"❌ Erro: {str(e)[:60]}...",
                ("#ff0000", "#cc0000")
            )
        
        finally:
            # Reativar botão
            self.btn_download.configure(state="normal")
    
    # ========================================================
    # INICIAR DOWNLOAD
    # ========================================================
    def start_download(self):
        """Inicia download em thread"""
        # Desabilitar botão
        self.btn_download.configure(state="disabled")
        
        # Resetar progresso
        self.progress_bar.set(0)
        self.label_percent.configure(text="0%")
        self.label_speed.configure(text="--")
        
        # Thread separada
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()
    
    # ========================================================
    # EXECUTAR
    # ========================================================
    def run(self):
        """Inicia aplicação"""
        self.window.mainloop()

# ============================================================
# EXECUTAR PROGRAMA
# ============================================================
if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.run()