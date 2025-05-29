import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QProgressBar, QLabel, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

OUTPUT_DIR = "output_videos"

class VideoProcessor(QThread):
    progress_update = pyqtSignal(int, int)  # index, percent
    status_update = pyqtSignal(int, str, str)  # index, emoji, status text

    def __init__(self, index, input_path):
        super().__init__()
        self.index = index
        self.input_path = input_path

    def run(self):
        filename = os.path.basename(self.input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.mp4")

        cmd = [
            "ffmpeg", "-y", "-i", self.input_path, "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "boxblur=40:1,scale='trunc(iw/2)*2':'trunc(ih/2)*2'[blurred];"
            "[0:v]scale=w=1080:h=1920:force_original_aspect_ratio=decrease,"
            "scale='trunc(iw/2)*2':'trunc(ih/2)*2'[scaled];"
            "color=white:s=1080x1920[c];"
            "[c][blurred]overlay[bg];"
            "[bg][scaled]overlay=(W-w)/2:(H-h)/2:shortest=1",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "copy", output_path
        ]

        try:
            self.status_update.emit(self.index, "⏳", f"{filename} işleniyor...")
            # Simüle edilmiş ilerleme
            for i in range(1, 101, 5):
                self.progress_update.emit(self.index, i)
                time.sleep(0.1)  # bu sadece görsellik için

            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.progress_update.emit(self.index, 100)
            self.status_update.emit(self.index, "✅", f"{filename} tamamlandı!")
        except subprocess.CalledProcessError:
            self.status_update.emit(self.index, "❌", f"{filename} başarısız!")

class VideoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 9:16 Blur Video İşleyici")
        self.resize(700, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.select_btn = QPushButton("📂 Videoları Seç")
        self.select_btn.clicked.connect(self.select_files)
        self.layout.addWidget(self.select_btn)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.video_widgets = []
        self.threads = []

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Video Dosyalarını Seç", "", "Video Files (*.mp4 *.mov *.mts *.avi *.mkv)"
        )

        if not files:
            return

        self.clear_grid()
        for i, file in enumerate(files):
            name = os.path.basename(file)
            label = QLabel(f"🎞 {name}")
            progress_bar = QProgressBar()
            progress_bar.setValue(0)
            status = QLabel("⏳ Beklemede...")

            self.grid_layout.addWidget(label, i, 0)
            self.grid_layout.addWidget(progress_bar, i, 1)
            self.grid_layout.addWidget(status, i, 2)

            self.video_widgets.append((progress_bar, status))

            thread = VideoProcessor(i, file)
            thread.progress_update.connect(self.update_progress)
            thread.status_update.connect(self.update_status)
            self.threads.append(thread)

        for thread in self.threads:
            thread.start()

    def update_progress(self, index, percent):
        progress_bar, _ = self.video_widgets[index]
        progress_bar.setValue(percent)

    def update_status(self, index, emoji, message):
        _, status_label = self.video_widgets[index]
        status_label.setText(f"{emoji} {message}")

    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()
        self.video_widgets = []
        self.threads = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoGUI()
    gui.show()
    sys.exit(app.exec_())
