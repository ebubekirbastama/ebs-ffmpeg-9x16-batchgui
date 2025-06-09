import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QProgressBar, QLabel, QGridLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

OUTPUT_DIR = "output_videos"

class VideoProcessor(QThread):
    progress_update = pyqtSignal(int, int)  # index, percent
    status_update = pyqtSignal(int, str, str)  # index, emoji, status text

    def __init__(self, index, input_path, mode):
        super().__init__()
        self.index = index
        self.input_path = input_path
        self.mode = mode  # "vertical" or "horizontal"

    def run(self):
        filename = os.path.basename(self.input_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.mp4")

        if self.mode == "vertical":
            resolution = "1080x1920"
        else:
            resolution = "1920x1080"

        width, height = resolution.split("x")

        cmd = [
            "ffmpeg", "-y", "-i", self.input_path, "-filter_complex",
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            "boxblur=40:1,scale='trunc(iw/2)*2':'trunc(ih/2)*2'[blurred];"
            f"[0:v]scale=w={width}:h={height}:force_original_aspect_ratio=decrease,"
            "scale='trunc(iw/2)*2':'trunc(ih/2)*2'[scaled];"
            f"color=white:s={resolution}[c];"
            "[c][blurred]overlay[bg];"
            "[bg][scaled]overlay=(W-w)/2:(H-h)/2:shortest=1",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "copy", output_path
        ]

        try:
            self.status_update.emit(self.index, "⏳", f"{filename} işleniyor...")
            for i in range(1, 101, 5):
                self.progress_update.emit(self.index, i)
                time.sleep(0.1)

            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.progress_update.emit(self.index, 100)
            self.status_update.emit(self.index, "✅", f"{filename} tamamlandı!")
        except subprocess.CalledProcessError:
            self.status_update.emit(self.index, "❌", f"{filename} başarısız!")

class VideoGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Video Blur İşleyici")
        self.resize(750, 550)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.mode_selector = QComboBox()
        self.mode_selector.addItem("📱 Dikey (9:16)", userData="vertical")
        self.mode_selector.addItem("🖥️ Yatay (16:9)", userData="horizontal")
        self.layout.addWidget(self.mode_selector)

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
        selected_mode = self.mode_selector.currentData()

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

            thread = VideoProcessor(i, file, selected_mode)
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
