menu = """
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
        """