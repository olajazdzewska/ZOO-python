




from PySide6.QtWidgets import QApplication, QWidgetAction, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, \
    QDialog, QVBoxLayout, QGridLayout, QTextEdit, QScrollArea, QMenu
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, QEvent
from World import World
from Organism import specie_enum

BUTTON_GRID = [[]]


class Window(QWidget):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent = parent)
        # QWidget.__init__(self, *args, **kwargs)
        self.setGeometry(100, 10, 1200, 800)

        self.main_layout = QVBoxLayout()
        self.main_layout.setStretch(0, 3)
        self.grid_layout = QGridLayout()
        self.button_grid_init()
        self.button_game_layout = QHBoxLayout()
        self.button_game_layout.setStretch(0, 3)
        self.menu_bar_init()
        self.main_layout.addLayout(self.grid_layout, stretch=1)
        self.setLayout(self.main_layout)
        self.can_move = True
        self.world = World(15, 15)
        self.eventFilter = key_press_filter(parent=self)
        self.installEventFilter(self.eventFilter)
        self.comment_label = ScrollLabel()
        #self.comment_label.setText("hi")
        self.main_layout.addWidget(self.comment_label)

    def on_click(self):
        print("wrr")

    def button_grid_init(self):
        for i in range(0, 15):
            for j in range(0, 15):
                tmp = QPushButton()
                tmp.resize(10, 10)
                self.grid_layout.addWidget(tmp, i, j)
                BUTTON_GRID[i].append(tmp)
                BUTTON_GRID[i][j].clicked.connect(self.on_click)
            BUTTON_GRID.append([])

    def new_game(self):
        # Comment.clear_comment()
        self.world.organism_arr.clear()
        self.world.human_arr.clear()
        self.world.null_grid()
        self.world.create_organisms()
        self.world.collect_org_from_grid()
        self.world.collect_human()
        self.world.is_human_alive = True
        self.refresh_grid()

    def save_game(self):
        self.world.save()

    def load_game(self):
        self.world = self.world.load()
        self.world.organism_arr.clear()
        self.world.human_arr.clear()
        # self.world.null_grid()
        self.world.collect_org_from_grid()
        self.world.collect_human()

        # if self.world.is_human_alive and self.world.prev_human_strength != self.world.human_arr[0].strength:
        #     self.world.SA_is_activated = True
        #     self.world.humanSA = True

        self.refresh_grid()

    def refresh_comment(self):
        text = "Aleksandra Jazdzewska \n w,s,a,d - human's moves \n p - special ability \n t - next turn \n"
        for item in self.world.comment_list:
            text += item + "\n"
        self.world.comment_list = []
        self.comment_label.setText(text)

    def refresh_grid(self):
        for i in range(self.world.height):
            for j in range(self.world.width):
                if self.world.grid[i][j] is None:
                    BUTTON_GRID[i][j].setText(" ")
                else:
                    tmp_text = specie_enum[self.world.grid[i][j].specie_enum]
                    BUTTON_GRID[i][j].setText(tmp_text)
        self.refresh_comment()

    def do_human_action(self, dir):
        self.world.human_arr[0].check_action(dir)
        self.world.human_arr[0].action()
        self.refresh_grid()
        # self.can_move = False

    def menu_bar_init(self):
        new_game_button = QPushButton("new game")
        save_button = QPushButton("save")
        load_button = QPushButton("load")
        # action
        new_game_button.clicked.connect(self.new_game)  # usunelam nawiasy
        save_button.clicked.connect(self.save_game)
        load_button.clicked.connect(self.load_game)
        self.button_game_layout.addWidget(new_game_button)
        self.button_game_layout.addWidget(save_button)
        self.button_game_layout.addWidget(load_button)
        self.main_layout.addLayout(self.button_game_layout)



class key_press_filter(QObject):

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress:
            text = event.text()
            if event.modifiers():
                text = event.keyCombination().key().name.decode(encoding = "utf-8")
            if text == 't':
                print(text)
                # widget.world.create_organisms()
                widget.world.make_turn()
                widget.refresh_grid()
            elif text == 'w' and widget.world.is_human_alive:
                dir = 'up'
                widget.do_human_action(dir)
                print(text)
            elif text == 's' and widget.world.is_human_alive:
                dir = 'down'
                widget.do_human_action(dir)
                print(text)
            elif text == 'a' and widget.world.is_human_alive:
                dir = 'left'
                widget.do_human_action(dir)
                print(text)
            elif text == 'd' and widget.world.is_human_alive:
                dir = 'right'
                widget.do_human_action(dir)
                print(text)
            elif text == 'p' and widget.world.is_human_alive:
                if widget.world.SA_can_be_activated and widget.world.SA_is_activated == False:
                    if widget.world.human_arr[0].strength < 10:
                        widget.world.prev_human_strength = widget.world.human_arr[0].strength
                        widget.world.humanSA = True
                        widget.world.human_arr[0].special_ability()
                        widget.world.comment_list.append("human's special ability activated")
                    else:
                        widget.world.comment_list.append("human's strength is greater than 10")
                elif widget.world.SA_is_activated:
                    widget.world.comment_list.append("special ability is already activated")
                else:
                    widget.world.comment_list.append("you need to wait until human's cooldown end to use special"
                                                     " ability again")
                widget.refresh_grid()


            else:
                pass
        return False

class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)


app = QApplication([])
label2 = ScrollLabel()
scroll = QScrollArea()
scroll.setWidgetResizable(True)
scroll.setFixedHeight(100)
scroll.setFixedWidth(300)

window = Window()
window.show()
app.exec()










