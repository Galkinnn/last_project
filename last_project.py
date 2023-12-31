# импорт всех используемых библиотек
import tkinter as tk
from tkinter import ttk
import sqlite3

# класс основного окна
class Main(tk.Frame):
    # обязательный метод без него ничего работать не будет
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # функция для поиска
    def search_record(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            """SELECT * FROM db WHERE name LIKE ?""", name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row)
        for row in self.db.c.fetchall()]

    # открывает окно поиска
    def open_search_dialog(self):
        Search()

    # удаляет записи
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("""DELETE FROM db WHERE
            id=?""", (self.tree.set(selection_item, '#1'),))
            self.db.connect.commit()
            self.view_records()

    # редактирует записи
    def upadate_record(self, name, tel, email, zp):
        self.db.c.execute("UPDATE db SET name=?, tel=?, email=?, zp=? WHERE ID=?", (name, tel, email, zp, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.connect.commit()
        self.view_records()

    # открывает окно редактирования
    def open_update_dialog(self):
        Update()

    # функция, которая вытягиевает записи из базы данных
    def view_records(self):
        self.db.c.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row)
         for row in self.db.c.fetchall()]

    # функция, которая выводит все записи
    def records(self, name, tel, email, zp):
        self.db.insert_data(name, tel, email, zp)
        self.view_records()

    # функция, открывающая окно добавления записи
    def open_dialog(self):
        Child()

    # тут кароче прописаны кнопки (в основном окне), заголовки таблицы с записями и где они находятся
    def init_main(self):
        toolbar = tk.Frame(bg = '#d7d8e0', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)

        self.add_img = tk.PhotoImage(file = './img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.add_img, command = self.open_dialog)
        btn_open_dialog.pack(side = tk.LEFT)

        self.tree = ttk.Treeview(self, columns = ('ID', 'name', 'tel', 'email', 'zp'), height = 45, show = 'headings')

        self.tree.column('ID', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 200, anchor = tk.CENTER)
        self.tree.column('tel', width = 150, anchor = tk.CENTER)
        self.tree.column('email', width = 150, anchor = tk.CENTER)
        self.tree.column('zp', width = 150, anchor = tk.CENTER)

        self.tree.heading('ID', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('tel', text = 'Телефон')
        self.tree.heading('email', text = 'E-mail')
        self.tree.heading('zp', text = 'Зарплата')

        self.tree.pack(side = tk.LEFT)

        self.update_img = tk.PhotoImage(file = './img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.update_img, command = self.open_update_dialog)
        btn_edit_dialog.pack(side = tk.LEFT)

        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        btn_delete = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.delete_img, command = self.delete_records)
        btn_delete.pack(side = tk.LEFT)

        self.search_img = tk.PhotoImage(file = './img/search.png')
        btn_search = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.search_img, command = self.open_search_dialog)
        btn_search.pack(side = tk.LEFT)

        self.refresh_img = tk.PhotoImage(file = './img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.refresh_img, command = self.view_records)
        btn_refresh.pack(side = tk.LEFT)

# класс добавления записи
class Child(tk.Toplevel):
    # (х2) обязательный метод без него ничего работать не будет
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # тут описаны все кнопки и тп в окне добавить
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x = 50, y = 50)
        label_tel = tk.Label(self, text = 'Телефон')
        label_tel.place(x = 50, y = 80)
        label_email = tk.Label(self, text = 'E-mail')
        label_email.place(x = 50, y = 110)
        label_zp = tk.Label(self, text = 'Зарпалата')
        label_zp.place(x = 50, y = 140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x = 200, y = 80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 110)
        self.entry_zp = ttk.Entry(self)
        self.entry_zp.place(x = 200, y = 140)

        self.btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.btn_cancel.place(x = 300, y = 170)
        self.btn_ok = ttk.Button(self, text = 'Добавить')
        self.btn_ok.place(x = 220, y = 170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_tel.get(),
                                           self.entry_email.get(),
                                           self.entry_zp.get()))
        
# класс редактирования записей
class Update(Child):
    # (х3) обязательный метод без него ничего работать не будет
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # окно редактирования
    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = tk.Button(self, text = 'Редактировать')
        btn_edit.place(x = 205, y = 170)
        btn_edit.bind('<Button-1>', lambda event:
                         self.view.upadate_record(self.entry_name.get(),
                                                self.entry_tel.get(),
                                                self.entry_email.get(),
                                                self.entry_zp.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add = '+')
        self.btn_ok.destroy()

    # для более удобного редактирования показывает исходные данные при редатипровании
    def default_data(self):
        self.db.c.execute("""SELECT * FROM db WHERE id=?""", (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_zp.insert(0, row[4])

# класс поиска
class Search(tk.Toplevel):
    # (х4) обязательный метод без него ничего работать не будет
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # расположение надписей и кнопок в окне поиска
    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text = 'Поиск')
        label_search.place(x = 50, y = 20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 105, y = 20, width = 150)
        
        btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        btn_cancel.place(x = 185, y = 50)

        btn_search = ttk.Button(self, text = 'Поиск')
        btn_search.place(x = 105, y = 50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_record(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add = '+')

# класс базы данных
class DB:
    # (х5) обязательный метод без него ничего работать не будет
    def __init__(self):
        self.connect = sqlite3.connect('DB.db')
        self.c = self.connect.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db(
                id INTEGER PRIMARY KEY,
                name TEXT, 
                tel TEXT,
                email TEXT, 
                zp TEXT);
        """)
        self.connect.commit()

    # соранение данных в дб
    def insert_data(self, name, tel, email, zp):
        self.c.execute("""INSERT INTO db(name, tel, email, zp) 
                VALUES(?, ?, ?, ?)""", (name, tel, email, zp))
        self.connect.commit()

# тут реализована подпись, указана дб и без этого всего код работать не будет
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
