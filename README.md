# 📦 Video Compressor for Discord (<10MB)

A simple and user-friendly Python tool with a graphical interface that compresses your videos to under 10MB — perfect for sharing on Discord!

---

## 🔧 Features

- Compresses videos to under 10MB
- Graphical interface with quality options: High, Medium, Low
- Automatically copies videos already under 10MB without recompression
- Automatically creates `Input` and `Output` folders
- Supports `.mp4`, `.mov`, `.avi`, `.mkv` formats

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HeitorSpectre/Video-Compressor-10MB-.git
cd Video-Compressor-10MB
```

2. Instale o Python
Baixe e instale o Python 3.10 ou superior:

```bash
👉 https://www.python.org/downloads/
```

⚠️ Marque a opção "Add Python to PATH" durante a instalação.

3. Instale o FFmpeg
Windows:

```bash
Baixe o zip: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
```

Extraia o conteúdo (ex: C:\ffmpeg)

Adicione ```C:\ffmpeg\bin ao seu PATH (painel de controle > sistema > variáveis de ambiente)```

Linux/macOS:

```bash
Copiar
Editar
sudo apt install ffmpeg    # Debian/Ubuntu
brew install ffmpeg        # macOS
```

4. Instale as dependências Python
   
```bash
Copiar
Editar
pip install -r requirements.txt
```
