import tkinter as tk
from tkinter import simpledialog
import random


class Room:
    def __init__(self, canvas, x, y, width, height, name):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name

        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF)) #генерируем рандомный цвет для комнаты

        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill=random_color, tags="room")
        self.text = canvas.create_text(x + width / 2, y + height / 2,
                                       text=f"{name}\n{width}x{height}\nПлощадь: {width * height}", tags="room_text")

        #drag & drop
        self.canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.rect, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y

    def on_drag(self, event):
        new_x = event.x - self.offset_x
        new_y = event.y - self.offset_y
        self.canvas.coords(self.rect, new_x, new_y, new_x + self.width, new_y + self.height)
        self.canvas.coords(self.text, new_x + self.width / 2, new_y + self.height / 2)

    def on_release(self, event):
        pass


class Apartment: #квартира
    def __init__(self, canvas, x, y, width, height, name):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.outer_rect = canvas.create_rectangle(x, y, x + width, y + height, outline="gray", width=2) #границы квартиры
        #площадь и название квартиры
        area = width * height
        self.text = canvas.create_text(x + width / 2, y - 20, text=f"{name} (Площадь: {area})", font=("Arial", 14),
                                       fill="black")


class ApartmentPlanner: #модальное окно
    def __init__(self, master):
        self.master = master
        master.title("Архитектурный планировщик")

        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack()

        self.create_apartment_button = tk.Button(master, text="Создать квартиру", command=self.create_apartment)
        self.create_apartment_button.pack()

        self.create_room_button = tk.Button(master, text="Создать комнату", command=self.create_room)
        self.create_room_button.pack()

        #изначально false, т.к. еще не создана квартира (флаг)
        self.apartment_created = False

    def create_apartment(self): #создание квартиры
        if not self.apartment_created:
            name = simpledialog.askstring("Имя квартиры", "Введите имя квартиры:")
            width = simpledialog.askinteger("Размеры квартиры", "Введите ширину квартиры:")
            height = simpledialog.askinteger("Размеры квартиры", "Введите высоту квартиры:")

            if name and width and height:
                Apartment(self.canvas, 50, 50, width, height, name) #создаем новую квартиру
                self.apartment_created = True #флаг в true, после создания
                self.create_apartment_button.pack_forget() #скрыли кнопку

    def create_room(self): #создание комнаты
        name = simpledialog.askstring("Имя комнаты", "Введите имя комнаты:")
        width = simpledialog.askinteger("Размеры комнаты", "Введите ширину комнаты:")
        height = simpledialog.askinteger("Размеры комнаты", "Введите высоту комнаты:")

        if name and width and height:
            Room(self.canvas, 50, 50, width, height, name) #создаем новую комнату


if __name__ == "__main__":
    root = tk.Tk()
    app = ApartmentPlanner(root)
    root.mainloop()