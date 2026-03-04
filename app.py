from datetime import datetime

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QListWidget, QTextEdit, \
    QPushButton, QInputDialog, QLineEdit
from PySide6.QtCore import Qt


from api import colors, get_all_tasks, Task



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoList")
        self.setWindowIcon(QIcon(r"C:\Users\Supa\Desktop\Apprentissage_DEV\PYTHON\projets\ToDoList_App\todolist.ico"))
        # self.setFixedSize(QSize(800, 600))
        self.setStyleSheet("background-color:rgb(40, 40, 40); color:white")

        #ajout d'un widget central dans lequel on ajotuera le layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setup_ui()
        self.set_default_values()
        self.setup_connections()




    def setup_ui(self):
        #ajout du layout dans le widget central
        self.main_layout = QGridLayout(self.central_widget)

        #Création des widgets + ajout dans le layout
        self.title_label = QLabel()

        self.add_task_btn = QPushButton("Ajouter")

        self.tasks_list = QListWidget()

        self.task_name = QLineEdit()

        self.task_color_btn = QPushButton("Couleur")

        self.last_modification = QLabel()

        self.modification_date = QLabel()

        self.task_content = QTextEdit()

        self.save_content_btn = QPushButton("Sauvegarder")

        self.delete_task_btn = QPushButton("Supprimer")

        #Ajout des Widgets au layout :
        self.main_layout.addWidget(self.title_label, 0, 0, 1, 3, Qt.AlignCenter)
        self.main_layout.addWidget(self.add_task_btn, 1, 0, 1, 1)
        self.main_layout.addWidget(self.tasks_list, 2, 0, 2, 1)
        self.main_layout.addWidget(self.task_name, 1, 1, 1, 2, Qt.AlignCenter)
        self.main_layout.addWidget(self.task_color_btn, 1, 3)
        self.main_layout.addWidget(self.last_modification, 2, 1)
        self.main_layout.addWidget(self.modification_date, 2, 3, Qt.AlignRight)
        self.main_layout.addWidget(self.task_content, 3, 1, 1, 3)
        self.main_layout.addWidget(self.save_content_btn, 4, 3)
        self.main_layout.addWidget(self.delete_task_btn, 4, 0)


        #gestion des style des Widgets :
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.tasks_list.setStyleSheet("font-size: 14px; ")
        self.task_name.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.last_modification.setStyleSheet("font-size: 12px; font-style: italic; ")
        self.modification_date.setStyleSheet("font-size: 12px; font-style: italic; ")
        self.task_content.setStyleSheet("font-size: 14px; ")


        # ajouter des dimensions max et mini pour certains widgets :
        # .setMinimumWidth()
        # .setMaximumWidth()
        # .setMinimumHeight()
        # .setMaximumHeight()

        # gestion des dimensions des rows et cols
        self.main_layout.setColumnStretch(0, 1)  # Colonne de gauche
        self.main_layout.setColumnStretch(1, 3)  # Colonne centrale
        self.main_layout.setColumnStretch(2, 1)  # Colonne de droite

        self.main_layout.setRowStretch(0, 1)  # Ligne du titre
        self.main_layout.setRowStretch(1, 1)  # Ligne principale
        self.main_layout.setRowStretch(2, 1)  # Ligne bas
        self.main_layout.setRowStretch(3, 6)  # Contenu


        #ajouter des espacements :
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # marges autour du layout
        self.main_layout.setHorizontalSpacing(5)  # espace horizontal entre cellules
        self.main_layout.setVerticalSpacing(5)  # espace vertical entre cellules


    def set_default_values(self):

        self.tasks_list.clear()
        self.title_label.setText("ToDoList")
        self.tasks_list.addItems(self.get_tasks_list_name())


        # Sélectionner la première tâche si la liste n'est pas vide
        if self.tasks_list.count() > 0:
            self.tasks_list.setCurrentRow(0)
            self.display_selected_task()  # afficher ses infos

        else :
            self.task_content.setText("Ajouter une nouvelle tache")




    #récuperer la liste des tache task.name et l'afficher dans tasks_list
    @staticmethod
    def get_tasks_list_name():
        tasks = get_all_tasks()
        tasks_names = []
        for task in tasks:
            tasks_names.append(task.name)
        return tasks_names


    def setup_connections(self):
        self.tasks_list.currentItemChanged.connect(self.display_selected_task)
        self.task_color_btn.clicked.connect(self.choose_color)
        self.task_name.editingFinished.connect(self.rename_task)
        self.add_task_btn.clicked.connect(self.add_task)
        self.save_content_btn.clicked.connect(self.modify_content)
        self.delete_task_btn.clicked.connect(self.delete_task)


    # ajouter une tache -> créer une tache vide
    def add_task(self):
        new_name = "Nouvelle tâche"
        if not new_name in self.get_tasks_list_name():
            t=Task(new_name)
            t.create_task()
            self.tasks_list.addItem(new_name)

            #permet de selectionner la derniere tache
            self.tasks_list.setCurrentRow(self.tasks_list.count() - 1)

            self.display_selected_task()


    # selectionner une tache et l'afficher
    def display_selected_task(self):
        selected_task = self.tasks_list.currentItem().text()
        t = Task.load_task(selected_task)
        if t:
            self.task_name.setText(t.name)
            self.task_content.setText(t.content)
            self.modification_date.setText(t.date)

            #gestion temps
            last_modif = datetime.strptime(t.date, "%d/%m/%Y %H:%M")
            current_time = datetime.now()
            delta = current_time - last_modif
            self.last_modification.setText(f"Il y a {delta.days} jours, {delta.seconds//3600} heures, {delta.seconds//60 - (60*(delta.seconds//3600))} minutes.")

            #gestion couleur
            self.task_name.setStyleSheet(
                f"background-color: {t.color['hex_name']}; "
                f"color: {t.color['color_text']}; "
                "font-size: 16px; font-weight: bold;"
            )
            self.task_content.setStyleSheet(
                f"background-color: {t.color['hex_name']}; "
                f"color: {t.color['color_text']}; "
                "font-size: 14px;"
            )
            self.task_name.setAlignment(Qt.AlignCenter)

            self.task_color_btn.setStyleSheet(
                f"background-color: {t.color['hex_name']}; "
                f"color: {t.color['color_text']}; "
            )


    def rename_task(self):
        #on récupère l'item actuel, pour pouvoir le renommer avec le nouveau nom
        current_item = self.tasks_list.currentItem()

        #on recupere le text de l'item actuel
        selected_task = self.tasks_list.currentItem().text()

        #on créer une isntance qui correpsond exactement à ce qu'il y a dans tiny db via la methode de classe
        t = Task.load_task(selected_task)
        if t:
            t.update_name(self.task_name.text())

        #on renomme l'item actuel avec le nouveau nom
        current_item.setText(self.task_name.text())

        self.display_selected_task()


    def modify_content(self):
        #on recupere le text de l'item actuel
        selected_task = self.tasks_list.currentItem().text()

        #on créer une isntance qui correpsond exactement à ce qu'il y a dans tiny db via la methode de classe
        t = Task.load_task(selected_task)
        if t:
            t.update_content(self.task_content.toPlainText())

        self.display_selected_task()


    def choose_color(self):
        # afficher une liste déroulante avec les couleurs disponibles
        color_name, ok = QInputDialog.getItem(
            self,
            "Choisir une couleur",
            "Sélectionne une couleur :",
            colors,  # liste importée depuis api.py
            editable=False
        )
        if ok and color_name:
            #affilier la couleur à la tâche en cours
            selected_task = self.tasks_list.currentItem().text()
            # on créer une isntance qui correpsond exactement à ce qu'il y a dans tiny db via la methode de classe
            t = Task.load_task(selected_task)
            if t:
                t.update_color(color_name)
            self.display_selected_task()


    def delete_task(self):
        selected_task = self.tasks_list.currentItem().text()

        # on créer une instance qui correpsond exactement à ce qu'il y a dans tiny db via la methode de classe
        t = Task.load_task(selected_task)
        if t:
            t.remove_task()

        # déconnecter le signal temporairement
        self.tasks_list.currentItemChanged.disconnect(self.display_selected_task)
        self.tasks_list.clear()
        self.set_default_values()
        # reconnecter le signal
        self.tasks_list.currentItemChanged.connect(self.display_selected_task)




app = QApplication([])
window = App()
window.show()
app.exec()


if __name__ == "__main__":
    pass