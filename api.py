# ToDoList
import logging
from pathlib import Path
from datetime import datetime




from tinydb import TinyDB, where, Query

logging.basicConfig(level=logging.INFO)

CUR_DIR = Path(__file__).resolve().parent
DATA_FILE = CUR_DIR / 'data' / 'data.json'

# Création du dossier data
(CUR_DIR / "data").mkdir(exist_ok=True)

# stockage des données avec tinydb
data = TinyDB(DATA_FILE, indent=4)

# couleurs :
colors_hex = {"Yellow": "#ffff66",
              "Red": "#e52b50",
              "Green": "#a0db8e",
              "Purple": "#7e5687",
              "Blue": "#03396c",
              "Orange": "#ffab7a",
              "White": "#ffffff",
              "Black": "#161314",
              "Grey": "#515e55", }
colors = ["Yellow", "Red", "Green", "Purple", "Blue", "Orange", "White", "Black", "Grey"]
# black : Yellow GReen orange white



# on fait une classe pour créer chaque tache
class Task:
    def __init__(self, name, content="", color="Yellow", date=None):
        self.name = name
        self.content = content
        self.color = self._set_color(color)
        self.date = date

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Task({self.name}, {self.content}, {self.color["color_name"]}, {self.date})"

    def create_task(self):
        if self._control_existing_names(self.name):
            task = {"name": self.name,
                    "content": self.content,
                    "color": self.color,
                    "date": self._set_date(), }
            data.insert(task)
            return True
        return False


    def update_name(self, new_name):
        if self._control_existing_names(new_name):
            data.update({"name": new_name}, where("name") == self.name)
            self.name = new_name
            self._update_date()
            return True
        return False

    def update_content(self, new_content):
        data.update({"content": new_content}, where("name") == self.name)
        self.content = new_content
        self._update_date()

    def update_color(self, new_color):
        data.update({"color": self._set_color(new_color)}, where("name") == self.name)
        self.color = self._set_color(new_color)
        self._update_date()
        pass

    #methode à terminer
    def search_element_in_content(self, element):
        if element in self.content:
            return True
        return False


    @classmethod
    def load_task(cls, task_name):
        """ utiliser pour éviter les erreurs de normalisation liées à tinydb + permet de recreer des instances qui correspondent exactement à ce qui est stocké dans tinydb"""
        task = Query()
        task_dict = data.get(task.name == task_name)
        if task_dict:
            return cls(
                name=task_dict["name"],
                content=task_dict["content"],
                color=task_dict["color"]["color_name"],
                date=task_dict["date"]
            )
        return None


    def remove_task(self):
        data.remove(where("name") == self.name)


    # Créer une condition si une tache porte déja le meme nom
    @staticmethod
    def _control_existing_names(name):
        task = Query()
        result = data.get(task.name == name)
        if result:
            logging.warning(f"Il éxiste déja une tache '{name}', veuillez modifier le nom.")
            return False
        return True

    def _update_date(self):
        data.update({"date": self._set_date()}, where("name") == self.name)

    @staticmethod
    def _set_date() -> str:
        date = datetime.today()
        return date.strftime("%d/%m/%Y %H:%M")

    @staticmethod
    def _set_color(color) -> dict:
        if color in colors_hex:
            add_color = {"color_name" : color, "hex_name": colors_hex[color]}
        else:
            logging.warning(f"La couleur '{color}' n'existe pas. La couleur à été mise par défaut : 'Yellow'")
            add_color = {"color_name": "Yellow", "hex_name": colors_hex["Yellow"]}
        
        if add_color["color_name"] in ["Yellow", "Green", "Orange", "White"]:    
            add_color["color_text"] = "black"
        else :
            add_color["color_text"] = "white"
        return add_color
        
            
        


def get_all_tasks():
    tasks = []
    for task in data.all():

        #pemret de recrer des isntance de task à partir de la base de donnée
        each_task = Task(task["name"], task["content"], task["color"]["color_name"], task["date"])
        tasks.append(each_task)
    return tasks #pour pouvoir visualiser task il faut une methode __repr__dans la classe




if __name__ == "__main__":
    a = Task("à")
    a.create_task()
    # a.update_name("Task 2")
    a.update_content("l'anée derniere à été...")
    a.update_color('Purple')
    # a.remove_task()
