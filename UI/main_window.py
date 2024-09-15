import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
)
import config.gradient


class TaoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.startPos = None
        self.default_coordinates = (300, 200, 1280, 720)

        # Инициализация медиаплеера и виджета видео
        self.media_player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.video_widget = QVideoWidget()
        self.setup_video_widget()

        self.media_player.setAudioOutput(self.audio)
        self.media_player.setVideoOutput(self.video_widget)

        self.init_ui()
        self.set_position()

    def setup_video_widget(self):
        """Настройка виджета видео."""
        self.video_widget.setMinimumWidth(1280)
        self.video_widget.setMinimumHeight(525)

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle('Tao Player')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addLayout(self.setup_header_service_menu())
        layout.addWidget(self.video_widget)
        layout.addWidget(self.setup_menu_control_video(), alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)

    def set_position(self):
        """Установка позиции окна на экране."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        if screen_rect.width() >= 1920:
            self.setGeometry(*self.default_coordinates)

    def setup_menu_control_video(self):
        """Создание меню управления."""
        menu_label = self.create_label("МЕНЮ УПРАВЛЕНИЯ", 155)
        menu_label.setStyleSheet(config.gradient.gradient_brown)
        return menu_label

    def setup_header_service_menu(self):




    def create_label(self, text, height):
        """Создание метки."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(height)
        return label

    def create_button(self, text):
        """Создание кнопки."""
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(self.on_button_clicked)
        return button

    def mousePressEvent(self, event):
        """Обработка нажатия мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Обработка перемещения мыши."""
        if self.startPos is not None:
            self.move(event.globalPosition().toPoint() - self.startPos)

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = None

    def on_button_clicked(self):
        """Обработка нажатия кнопки загрузки видео."""
        video_file, _ = QFileDialog.getOpenFileName(self, "Выберите видео файл", "", "Video Files (*.mp4 *.avi *.mkv)")
        if video_file:
            self.load_video(video_file)

    def load_video(self, video_file):
        """Загрузка и воспроизведение видео."""
        print(f"Выбран файл: {video_file}")  # Отладочное сообщение
        self.media_player.setSource(QUrl.fromLocalFile(video_file))
        self.media_player.play()  # Запускаем воспроизведение
        print("Воспроизведение видео начато.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaoApp()
    window.show()
    sys.exit(app.exec())
