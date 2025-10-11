import importlib


def loadPlatform(name: str):
    return importlib.import_module(f"Platform.{name}")
