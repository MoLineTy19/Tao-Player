button_style = """
QPushButton {
    background: transparent;
    outline: none;          /* Убираем контур */
    color: white;                /* Белый текст */
    border: none;               /* Убираем границу */
    padding: 10px 20px;        /* Внутренние отступы */
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