import os.path
import random
from random import randint
from flask import Blueprint, current_app
from flask import Blueprint, render_template, request

from classes.data_manager import DataManager

loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder='templates')


class OutOfFreeNamesError(Exception):
    pass


def get_free_filename(folder, file_type):

    attemps = 0
    RANGE_OF_IMAGE_NUMBERS = 100
    LIMIT_OF_ATEMPS = 10000

    while True:
        pic_name = str(random.randint(0, RANGE_OF_IMAGE_NUMBERS))
        filename_to_save = f"{pic_name}.{file_type}"
        os_path = os.path.join(folder, filename_to_save)
        is_filename_occupied = os.path.exists(os_path)

        if not is_filename_occupied:
            return filename_to_save
        attemps += 1

        if attemps > LIMIT_OF_ATEMPS:
            raise OutOfFreeNamesError("No free names to save Image")



@loader_blueprint.route('/post', methods=['GET'])
def page_from():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def page_greate_posts():

    picture = request.files.get("picture", None)
    content = request.values.get("content", "")

    filename = picture.filename
    file_type = filename.split('.')[-1]

    folder = os.path.join(".", "uploads", "images")

    # получаем свободное имя
    filename_to_save = get_free_filename(folder, file_type)

    # сохраняем под новым именем
    picture.save(os.path.join(folder, filename_to_save))

    # формируем путь для браузера клиент
    web_path = f"/uploads/images{filename_to_save}"

    # Сохраняем данные
    post = {"pic": web_path, "content": content}

    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    data_manager.add(post)

    return render_template("post_uploaded.html", pic=web_path, content=content)

@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_names(e):
    return "Закончились свободные имена для загрузки картринок"
