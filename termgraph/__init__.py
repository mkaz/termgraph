__all__ = ["main"]

def __getattr__(name):
    if name == "main":
        from .termgraph import main
        return main
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")