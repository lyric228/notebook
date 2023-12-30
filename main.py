from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QListWidget, QLineEdit, QInputDialog, QMessageBox
import json
#ЫАРШПЫАРШЩДГПШЫАшщргЫАргшыапшгфгшафшоафдроларолфарлофаорл

app = QApplication([])
window = QWidget()
window.resize(1000, 600)


class UltraQMessageBobux(QMessageBox):
    def __init__(self):
        super().__init__()
        self.signal = False
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.buttonClicked.connect(self.next)

    def next(self, button):
        button = self.standardButton(button)
        if button == QMessageBox.StandardButton.Ok:
            self.signal = True
        elif button == QMessageBox.StandardButton.Cancel:
            self.signal = False


def save_files():
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file)


def load_files():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            load = json.load(file)
            return load
    except FileNotFoundError:
        return {}


def refresh(notes):
    notes_list.clear()
    edit_text.clear()
    tags_list.clear()
    notes_list.addItems(notes)
    for note_name in notes:
        tags_list.addItems(notes[note_name]['теги'])



def add_note():
    note_name, ok = QInputDialog.getText(window, "Добавить заметку", "Текст заметки")
    if ok and note_name != "":
        notes[note_name] = {"текст": "",
                            "теги": []
                            }
        refresh(notes)
        save_files()


def delete_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        refresh(notes)
        save_files()


def save_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        notes[key]['текст'] = edit_text.toPlainText()
        save_files()


def show_note():
    key = notes_list.selectedItems()[0].text()
    edit_text.setText(notes[key]['текст'])


def add_tag():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        tag_name, ok = QInputDialog.getText(window, "Добавить тег", "Тег")
        if ok and tag_name != "":
            if tag_name not in notes[note_name]['теги']:
                notes[note_name]['теги'].append(tag_name)
                refresh(notes)
                save_files()
    else:
        message_box.setText("Заметка не выбрана!")
        message_box.exec()


def delete_tag():
    if notes_list.selectedItems() and tags_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        tag_name = tags_list.selectedItems()[0].text()
        if tag_name in notes[note_name]['теги']:
            notes[note_name]['теги'].remove(tag_name)
            refresh(notes)
            save_files()


def search_tag():
    tag_name = tag_input.text()
    search_result = {}
    for note_name in notes:
        for tag in notes[note_name]['теги']:
            if tag_name in tag:
                search_result[note_name] = notes[note_name]
    refresh(search_result)


def clear_memory():
    yes_message_box = UltraQMessageBobux()
    yes_message_box.setText("Вы ТОЧНО уверены? (оно удалит все заметки навсегда!)")
    yes_message_box.exec()
    if yes_message_box.signal:
        notes.clear()
        refresh(notes)
        save_files()


'''
notes = {
    "имя заметки": {
        "текст": "текст замтеки"
        "теги": [тег1, тег2]
        }
    }
'''

vline = QVBoxLayout()
main_hline = QHBoxLayout()
edit_text = QTextEdit()
label_notes = QLabel('Список заметок')
label_tags = QLabel('Список тегов')
notes_list = QListWidget()
hline_notes = QHBoxLayout()
add_note_button = QPushButton('Создать заметку')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметку')
hline_tags = QHBoxLayout()
tag_input = QLineEdit()
tag_input.setPlaceholderText("Введите тег:")
add_tag_button = QPushButton('Добавить тег')
delete_tag_button = QPushButton('Удалить тег')
delete_all_memory = QPushButton('Удалить данные')
tags_list = QListWidget()
message_box = QMessageBox()


window.setLayout(main_hline)
main_hline.addWidget(edit_text)
main_hline.addLayout(vline)
vline.addWidget(label_notes)
vline.addWidget(notes_list)
vline.addLayout(hline_notes)
hline_notes.addWidget(add_note_button)
hline_notes.addWidget(delete_note_button)
vline.addWidget(save_note_button)
vline.addWidget(label_tags)
vline.addWidget(tags_list)
vline.addWidget(tag_input)
vline.addLayout(hline_tags)
vline.addWidget(delete_all_memory)
hline_tags.addWidget(add_tag_button)
hline_tags.addWidget(delete_tag_button)
add_note_button.clicked.connect(add_note)
delete_note_button.clicked.connect(delete_note)
save_note_button.clicked.connect(save_note)
notes_list.itemClicked.connect(show_note)
add_tag_button.clicked.connect(add_tag)
delete_tag_button.clicked.connect(delete_tag)
tag_input.textChanged.connect(search_tag)
delete_all_memory.clicked.connect(clear_memory)
notes = load_files()
refresh(notes)


window.show()
app.exec()
