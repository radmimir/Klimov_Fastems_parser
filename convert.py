from parser import *
from constants import constants as cnt

from numpy import array, append


def convert(amount_of_files=-1):  # преобразование файла и возврат в виде 6 numpy - массивов
    consts = cnt()
    dirname = os.path.dirname(__file__)
    in_dir = os.path.join(dirname, 'files\\')
    out_dir = os.path.join(dirname, 'result\\')
    out_dir = os.path.join(dirname, 'result\\')
    x_ar, y_ar, z_ar = array([]), array([]), array([])
    x_ard, y_ard, z_ard = array([]), array([]), array([])
    if os.path.exists(in_dir):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        n = len(os.listdir(in_dir))
        k = 0
        if n != 0:
            for file in os.listdir(in_dir):
                x_ar, y_ar, z_ar = array([]), array([]), array([])
                x_ard, y_ard, z_ard = array([]), array([]), array([])
                infile_name = in_dir + file
                outfile_name_up = out_dir + file[:-8] + "_up.txt"  # out_dir +
                outfile_name_down = out_dir + file[:-8] + "_down.txt"  # out_dir +
                print(k + 1, "Запись. Имя файла=", infile_name)
                k += 1
                with open(infile_name, 'r') as f:
                    inp = f.readlines()  # Входные данные
                # Запишем параметры считывания
                params = list(map(int, inp[4].split(';')))
                xpitch = params[2] / consts['PARAMS_OFFSET']  # шаг
                xstart = params[3] / consts['PARAMS_OFFSET']  # Начальное значение x
                data_cnt = params[4]  # Количество точек на срезе
                xstop = xstart + xpitch * data_cnt  # Конечный x
                n = len(inp)  # Количество строк в файле
                # Инициализация переменных
                out = []  # Выходной массив
                # Цикл по строкам
                outfile_up = open(outfile_name_up, 'w')
                outfile_down = open(outfile_name_down, 'w')
                try:
                    for i in range(consts['FILE_OFFSET'], n, 1):
                        x = xstart - consts['offset_x']
                        a = list(map(int, inp[i].split(';')[:-1]))
                        y_up = list(map(lambda t: t / consts['DOTS_OFFSET'], a[2:data_cnt + 2]))
                        y_down = list(map(lambda t: t / consts['DOTS_OFFSET'], a[data_cnt + 2:2 * data_cnt + 2]))
                        z = round(a[1] / 10 ** 3 - consts['z_offset'] - consts['offset_z'], 2)  # Позиция Энкодера
                        if z < 0:
                            continue
                        for y in y_up:
                            if y > 15:
                                continue
                            if y != consts['Y_ZERO'] / consts['DOTS_OFFSET']:
                                outstr_up = "{0};{1};{2}\n".format(x, y, z)  # форматирование строки
                                x_ar = append(x_ar, x)
                                y_ar = append(y_ar, y)
                                z_ar = append(z_ar, z)
                                outfile_up.write(outstr_up)
                                x = round(x + xpitch, 2)
                            else:
                                x = round(x + xpitch, 2)
                                continue
                        x = xstart
                        for y in y_down:
                            if y > 15:
                                continue
                            if y != consts['Y_ZERO'] / consts['DOTS_OFFSET']:
                                outstr_down = "{0};{1};{2}\n".format(x, y, z)  # форматирование строки
                                outfile_down.write(outstr_down)
                                x_ard = append(x_ard, x)  # x + 1.5)
                                y_ard = append(y_ard, y)  # -y + 19)
                                z_ard = append(z_ard, z)
                                x = round(x + xpitch, 2)
                            else:
                                x = round(x + xpitch, 2)
                                continue
                    amount_of_files -= 1
                    if amount_of_files == 0:
                        break
                except IndexError:
                    print(j)
                outfile_up.close()
                outfile_down.close()
            print("Всего", 2 * k, "файлов записано.")
        else:
            print("Папка с данными files пуста.")
    else:
        print("Папка с данными files не существует. Поместите исполняемый файл в папку files.")
    return (x_ar, x_ard), (y_ar, y_ard), (z_ar, z_ard)


def read_converted():
    consts = cnt()
    dirname = os.path.dirname(__file__)
    in_dir = os.path.join(dirname, 'result\\')
    print(in_dir)
    res = {}
    if not os.path.exists(in_dir):
        print("Error, directory /results not found")
    n = len(os.listdir(in_dir))
    k = 0
    if n != 0:
        for file in os.listdir(in_dir):
            x_ar, y_ar, z_ar = array([], dtype='float'), array([], dtype='float'), array([], dtype='float')
            x_ard, y_ard, z_ard = array([], dtype='float'), array([], dtype='float'), array([], dtype='float')
            if file[-6:-4] == 'up':
                up = 1
            else:
                up = 0
            infile_name = in_dir + file
            print(k + 1, "Чтение. Имя файла=", infile_name)
            k += 1
            with open(infile_name, 'r') as f:
                inp = ''.join(f.readlines()).splitlines()  # Входные данные
                for i in range(len(inp)):
                    inp[i] = list(map(float, (inp[i].split(sep=';'))))

            try:
                n = len(inp)
                for line in inp:
                    if up:
                        x_ar = append(x_ar, line[0])
                        y_ar = append(y_ar, line[1])
                        z_ar = append(z_ar, line[2])
                    else:
                        x_ard = append(x_ard, line[0])
                        y_ard = append(y_ard, line[1])
                        z_ard = append(z_ard, line[2])
                res[file] = (x_ar, x_ard), (y_ar, y_ard), (z_ar, z_ard)
            except IndexError:
                print(j)
        print("Всего", k, "файлов прочитано.")
    else:
        print("Папка с данными", dirname, "пуста.")
    return res


def convert_form(filename, up_mirror, down_mirror,
                 offset):  # чтение файла и преобразование координатв зависимости от зеркала,
    # смещения координат, вывод в 2 файла up,down
    # offset = [offset_z,offset_x_up,offset_y_up,offset_x_down,offset_y_down]
    if not filename or filename[-7:] != 'profile':
        return 0
    consts = cnt()
    x_ar, y_ar, z_ar = array([]), array([]), array([])
    x_ard, y_ard, z_ard = array([]), array([]), array([])
    infile_name = filename
    outfile_name_up = infile_name[:-8] + "_up.txt"  # out_dir +
    outfile_name_down = infile_name[:-8] + "_down.txt"  # out_dir +
    print("Запись. Имя файла=", infile_name)
    with open(infile_name, 'r') as f:
        inp = f.readlines()  # Входные данные
    # Запишем параметры считывания
    params = list(map(int, inp[4].split(';')))
    xpitch = params[2] / consts['PARAMS_OFFSET']  # шаг
    xstart = params[3] / consts['PARAMS_OFFSET']  # Начальное значение x
    data_cnt = params[4]  # Количество точек на срезе
    xstop = xstart + xpitch * data_cnt  # Конечный x
    n = len(inp)  # Количество строк в файле
    # Инициализация переменных
    out = []  # Выходной массив
    # Цикл по строкам
    outfile_up = open(outfile_name_up, 'w')
    outfile_down = open(outfile_name_down, 'w')
    if len(inp[6].split(';')) == 1203:
        off_firstline = 0
    elif len(inp[6].split(';')) == 1204:
        off_firstline = 1
    else:
        return 0
    try:
        for i in range(consts['FILE_OFFSET'], n, 1):
            x_up = xstart + offset[1]

            if i != 6 and off_firstline:
                off_firstline = 0
            a = list(map(int, inp[i].split(';')[off_firstline:-1]))
            y_up = list(map(lambda t: t / consts['DOTS_OFFSET'], a[2:data_cnt + 2]))
            y_down = list(map(lambda t: t / consts['DOTS_OFFSET'], a[data_cnt + 2:2 * data_cnt + 2]))
            z = round(a[1] / 10 ** 3 + offset[0], 2)  # Позиция Энкодера
            for y in y_up:
                if y != consts['Y_ZERO'] / consts['DOTS_OFFSET']:
                    if up_mirror:
                        y = -y
                    y = y + offset[2]
                    outstr_up = "{0};{1};{2}\n".format(x_up, y, z)  # форматирование строки
                    outfile_up.write(outstr_up)
                    x_ar = append(x_ar, x_up)  #
                    y_ar = append(y_ar, y)
                    z_ar = append(z_ar, z)
                    x_up = round(x_up + xpitch, 2)
                else:
                    x_up = round(x_up + xpitch, 2)
                    continue
            if down_mirror:
                x_down = -xstart + offset[3]
                xpitch_down = -xpitch
            else:
                x_down = xstart + offset[3]
                xpitch_down = xpitch
            for y in y_down:
                if y != consts['Y_ZERO'] / consts['DOTS_OFFSET']:
                    y = y + offset[4]
                    outstr_down = "{0};{1};{2}\n".format(x_down, y, z)  # форматирование строки
                    outfile_down.write(outstr_down)
                    x_ard = append(x_ard, x_down)  # x + 1.5)
                    y_ard = append(y_ard, y)  # -y + 19)
                    z_ard = append(z_ard, z)
                    x_down = round(x_down + xpitch_down, 2)
                else:
                    x_down = round(x_down + xpitch_down, 2)
                    continue
    except IndexError:
        print(j)
    outfile_up.close()
    outfile_down.close()
    return 1  # (x_ar, x_ard), (y_ar, y_ard), (z_ar, z_ard)


if __name__ == '__main__':
    offset = [0, 0, 0, 0, 0]
    res = convert_form(r'D:\Projects\Klimov_Fastems_parser\files\2.profile', False, False, offset)
    # res = read_converted()
    # print(res.keys())
    # convert(1)
