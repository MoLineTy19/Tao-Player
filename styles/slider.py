style_volume_slider = """
QSlider {
    background: #E5A795;
    height: 10px;
    border-radius: 5px;
}

QSlider::handle {
    background: white;
    border: 2px solid #E5A795;
    width: 20px;
    height: 20px;
    border-radius: 10px;
    margin: -5px 0; /* Центрируем ручку по вертикали */
}

QSlider::groove:horizontal {
    background: #E5A795;
    height: 10px;
    border-radius: 5px;
}

QSlider::sub-page:horizontal {
    background: #CFAE9A; /* Более тёмный оттенок для заполненной области */
    border-radius: 5px;
}

QSlider::add-page:horizontal {
    background: #E5A795; /* Цвет для незаполненной области */
    border-radius: 5px;
}
"""