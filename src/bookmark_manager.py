import json
from pathlib import Path


class BookmarkManager:

    def __init__(self):
        self.file = (
            Path(__file__).parent.parent /
            "bookmarks.json"
        )

        self.bookmarks = self.load()

    def load(self):
        if not self.file.exists():
            return []

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.bookmarks, f, indent=4)

    def add_bookmark(self, title, url):

        for bookmark in self.bookmarks:
            if bookmark["url"] == url:
                return

        self.bookmarks.append({
            "title": title,
            "url": url
        })

        self.save()

    def all_bookmarks(self):
        return self.bookmarks