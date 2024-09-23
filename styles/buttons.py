style_control_button = """
QPushButton {
    background: transparent;
    outline: none;          /* Убираем контур */
    color: white;                /* Белый текст */
    border: none;               /* Убираем границу */
    padding: 0;                /* Убираем внутренние отступы */
    font-size: 16px;           /* Размер шрифта */
    font-weight: bold;         /* Жирный шрифт */
    transition: background 0.3s, transform 0.2s; /* Плавный переход фона и эффекта нажатия */
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Тень кнопки */
}

QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                stop: 0 rgba(170, 90, 70, 255), 
                                stop: 1 rgba(130, 60, 50, 255));  /* Более темный градиент при наведении */
    transform: scale(1.05); /* Увеличение кнопки при наведении */
}

QPushButton:pressed {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                stop: 0 rgba(150, 80, 60, 255), 
                                stop: 1 rgba(120, 50, 40, 255));  /* Темный градиент при нажатии */
    transform: scale(0.95); /* Уменьшение кнопки при нажатии */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3); /* Уменьшение тени при нажатии */
}
"""

style_action_button = """
    QPushButton {
        background: white;                  /* Фоновый цвет */
        border-radius: 32px;                /* Закругление углов кнопки */
        transition: background-color 0.3s, color 0.3s; /* Плавный переход */
    }
    QPushButton:hover {
        background: #F0E0D0;                /* Цвет фона при наведении */
        color: #A35B45;                     /* Цвет текста при наведении */
    }
    QPushButton:pressed {
        background: #D8CFC0;                /* Цвет фона при нажатии */
        color: #7A4A3A;                     /* Цвет текста при нажатии */
    }
"""

style_mini_act_button = """
    QPushButton {
        background: white;                  /* Фоновый цвет */
        width: 47px;                         /* Ширина кнопки */
        height: 47px;                        /* Высота кнопки */
        border-radius: 22px;                /* Закругление углов кнопки */
        transition: background-color 0.3s, color 0.3s; /* Плавный переход */
    }
    QPushButton:hover {
        background: #F0E0D0;                /* Цвет фона при наведении */
        color: #A35B45;                     /* Цвет текста при наведении */
    }
    QPushButton:pressed {
        background: #D8CFC0;                /* Цвет фона при нажатии */
        color: #7A4A3A;                     /* Цвет текста при нажатии */
    }
"""