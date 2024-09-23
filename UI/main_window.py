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
from config import app
from styles.buttons import button_style
from styles.main_window import default_text


class TaoApp(QWidget):
    def __init__(self):
        super().__init__()


        self.drag_start_position = None
        self.default_window_geometry = (300, 200, 1280, 720)
        self.resize(self.default_window_geometry[2], self.default_window_geometry[3])
        # Инициализация медиаплеера и виджета видео
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_widget = QVideoWidget()
        self.update_coordinate_default_video_widget()

        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        self.title_window_icon = None
        self.name_header_text = None
        self.version_header_text = None

        self.close_button = None
        self.wrap_button = None
        self.maximize_button = None

        self.initialize_ui()
        self.set_window_position()

    def update_coordinate_default_video_widget(self):
        """Настройка виджета видео."""
        self.video_widget.setMinimumWidth(1280)
        self.video_widget.setMinimumHeight(525)

    def update_coordinate_maximize_video_widget(self):
        """Настройка виджета видео."""
        self.video_widget.setMinimumWidth(1920)
        self.video_widget.setMinimumHeight(885)

    def initialize_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(config.gradient.gradient_brown)  # Фон для основного виджета
        self.setWindowTitle('Tao Player')

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.create_window_control_buttons()

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



        header_layout.addLayout(inner_layout)

        return header_layout

    def create_window_control_buttons(self):
        """Создание кнопок для хедера"""
        self.wrap_button = self.create_icon_button("resources/wrap.png", self.wrap_window)
        self.maximize_button = self.create_icon_button("resources/maximize.png", self.maximize_window)
        self.close_button = self.create_icon_button("resources/close.png", self.close_window)
        self.update_position_control_buttons()

    def update_position_control_buttons(self):
        width = self.size().width()
        self.wrap_button.move(width - 40 * 3, 0)
        self.maximize_button.move(width - 40 * 2, 0)
        self.close_button.move(width - 40 * 1, 0)

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
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)

        menu_button = QPushButton()
        menu_button.setIcon(QIcon("resources/menu.png"))
        menu_button.setIconSize(QSize(32, 32))  # Устанавливаем размер иконки
        menu_button.setFixedSize(40, 40)  # Устанавливаем фиксированный размер кнопки
        menu_button.setStyleSheet(button_style)
        inner_layout.addWidget(menu_button)

        # Иконка
        self.title_window_icon = QLabel(self)
        logo_pixmap = QPixmap("logo.jpg")
        self.title_window_icon.setPixmap(logo_pixmap)
        self.title_window_icon.setStyleSheet('QLabel { background-color: transparent; }')
        self.title_window_icon.move(self.size().width() // 2 - logo_pixmap.width() // 2, 5)


        # Название плеера
        self.name_header_text = QLabel('<span style="color: white;">Tao</span> <span style="color: #9C0303;">Player</span>',
                                   self)
        self.name_header_text.setStyleSheet(default_text + "font-size: 16px; font-weight: bold;")

        # Версия плеера
        self.version_header_text = QLabel(app.version, self)
        self.version_header_text.setStyleSheet(default_text + "font-size: 14px; font-weight: regular; color: white;")

        self.update_position_header_info()
        return inner_layout

    def update_position_header_info(self):
        width = self.size().width()
        self.title_window_icon.move(width // 2, 5)
        self.name_header_text.move(int(width * 0.43), 5)
        self.version_header_text.move(int(width * 0.5365), 4)

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

    def close_window(self):
        """Закрытие окна."""
        self.close()

    def maximize_window(self):
        """Максимизация окна."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.geometry()
        if self.geometry() == screen_rect:

            self.showNormal()
            self.update_coordinate_default_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()
        else:
            # тут надо сделать перемещение элементов либо настроить на % изменение
            self.showFullScreen()
            self.update_coordinate_maximize_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()

    def wrap_window(self):
        """Сворачивание окна"""
        self.showMinimized()
