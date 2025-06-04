import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sys
import os
import sqlite3

# Добавляем путь к модулю с функциями базы данных
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mod2'))
from database_operations import (
    init_database, get_user, update_user, add_user,
    get_vehicles_info, update_vehicle_status, calculate_vehicle_usage
)

class UserStatusForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Автопарк - Статус пользователя")
        self.root.geometry("800x600")
        
        # Создаем фрейм для таблицы
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создаем таблицу
        columns = ('Номер', 'Модель', 'Категория', 'Статус', 'Часы использования')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=10)

        # Настраиваем заголовки
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем элементы
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Загружаем данные
        self.load_vehicles_data()

        # Фрейм для кнопок
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Кнопка обновления
        tk.Button(button_frame, text="Обновить список", command=self.load_vehicles_data).pack(side='left', padx=5)

        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_vehicles_data(self):
        try:
            # Очищаем таблицу
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Загружаем новые данные
            vehicles_data = get_vehicles_info()
            if vehicles_data:
                for vehicle in vehicles_data:
                    self.tree.insert('', 'end', values=vehicle[1:])
            else:
                messagebox.showinfo("Информация", "Нет доступных автомобилей")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

if __name__ == "__main__":
    # Инициализируем базу данных при запуске
    init_database()
    
    root = tk.Tk()
    app = UserStatusForm(root)
    root.mainloop() 