import sys
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QPixmap, QFontDatabase, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QApplication, QFileDialog, QHBoxLayout
)
import config.gradient
from styles.buttons import button_style
from styles.main_window import default_text


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
        self.setStyleSheet(config.gradient.gradient_brown)  # Фон для основного виджета
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
        return menu_label

    def setup_header_service_menu(self):
        # layout1 = self.crete_control_window()
        menu = QPushButton(self)
        menu.setStyleSheet(button_style)
        menu.setIcon(QIcon("resources/menu.png"))
        menu.setIconSize(QSize(32, 32))
        menu.setFixedSize(40, 40)

        wrap = QPushButton(self)
        wrap.setStyleSheet(button_style)
        wrap.setIcon(QIcon("resources/wrap.png"))
        wrap.setIconSize(QSize(32, 32))
        wrap.setFixedSize(40, 40)
        wrap.move(1160, 0)

        maximize = QPushButton(self)
        maximize.setStyleSheet(button_style)
        maximize.setIcon(QIcon("resources/maximize.png"))
        maximize.setIconSize(QSize(32, 32))
        maximize.setFixedSize(40, 40)
        maximize.move(1200, 0)

        close = QPushButton(self)
        close.setStyleSheet(button_style)
        close.setIcon(QIcon("resources/close.png"))
        close.setIconSize(QSize(32, 32))
        close.setFixedSize(40, 40)
        close.move(1240, 0)

        inner_layout = self.create_header_info()

        return inner_layout

    def create_header_info(self):
        # Внутренний QHBoxLayout
        # ЗДЕСЬ ВСЁ ДЕРЖИТСЯ НА ИКОНКЕ (ЛОГО)
        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(10)  # Установите нужное расстояние между элементами

        # Иконка
        icon = QLabel()
        pixmap = QPixmap("logo.jpg")
        icon.setPixmap(pixmap)
        icon.setMaximumHeight(40)
        icon.setStyleSheet('QLabel { background-color: transparent; }')

        # Название плеера
        name_player = QLabel('<span style="color: white;">Tao</span> <span style="color: #BD321D;">Player</span>', self)
        name_player.setStyleSheet(default_text + "font-size: 16px; font-weight: bold;")
        name_player.move(530, 5)

        # Версия плеера
        version = QLabel("ver. 0.1 alpha", self)
        version.setStyleSheet(default_text + "font-size: 14px; font-weight: regular; color: white;")
        version.move(670, 5)

        inner_layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        return inner_layout

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

    def test(self):
        print("test")

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
