import sys
from PyQt6.QtCore import Qt, QUrl, QSize, QPoint
from PyQt6.QtGui import QPixmap, QIcon, QAction, QCursor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QApplication, QFileDialog, QHBoxLayout, QMenuBar, QToolBar, QMenu
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
        self.update_coordinate_video_widget()

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

    def update_coordinate_video_widget(self):
        """Настройка виджета видео."""
        if self.isFullScreen():
            self.video_widget.setMinimumWidth(1920)
            self.video_widget.setMinimumHeight(885)
        else:
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
        menu_button.clicked.connect(self.show_menu)

        # Логотип
        self.title_window_icon = QLabel(self)
        logo_pixmap = QPixmap("logo.jpg")
        self.title_window_icon.setPixmap(logo_pixmap)
        self.title_window_icon.setStyleSheet('QLabel { background-color: transparent; }')

        # Название плеера
        self.name_header_text = QLabel(
            '<span style="color: white;">Tao</span> <span style="color: #9C0303;">Player</span>',
            self)
        self.name_header_text.setStyleSheet(default_text + "font-size: 16px; font-weight: bold;")

        # Версия плеера
        self.version_header_text = QLabel(app.version, self)
        self.version_header_text.setStyleSheet(default_text + "font-size: 14px; font-weight: regular; color: white;")

        self.update_position_header_info()
        return inner_layout

    def show_menu(self):
        """Создание и отображение меню инструментов."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                             stop: 0 rgba(198, 110, 85, 51),  /* 20% прозрачность */
                                             stop: 1 rgba(153, 86, 67, 51));  /* 20% прозрачность */
                padding: 5px;                        
            }
            QMenu::item {
                color: white;                        
                padding: 8px 20px;                  
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.2);  
            }
            QMenu::separator {
                height: 2px;                        
                background-color: #444;             
                margin: 5px 0;                      
            }
        """)

        # Добавление действий в меню
        action_load = QAction("Загрузить", self)
        action_load.triggered.connect(self.on_load_video_button_clicked)
        menu.addAction(action_load)

        action_settings = QAction("Настройки", self)
        # action_settings.triggered.connect()
        menu.addAction(action_settings)

        action_exit = QAction("Выход", self)
        action_exit.triggered.connect(self.close)
        menu.addAction(action_exit)

        menu.exec(QPoint(self.pos().x(), self.pos().y() + 40))

    def update_position_header_info(self):
        width = self.size().width()
        if self.isFullScreen():
            self.title_window_icon.move(947, 5)
            self.name_header_text.move(855, 5)
            self.version_header_text.move(990, 4)
        else:
            self.title_window_icon.move(627, 5)
            self.name_header_text.move(535, 5)
            self.version_header_text.move(670, 4)

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
            self.update_coordinate_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()
        else:
            # тут надо сделать перемещение элементов либо настроить на % изменение
            self.showFullScreen()
            self.update_coordinate_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()

    def wrap_window(self):
        """Сворачивание окна"""
        self.showMinimized()
