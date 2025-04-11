import os
import subprocess
import shutil
import threading
import tkinter as tk
from tkinter import messagebox, ttk

INPUT_FOLDER = "Input"
OUTPUT_FOLDER = "Output"
TARGET_SIZE_MB = 10
TARGET_SIZE_BYTES = TARGET_SIZE_MB * 1024 * 1024

def ensure_folders():
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_duration(input_path):
    try:
        result = subprocess.check_output([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_path
        ], stderr=subprocess.STDOUT)
        return float(result.strip())
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter duração: {e.output.decode()}")
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

        target_bitrate = int((TARGET_SIZE_BYTES * 8) / duration)

        # Configurações baseadas na qualidade escolhida
        if quality == "Alta":
            preset = "fast"
            scale = None
        elif quality == "Média":
            preset = "faster"
            scale = "1280:720"
        else:  # Baixa
            preset = "ultrafast"
            scale = "854:480"

        compress_cmd = ["ffmpeg", "-i", input_path]

        if scale:
            compress_cmd += ["-vf", f"scale={scale}"]

        compress_cmd += [
            "-b:v", f"{target_bitrate}",
            "-maxrate", f"{target_bitrate}",
            "-bufsize", f"{target_bitrate}",
            "-preset", preset,
            "-y", output_path
        ]

        print(f"Comprimindo {os.path.basename(input_path)} em qualidade {quality.lower()}...")
        subprocess.run(compress_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=120)

        final_size = os.path.getsize(output_path)
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
    root = tk.Tk()
    root.title("Compressor de Vídeos < 10MB")
    root.geometry("400x250")
    root.resizable(False, False)

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
