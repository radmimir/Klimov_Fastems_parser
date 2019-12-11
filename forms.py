from tkinter import Frame, W, E, N, S, \
    StringVar, Entry, Button, Label, Checkbutton, \
    BooleanVar, DoubleVar
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from convert import convert_form
from os.path import abspath
from graphs import graph3d
from numpy import loadtxt, float as flt
from tools import filter3d, MAXDOUBLE, MINDOUBLE


class MyFrame(Frame):
    convert_res = ''

    def __init__(self):
        Frame.__init__(self)
        self.master.title("Profile parser")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W + E + N + S)

        # Variables
        self.file_var = StringVar(self, name='file_var')
        self.up_mirror = BooleanVar(self, False)
        self.down_mirror = BooleanVar(self, False)
        self.offset_up_x = DoubleVar(self)
        self.offset_up_y = DoubleVar(self)
        self.offset_down_x = DoubleVar(self)
        self.offset_down_y = DoubleVar(self)
        self.offset_z = DoubleVar(self)
        self.offset = [self.offset_z, self.offset_up_x, self.offset_up_y, self.offset_down_x, self.offset_down_y]
        self.convert_res = StringVar(self)
        # Filters
        self.filter_up_x = DoubleVar(self, MAXDOUBLE)
        self.filter_down_x = DoubleVar(self, MINDOUBLE)
        self.filter_up_y = DoubleVar(self, MAXDOUBLE)
        self.filter_down_y = DoubleVar(self, MINDOUBLE)
        self.filter_up_z = DoubleVar(self, MAXDOUBLE)
        self.filter_down_z = DoubleVar(self, MINDOUBLE)
        self.filter = [self.filter_down_x, self.filter_up_x, self.filter_down_y, self.filter_up_y, self.filter_down_z,
                       self.filter_up_z]

        Entry(self, width=70,
              textvariable=self.file_var).grid(row=0, column=0, sticky=W, padx=30, pady=30, columnspan=5)

        Button(self, text="Выбрать файл", command=lambda: self.load_file(self.file_var),
               width=15).grid(row=0, column=6, sticky=W, padx=20, pady=20)
        Label(self, text='Смещение Z', font='Arial 10').grid(row=1, column=0, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.offset_z).grid(row=1, column=1, sticky=W, padx=5, pady=5)

        Label(self, text='Смещение X', font='Arial 10').grid(row=1, column=2, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.offset_up_x).grid(row=2, column=2, sticky=W, padx=5, pady=5)
        Entry(self, textvariable=self.offset_down_x).grid(row=3, column=2, sticky=W, padx=5, pady=5)

        Label(self, text='Смещение Y', font='Arial 10').grid(row=1, column=3, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.offset_up_y).grid(row=2, column=3, sticky=W, padx=5, pady=5)
        Entry(self, textvariable=self.offset_down_y).grid(row=3, column=3, sticky=W, padx=5, pady=5)

        Label(self, text='UP', font='Arial 12 bold').grid(row=2, column=0, sticky=W, padx=30, pady=5)
        Checkbutton(self, text='Зеркало XZ', variable=self.up_mirror).grid(row=2, column=1, sticky=W)

        Label(self, text='DOWN', font='Arial 12 bold').grid(row=3, column=0, sticky=W, padx=30, pady=5)
        Checkbutton(self, text='Зеркало YZ', variable=self.down_mirror).grid(row=3, column=1, sticky=W)

        Button(self, text="Преобразовать",
               command=lambda: self.button_convert(self.file_var, self.up_mirror, self.down_mirror,
                                                   self.offset),
               width=15).grid(row=2, column=6, sticky=W, padx=20, pady=20)

        Button(self, text="График",
               command=lambda: self.button_graph(self.file_var, self.filter),
               width=15).grid(row=7, column=6, sticky=W, padx=20, pady=20)

        Label(self, text='Верхняя граница', font='Arial 10').grid(row=4, column=2, sticky=W, padx=5, pady=5)
        Label(self, text='Нижняя граница', font='Arial 10').grid(row=4, column=3, sticky=W, padx=5, pady=5)

        Label(self, text='Фильтр X', font='Arial 12 bold').grid(row=5, column=0, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.filter_up_x).grid(row=5, column=2, sticky=W, padx=5, pady=5)
        Entry(self, textvariable=self.filter_down_x).grid(row=5, column=3, sticky=W, padx=5, pady=5)

        Label(self, text='Фильтр Y', font='Arial 12 bold').grid(row=6, column=0, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.filter_up_y).grid(row=6, column=2, sticky=W, padx=5, pady=5)
        Entry(self, textvariable=self.filter_down_y).grid(row=6, column=3, sticky=W, padx=5, pady=5)

        Label(self, text='Фильтр Z', font='Arial 12 bold').grid(row=7, column=0, sticky=W, padx=30, pady=5)
        Entry(self, textvariable=self.filter_up_z).grid(row=7, column=2, sticky=W, padx=5, pady=5)
        Entry(self, textvariable=self.filter_down_z).grid(row=7, column=3, sticky=W, padx=5, pady=5)

    def load_file(self, file_var):
        f = askopenfilename(filetypes=(("Profile files", "*.profile"),
                                       ("All files", "*.*")), initialdir=abspath(__file__))
        if f:
            file_var.set(f)
            return self

    def button_convert(self, filevar, up_mirror, down_mirror, offset):
        filevar = filevar.get()
        up_mirror = up_mirror.get()
        down_mirror = down_mirror.get()
        offset = [i.get() for i in offset]
        res = convert_form(filevar, up_mirror, down_mirror, offset)
        if res:
            message = 'Файлы успешно записаны.'
            showinfo('Информация', message)
        else:
            message = 'Ошибка - неверный путь к файлу или формат. \nТребуется .profile - файл.'
            showerror('Ошибка', message)
            self.convert_res.set(res)

    def button_graph(self, filevar, filter, dec=10):
        filevar = filevar.get()
        filter = [i.get() for i in filter]
        if not filevar or filevar[-7:] != 'profile':
            message = 'Ошибка - неверный путь к файлу или формат. \nТребуется .profile - файл.'
            showerror('Ошибка', message)
            return 0
        up_file = filevar[:-8] + "_up.txt"
        down_file = filevar[:-8] + "_down.txt"
        up_data = loadtxt(up_file, delimiter=';', dtype=flt)
        down_data = loadtxt(down_file, delimiter=';', dtype=flt)
        up_data = filter3d(up_data, filter)
        down_data = filter3d(down_data, filter)
        x, y, z = [(up_data[:, 0][::dec], down_data[:, 0][::dec]), (up_data[:, 1][::dec], down_data[:, 1][::dec]),
                   (up_data[:, 2][::dec], down_data[:, 2][::dec])]
        graph3d(x, y, z)


if __name__ == "__main__":
    window = MyFrame().mainloop()
