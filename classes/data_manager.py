import json
# from pprint import pprint as pp

class DataManager:

    def __init__(self, path):
        self.path = path


    def _load_data(self):
        """Загружает данные из файла для исп другими методами"""
        # try:
        with open(self.path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # except (FileNotFoundError, json.JSONDecodeError):
        return data


    def _save_data(self, data):
        """Перезаписывает переданные в файле с данными"""
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


    def get_all(self):
        """Отдает полный список"""
        data = self._load_data()
        return data

    def search(self, substring):
        """Отдает посты который содержат substring"""
        posts = self._load_data()
        substring = substring.lower()

        matching_posts = [post for post in posts if substring in post["content"].lower()]
        return matching_posts

    def add(self, post):
        """Добавляет в хранилище постов определенный пост"""
        if type(post) != dict:
            raise TypeError("Dict expected for adding post")

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)


# dm = DataManager("../tests/mock_posts.json")
#
# post = {"pic": "...", "content": "..."}
#
# pp(dm.add(post))