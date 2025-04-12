import os
import subprocess
import shutil
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json

INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"
TARGET_SIZE_MB = 10
TARGET_SIZE_BYTES = TARGET_SIZE_MB * 1024 * 1024
CONFIG_FILE = "config.json"

ffmpeg_path = "ffmpeg"
ffprobe_path = "ffprobe"

def ensure_folders():
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"ffmpeg_path": ffmpeg_path}, f)

def load_config():
    global ffmpeg_path, ffprobe_path
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            ffmpeg_path = config.get("ffmpeg_path", "ffmpeg")
            ffprobe_path = ffmpeg_path.replace("ffmpeg.exe", "ffprobe.exe")

def select_ffmpeg_path():
    global ffmpeg_path, ffprobe_path
    selected_path = filedialog.askopenfilename(title="Selecione o ffmpeg.exe", filetypes=[("Executável", "ffmpeg.exe")])
    if selected_path:
        ffmpeg_path = selected_path
        ffprobe_path = ffmpeg_path.replace("ffmpeg.exe", "ffprobe.exe")
        save_config()

def ffmpeg_available():
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run([ffprobe_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def get_duration(input_path):
    try:
        result = subprocess.check_output([
            ffprobe_path, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_path
        ], stderr=subprocess.STDOUT)
        return float(result.strip())
    except Exception as e:
        print(f"Erro ao obter duração: {e}")
        return None

def compress_video(input_path, output_path, quality):
    try:
        if not os.path.exists(input_path):
            print(f"Arquivo não encontrado: {input_path}")
            return

        size_bytes = os.path.getsize(input_path)
        if size_bytes <= TARGET_SIZE_BYTES:
            print(f"{os.path.basename(input_path)} já está abaixo de {TARGET_SIZE_MB} MB. Copiando sem alterar.")
            shutil.copy2(input_path, output_path)
            return

        duration = get_duration(input_path)
        if duration is None or duration == 0:
            print(f"Não foi possível obter a duração do vídeo: {input_path}")
            return

        safe_target_size_bytes = int(TARGET_SIZE_BYTES * 0.95)
        target_bitrate = int((safe_target_size_bytes * 8) / duration)

        if quality == "Alta":
            preset = "fast"
            scale = None
        elif quality == "Média":
            preset = "faster"
            scale = "1280:720"
        else:
            preset = "ultrafast"
            scale = "640:360"

        log_file = "ffmpeg2pass"

        first_pass = [ffmpeg_path, "-y", "-i", input_path, "-c:v", "libx264"]
        if scale:
            first_pass += ["-vf", f"scale={scale}"]
        first_pass += [
            "-b:v", f"{target_bitrate}",
            "-maxrate", f"{target_bitrate}",
            "-bufsize", f"{target_bitrate}",
            "-preset", preset,
            "-pass", "1",
            "-an",
            "-f", "mp4", "NUL" if os.name == "nt" else "/dev/null"
        ]

        second_pass = [ffmpeg_path, "-y", "-i", input_path, "-c:v", "libx264"]
        if scale:
            second_pass += ["-vf", f"scale={scale}"]
        second_pass += [
            "-b:v", f"{target_bitrate}",
            "-maxrate", f"{target_bitrate}",
            "-bufsize", f"{target_bitrate}",
            "-preset", preset,
            "-pass", "2",
            "-c:a", "aac",
            "-b:a", "96k",
            output_path
        ]

        print(f"Comprimindo {os.path.basename(input_path)} em qualidade {quality.lower()} com 2-pass...")

        subprocess.run(first_pass, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=120)
        subprocess.run(second_pass, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=120)

        for ext in [".log", "-0.log", "-0.log.mbtree"]:
            try:
                os.remove(f"{log_file}{ext}")
            except FileNotFoundError:
                pass

        final_size = os.path.getsize(output_path)
        if final_size > TARGET_SIZE_BYTES:
            print(f"❌ {os.path.basename(input_path)} ficou com {round(final_size / 1024 / 1024, 2)} MB! Excluindo...")
            os.remove(output_path)
        else:
            print(f"✔️ {os.path.basename(input_path)} comprimido com sucesso. Novo tamanho: {round(final_size / 1024 / 1024, 2)} MB")

    except subprocess.TimeoutExpired:
        print(f"⏱️ Tempo excedido ao comprimir {input_path}. Pulando...")
    except Exception as e:
        print(f"❌ Erro ao processar {input_path}: {e}")

def compress_all_videos(quality):
    ensure_folders()
    input_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]

    if not input_files:
        print(f"Nenhum vídeo encontrado na pasta '{INPUT_FOLDER}'.")
        return

    print(f"Iniciando compressão de {len(input_files)} arquivo(s) com qualidade {quality}...\n")
    for i, filename in enumerate(input_files, 1):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        print(f"[{i}/{len(input_files)}] Processando: {filename}")
        compress_video(input_path, output_path, quality)
        print("-" * 40)

    print("✔️ Compressão finalizada!")
    messagebox.showinfo("Finalizado", f"Compressão concluída! Confira a pasta '{OUTPUT_FOLDER}'.")

def start_compression_thread(quality):
    thread = threading.Thread(target=compress_all_videos, args=(quality,))
    thread.start()

def create_gui():
    ensure_folders()
    load_config()

    if not ffmpeg_available():
        select_ffmpeg_path()
        if not ffmpeg_available():
            messagebox.showerror("Erro", "FFmpeg ainda não foi encontrado.")
            return

    root = tk.Tk()
    root.title("Compressor de Vídeos < 10MB")
    root.geometry("400x250")
    root.resizable(False, False)

    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="Configurações", command=select_ffmpeg_path)

    tk.Label(root, text="💾 Compressor de Vídeos para Discord", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text=f"Coloque os vídeos na pasta '{INPUT_FOLDER}'\ne escolha a qualidade desejada", font=("Arial", 10)).pack(pady=5)

    quality_label = tk.Label(root, text="Qualidade da compressão:", font=("Arial", 11))
    quality_label.pack(pady=(10, 0))

    quality_var = tk.StringVar(value="Média")
    quality_menu = ttk.Combobox(root, textvariable=quality_var, state="readonly", font=("Arial", 10))
    quality_menu["values"] = ["Alta", "Média", "Baixa"]
    quality_menu.pack(pady=5)

    compress_btn = tk.Button(root, text="Comprimir Vídeos", font=("Arial", 12), bg="#4CAF50", fg="white",
                             command=lambda: start_compression_thread(quality_var.get()))
    compress_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
