# 📦 Video Compressor for Discord (<10MB)

A simple and user-friendly tool with a graphical interface that compresses your videos to under 10MB — perfect for sharing on Discord!

---

## 🔧 Features

- ✅ Compresses videos to under 10MB  
- ✅ Graphical interface with quality options: High, Medium, Low  
- ✅ Automatically copies videos already under 10MB without recompression  
- ✅ Automatically creates `Input` and `Output` folders  
- ✅ Supports `.mp4`, `.mov`, `.avi`, `.mkv` formats  
- ✅ Drag-and-drop simplicity (just place videos into the Input folder)  
- ✅ **Mandatory** configuration of the FFmpeg path on your system  
- ✅ Ensures the compressed video size is **strictly under 10MB** (no 10.1MB allowed!)

---

## 💻 How to Use (Executable)

No setup or extraction needed!

1. Download the `.exe` file from the [Releases](https://github.com/HeitorSpectre/Video-Compressor-for-Discord-10MB-/releases/tag/1.0) page  
2. Run the file directly (double-click)  
3. When prompted, click the **"Config"** button to choose the location of `ffmpeg.exe` on your system  
4. Place your videos inside the `Input` folder  
5. Select compression quality (High, Medium, Low)  
6. Click “Compress Videos”  
7. Compressed videos will be saved to the `Output` folder — ready for Discord!

> ⚠️ **Important**: The FFmpeg path must be configured before using the tool. If it's not set, the application will prompt you to select the location of `ffmpeg.exe` when you first launch it. This is a **mandatory** step.

---

## 🐍 Optional: Run From Source (Python)

If you prefer running the script manually via Python:

### 1. Clone the repository

```bash
git clone https://github.com/HeitorSpectre/Video-Compressor-for-Discord-10MB-
```

### 2. Install Python

Download and install Python 3.10 or higher:  
👉 https://www.python.org/downloads/

> ⚠️ Make sure to check **"Add Python to PATH"** during installation.

### 3. Install FFmpeg

#### 🪟 Windows

1. Download the zip:  
   👉 https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip  
2. Extract to a folder (e.g., `C:\ffmpeg`)  
3. Add `C:\ffmpeg\bin` to your system `PATH`  
   - Control Panel → System → Advanced system settings → Environment Variables

#### 🐧 Linux

```bash
sudo apt install ffmpeg
```

#### 🍎 macOS

```bash
brew install ffmpeg
```

### 4. Run the tool

```bash
python "Compressor de Vídeos (10MB).py"
```

---

## ▶️ Compression Options

- **High**: Better visual quality, larger file size  
- **Medium**: Balanced quality and size  
- **Low**: Faster compression, smaller size, lower quality

---

## 📂 Project Structure

```bash
Video-Compressor-10MB/
├── Input/                              # Put your original videos here
├── Output/                             # Compressed videos will appear here
├── Compressor de Vídeos (10MB).py      # Main Python script
└── README.md                           # Project documentation
```

---

## 🧠 Built With

- 🐍 Python 3
- 🎞 FFmpeg
- 🖼 Tkinter (for GUI)

---

## 📝 License

MIT License

---

## 🙌 Author

Created with ❤️ by [HeitorSpectre](https://github.com/HeitorSpectre)
