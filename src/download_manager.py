from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest

import json
from pathlib import Path


class DownloadManager:

    def __init__(self):
        self.file = (
            Path(__file__).parent.parent /
            "downloads.json"
        )

        self.downloads = self.load()

    def load(self):
        if not self.file.exists():
            return []

        with open(self.file, "r") as file:
            return json.load(file)

    def save(self):
        with open(self.file, "w") as file:
            json.dump(self.downloads, file, indent=4)

    def add_download(self, filename, path, status):
        self.downloads.append({
            "filename": filename,
            "path": path,
            "status": status
        })

        self.save()

    def all_downloads(self):
        return self.downloads

    def clear(self):
        self.downloads = []
        self.save()