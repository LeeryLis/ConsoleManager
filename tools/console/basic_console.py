from abc import ABC, abstractmethod
from tools.console import ConsoleManager

class BasicConsole(ABC):
    """
    При надстройке над некоторым классом необходимо заводить поле со ссылкой на этот класс.
    Например: ConsoleMathFuncs надстраивается над MathFuncs, работая с его методами.
    Тогда __init__() для ConsoleMathFuncs(BasicConsole) будет выглядеть так:
    def __init__(self, original: MathFuncs) -> None:
        self.original = original
    """
    @abstractmethod
    def _register_commands(self, console_manager: ConsoleManager) -> None:
        """
        Абстрактный метод регистрации команд консольного менеджера
        """
        pass

    def run(self, name: str) -> None:
        console_manager = ConsoleManager(name)
        self._register_commands(console_manager)
        console_manager.run()
