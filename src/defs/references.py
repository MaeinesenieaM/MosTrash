"""
Este código cria classes que guardam apenas um tipo de valor para ser possível mudá-las
diretamente por funções ou elas mesmas.
OBRIGADO PYTHON!
"""

class Reference:
    def set(self, value): pass
    def get(self) -> any: pass
    def as_str(self) -> str: pass
    def compare(self, other) -> bool: pass

    def __eq__(self, other):
        return self.compare(other)

    def __str__(self):
        return self.as_str()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.get()!r})"

class BoolRef(Reference):
    def __init__(self, state: bool):
        self.state = state

    def set(self, new_state: bool | Reference):
        if isinstance(new_state, Reference): new_state = bool(new_state.get())
        self.state = new_state

    def get(self):
        return self.state

    def compare(self, other_state: bool | Reference) -> bool:
        if isinstance(other_state, Reference): other_state = bool(other_state.get())
        return self.state == other_state

    def as_str(self) -> str:
        return str(self.state)

    def toggle(self):
        self.state = not self.state

    def __bool__(self):
        return self.state

class IntRef(Reference):
    def __init__(self, value: int):
        self.value = value

    def set(self, new_value: int | Reference):
        if isinstance(new_value, Reference): new_value = int(new_value.get())
        self.value = new_value

    def get(self) -> int:
        return self.value

    def compare(self, other_value: int | Reference) -> bool:
        if isinstance(other_value, Reference): other_value = int(other_value.get())
        return self.value == other_value

    def as_str(self) -> str:
        return str(self.value)

class FloatRef(Reference):
    def __init__(self, value: float):
        self.value = value

    def set(self, new_value: float | Reference):
        if isinstance(new_value, Reference): new_value = float(new_value.get())
        self.value = new_value

    def get(self) -> float:
        return self.value

    def compare(self, other_value: float | Reference):
        if isinstance(other_value, Reference): other_value = float(other_value.get())
        return self.value == other_value

    def as_str(self) -> str:
        return str(self.value)