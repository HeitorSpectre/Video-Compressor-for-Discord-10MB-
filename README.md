# 📦 Video Compressor for Discord (<10MB)

A simple and user-friendly Python tool with a graphical interface that compresses your videos to under 10MB — perfect for sharing on Discord!

---

## 🔧 Features

- ✅ Compresses videos to under 10MB  
- ✅ Graphical interface with quality options: High, Medium, Low  
- ✅ Automatically copies videos already under 10MB without recompression  
- ✅ Automatically creates `Input` and `Output` folders  
- ✅ Supports `.mp4`, `.mov`, `.avi`, `.mkv` formats  
- ✅ Drag-and-drop simplicity (just place videos into the Input folder)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HeitorSpectre/Video-Compressor-10MB-.git
cd Video-Compressor-10MB
```

### 2. Install Python

Download and install Python 3.10 or higher:  
👉 https://www.python.org/downloads/

⚠️ **Be sure to check the option "Add Python to PATH" during installation.**

### 3. Install FFmpeg

#### 🪟 Windows

1. Download the zip file:  
   👉 https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip  
2. Extract it to a folder (e.g., `C:\ffmpeg`)  
3. Add `C:\ffmpeg\bin` to your system `PATH`:  
   - Control Panel → System → Advanced system settings → Environment Variables

#### 🐧 Linux

```bash
sudo apt install ffmpeg
```

#### 🍎 macOS

```bash
brew install ffmpeg
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

1. Put all your videos into the `Input` folder  
2. Run the tool:

```bash
python compressor.py
```

3. Select the compression quality:  
   - **High** (slightly compressed, better quality)  
   - **Medium** (balance of quality and size)  
   - **Low** (smaller size, faster, lower quality)

4. The compressed videos will appear in the `Output` folder  
5. Done! Ready to send them on Discord 🚀

---

## 📂 Project Structure

```bash
Video-Compressor-10MB/
├── Input/                                 # Place your original videos here
├── Output/                                # Compressed videos will be saved here
├── Compressor de Vídeos (10MB).py         # Main Python application
├── requirements.txt                       # Python dependencies
└── README.md                              # Project documentation
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
