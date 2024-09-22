import sys
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QPixmap, QIcon
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
        self.drag_start_position = None
        self.default_window_geometry = (300, 200, 1280, 720)

        # Инициализация медиаплеера и виджета видео
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_widget = QVideoWidget()
        self.configure_video_widget()

        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        self.initialize_ui()
        self.set_window_position()

    def configure_video_widget(self):
        """Настройка виджета видео."""
        self.video_widget.setMinimumWidth(1280)
        self.video_widget.setMinimumHeight(525)

    def initialize_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(config.gradient.gradient_brown)  # Фон для основного виджета
        self.setWindowTitle('Tao Player')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addLayout(self.create_header_menu())
        layout.addWidget(self.video_widget)
        layout.addWidget(self.create_control_menu(), alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)

    def set_window_position(self):
        """Установка позиции окна на экране."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        if screen_rect.width() >= 1920:
            self.setGeometry(*self.default_window_geometry)

    def create_control_menu(self):
        """Создание меню управления."""

        label = QLabel("МЕНЮ УПРАВЛЕНИЯ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(155)
        return label

    def create_header_menu(self):
        """Создание шапки окна"""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        header_layout.setSpacing(0)

        inner_layout = self.create_header_info()

        menu_button = QPushButton(self)
        menu_button.setIcon(QIcon("resources/menu.png"))
        menu_button.setIconSize(QSize(32, 32))  # Устанавливаем размер иконки
        menu_button.setFixedSize(40, 40)  # Устанавливаем фиксированный размер кнопки
        menu_button.setStyleSheet(button_style)

        header_layout.addLayout(inner_layout)
        self.create_window_control_buttons()

        return header_layout

    def create_window_control_buttons(self):
        """Создание кнопок для хедера"""
        wrap_button = self.create_icon_button("resources/wrap.png", self.on_load_video_button_clicked)
        wrap_button.move(1160, 0)

        maximize_button = self.create_icon_button("resources/maximize.png", lambda: None)
        maximize_button.move(1200, 0)

        close_button = self.create_icon_button("resources/close.png", lambda: None)
        close_button.move(1240, 0)

    def create_icon_button(self, icon_path, action=None):
        """Генератор кнопок для хедера"""
        button = QPushButton(self)
        button.setStyleSheet(button_style)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(40, 40))
        button.setFixedSize(40, 40)
        button.clicked.connect(action)
        return button

    def create_header_info(self):
        """Создание внутреннего QHBoxLayout для заголовка."""
        inner_layout = QHBoxLayout()
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(10)

        # Иконка
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.jpg")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setMaximumHeight(40)
        logo_label.setStyleSheet('QLabel { background-color: transparent; }')

        # Название плеера
        player_name_label = QLabel('<span style="color: white;">Tao</span> <span style="color: #BD321D;">Player</span>', self)
        player_name_label.setStyleSheet(default_text + "font-size: 16px; font-weight: bold;")
        player_name_label.move(530, 5)

        # Версия плеера
        version_label = QLabel("ver. 0.1 alpha", self)
        version_label.setStyleSheet(default_text + "font-size: 14px; font-weight: regular; color: white;")
        version_label.move(668, 4)

        # Добавляем элементы во внутренний layout
        inner_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        return inner_layout

    def create_button(self, text):
        """Создание кнопки."""
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.clicked.connect(self.on_load_video_button_clicked)
        return button

    def mousePressEvent(self, event):
        """Обработка нажатия мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Обработка перемещения мыши."""
        if self.drag_start_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_start_position)

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = None

    def on_load_video_button_clicked(self):
        """Обработка нажатия кнопки загрузки видео."""
        video_file, _ = QFileDialog.getOpenFileName(self, "Выберите видео файл", "", "Video Files (*.mp4 *.avi *.mkv)")
        if video_file:
            self.load_video(video_file)

    def load_video(self, video_file):
        """Загрузка и воспроизведение видео."""
        print(f"Выбран файл: {video_file}")  # Отладочное сообщение
        self.media_player.setSource(QUrl.fromLocalFile(video_file))
        self.media_player.play()
