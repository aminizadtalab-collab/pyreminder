"""
مدیریت داده‌ها (خواندن/نوشتن JSON)
"""
import json
import os
from datetime import datetime
from typing import Any
from app.config import DATA_FILE


class DataManager:
    def __init__(self):
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "tasks": [],
            "settings": {
                "sound": True,
                "repeat": True,
                "repeat_interval": 10,
                "startup": False,
            },
            "profile": {"name": "کاربر", "role": "توسعه‌دهنده"},
        }

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    @property
    def data(self) -> dict:
        return self._data

    @property
    def tasks(self) -> list:
        return self._data["tasks"]

    @property
    def settings(self) -> dict:
        return self._data["settings"]

    def add_task(self, task: dict):
        self._data["tasks"].append(task)
        self.save()

    def remove_task(self, task_id: float):
        self._data["tasks"] = [t for t in self._data["tasks"] if t["id"] != task_id]
        self.save()

    def update_task(self, task_id: float, updates: dict):
        for t in self._data["tasks"]:
            if t["id"] == task_id:
                t.update(updates)
                break
        self.save()

    def get_task(self, task_id: float) -> dict | None:
        for t in self._data["tasks"]:
            if t["id"] == task_id:
                return t
        return None

    def update_setting(self, key: str, value: Any):
        self._data["settings"][key] = value
        self.save()