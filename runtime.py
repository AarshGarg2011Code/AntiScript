# AntiScript v1.0.0 Based on Python v3.14.5
# Author Aarsh Garg
# File 'runtime.py'
# AntiScript Python SRC

class RuntimeErrorAnti(Exception):
    pass
class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
    def exists(self, name):
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.exists(name)
        return False
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeErrorAnti(
            f"Variable '{name}' does not exist."
        )
    def set(self, name, value):
        self.variables[name] = value
class Runtime:
    def __init__(self):
        self.global_scope = Scope()
        self.functions = {}
        self.native_functions = {}
        self.loaded_modules = set()
        self.modules = {}
        self.loaded_modules = set()
        self.last_input = None
        self.native_functions = {}
        self.loaded_modules = set()
    def get(self, name):
        return self.global_scope.get(name)
    def set(self, name, value):
        self.global_scope.set(name, value)