import json
from pathlib import Path


class HistoryManager:

    def __init__(self):
        self.file = (
            Path(__file__).parent.parent /
            "history.json"
        )

        self.history = self.load()

    def load(self):

        if not self.file.exists():
            return []

        with open(self.file, "r") as file:
            return json.load(file)

    def save(self):

        with open(self.file, "w") as file:
            json.dump(self.history, file, indent=4)

    def add_visit(self, title, url):

        if url.startswith("file:///"):
            return

        self.history.append({
            "title": title,
            "url": url
        })

        self.save()

    def all_history(self):
        return self.history
    def clear(self):

         self.history = []

         self.save()