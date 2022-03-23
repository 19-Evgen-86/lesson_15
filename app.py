from flask import Flask
import utils

app = Flask(__name__)


@app.get("/animal/<int:id>")
def get_animal(id):
    return utils.get_animal_by_id(id)


if __name__ == '__main__':
    app.run()
