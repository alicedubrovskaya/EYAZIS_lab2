from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from bs4 import BeautifulSoup


def distance(a, b):
    n = len(a)
    m = len(b)

    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row = current_row
        current_row = [i] + [0] * n

        for j in range(1, n + 1):
            add = previous_row[j] + 1
            delete = current_row[j - 1] + 1
            change = previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def suitable_words(word, words_from_file, max_number_of_mistakes):
    result = list()
    dict_words_and_errors = {}
    for i in range(0, len(words_from_file)):
        errors=distance(word, words_from_file[i])
        if errors <= max_number_of_mistakes:
            dict_words_and_errors.update({words_from_file[i]: errors})
            result = list(dict_words_and_errors.items())
            result.sort(key=lambda i: i[1])
    return result


def read_from_html(name):
    with open(name, "r", encoding='utf-8') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, "html.parser")

        words=soup.ul.text
        words_correct=list(words.split(" "))

    return words_correct

def get_filename():
    global file_name
    file_name = fd.askopenfilename(filetypes=(("HTML files", "*.html"),))

def information():
    messagebox.askquestion("Help", "1. Ввести слово для проверки.\n"
                                   "2. Ввести максимально допустимое количество ошибок.\n"
                                   "3. Выбрать файл с корректными словами.\n"
                                   "4. Снизу отобразится список подходящих слов.", type='ok')


def do():
    listbox_resulting_words.delete(0, END)
    word = entry_words.get();
    max_number = int(entry_number.get())

    words_from_file = read_from_html(file_name)
    result = suitable_words(word, words_from_file, max_number)

    for word in result[::-1]:
        listbox_resulting_words.insert(END, word)




root = Tk()

root.title("Ошибки в словах")
root.geometry("400x300")

label_enter_words = Label(text="Введите слово")
label_enter_words.pack()

entry_words = Entry()
entry_words.pack()

label_enter_number = Label(text="Введите максимально допустимое количество ошибок")
label_enter_number.pack()

entry_number = Entry()
entry_number.pack()

button_open_file= Button(text="Открыть файл", command=get_filename)
button_open_file.pack()

button_done = Button(text="Готово", command=do)
button_done.pack()


button_help = Button(text="Помощь", command=information)
button_help.pack()

listbox_resulting_words = Listbox()
listbox_resulting_words.pack()

root.mainloop()
