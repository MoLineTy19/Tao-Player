import sys
from PyQt6.QtCore import Qt, QUrl, QSize, QPoint
from PyQt6.QtGui import QPixmap, QIcon, QAction, QCursor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSizePolicy, QApplication, QFileDialog, QHBoxLayout, QMenuBar, QToolBar, QMenu, QSlider
)
import config.gradient
import styles.menu
from config import app
from styles.buttons import style_control_button, style_action_button, style_mini_act_button
from styles.main_window import default_text
from styles.slider import style_volume_slider


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
        layout.addWidget(self.create_control_menu())

        self.setLayout(layout)

    def set_window_position(self):
        """Установка позиции окна на экране."""
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        if screen_rect.width() >= 1920:
            self.setGeometry(*self.default_window_geometry)

    def create_control_menu(self):
        """Создание меню управления."""

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(0)

        self.action_video = QPushButton()
        self.action_video.setIcon(QIcon("resources/pause.png"))
        self.action_video.setIconSize(QSize(65, 65))
        self.action_video.setStyleSheet(style_action_button)
        self.action_video.clicked.connect(self.play_video)

        fast_forward = QPushButton()
        fast_forward.setIcon(QIcon("resources/fast_forward.png"))
        fast_forward.setIconSize(QSize(35, 35))
        fast_forward.setStyleSheet(style_mini_act_button)
        # fast_forward.clicked.connect(self.fast_forward)

        go_back = QPushButton()
        go_back.setIcon(QIcon("resources/go_back.png"))
        go_back.setIconSize(QSize(35, 35))
        go_back.setStyleSheet(style_mini_act_button)

        next_episode = QPushButton()
        next_episode.setIcon(QIcon("resources/next_episode.png"))
        next_episode.setIconSize(QSize(35, 35))
        next_episode.setStyleSheet(style_mini_act_button)

        last_episode = QPushButton()
        last_episode.setIcon(QIcon("resources/last_episode.png"))
        last_episode.setIconSize(QSize(35, 35))
        last_episode.setStyleSheet(style_mini_act_button)

        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        volume_slider.setStyleSheet(style_volume_slider)
        # volume_slider.valueChanged.connect(self.change_volume)

        label = QLabel()
        label.setText('One piece - 1 episode\n'
                      'One piece - 1 episode\n'
                      'One piece - 1 episode')
        label.setStyleSheet(default_text + "font-size: 18px; font-weight: bold; color: white;")

        maximize = QPushButton()
        maximize.setIcon(QIcon("resources/maximize_black.png"))
        maximize.setIconSize(QSize(35, 35))
        maximize.setStyleSheet(style_mini_act_button)

        control_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignRight, stretch=15)
        control_layout.addWidget(last_episode, alignment=Qt.AlignmentFlag.AlignRight, stretch=15)
        control_layout.addWidget(go_back, alignment=Qt.AlignmentFlag.AlignRight, stretch=4)
        control_layout.addWidget(self.action_video, alignment=Qt.AlignmentFlag.AlignCenter, stretch=7)
        control_layout.addWidget(fast_forward, alignment=Qt.AlignmentFlag.AlignLeft, stretch=4)
        control_layout.addWidget(next_episode, alignment=Qt.AlignmentFlag.AlignLeft, stretch=18)
        control_layout.addWidget(volume_slider, alignment=Qt.AlignmentFlag.AlignLeft, stretch=10)
        control_layout.addWidget(maximize, alignment=Qt.AlignmentFlag.AlignLeft, stretch=5)

        # Создаем виджет и устанавливаем в него layout
        control_widget = QWidget()
        control_widget.setLayout(control_layout)




        return control_widget  # Возвращаем виджет, а не layout
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
        """Позиционирование кнопок для хедера"""
        width = self.size().width()
        self.wrap_button.move(width - 40 * 3, 0)
        self.maximize_button.move(width - 40 * 2, 0)
        self.close_button.move(width - 40 * 1, 0)

    def create_icon_button(self, icon_path, action=None):
        """Генератор кнопок для хедера"""
        button = QPushButton(self)
        button.setStyleSheet(style_control_button)
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
        menu_button.setStyleSheet(style_control_button)
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
        menu.setStyleSheet(styles.menu.menu)

        # Добавление действий в меню
        action_load = QAction("Загрузить", self)
        action_load.triggered.connect(self.on_load_video_button_clicked)
        menu.addAction(action_load)

        action_settings = QAction("Настройки", self)
        # action_settings.triggered.connect()
        menu.addAction(action_settings)

        action_donate = QAction("Донат", self)
        action_donate.triggered.connect(self.close)
        menu.addAction(action_donate)

        menu.exec(QPoint(self.pos().x(), self.pos().y() + 40))

    def update_position_header_info(self):
        """Позиционирование хедера."""

        # Если окно в полноэкранном режиме
        if self.isFullScreen():
            self.title_window_icon.move(947, 5)
            self.name_header_text.move(855, 5)
            self.version_header_text.move(990, 4)
        else:
            # Если окно в оконном режиме
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

        # Минимизация окна
        if self.geometry() == screen_rect:
            self.showNormal()
            self.update_coordinate_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()
        else:
            # Максимизация окна
            self.showFullScreen()
            self.update_coordinate_video_widget()
            self.update_position_control_buttons()
            self.update_position_header_info()

    def wrap_window(self):
        """Сворачивание окна"""
        self.showMinimized()

    def play_video(self):
        """Воспроизведение видео."""
        if self.media_player.playbackState() == QMediaPlayer.playbackState(self.media_player).PlayingState:
            self.media_player.pause()
            self.action_video.setIcon(QIcon("resources/play.png"))


        else:
            if self.media_player.mediaStatus() == self.media_player.MediaStatus.BufferedMedia:
                self.media_player.play()
                self.action_video.setIcon(QIcon("resources/pause.png"))

