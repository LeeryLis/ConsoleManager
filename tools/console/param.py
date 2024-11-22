from typing import Callable,Optional, Any


class Param:
    def __init__(
            self,
            *,
            description: str,
            action: Callable[..., Any],
            modify: bool = True,
            execute_command_action: bool = True,
            return_result: bool = False,
            use_command_args: bool = True,
            arg_types: Optional[list[type]] = None,
            usage: str = ''
    ) -> None:
        """
        Параметр команды. Нужен для организации вариаций одной и той же команды или модификации переданных
        в команду аргументов.
        Имя параметра не представлено, так как это подчёркивает, что любой параметр
        неразрывно связан со своей командой и должен храниться в собственном словаре команды.

        :param description: Описание параметра для пользователя
        :param action: Вызываемая параметром функция
        :param modify: Параметр, показывающий, будут ли модифицированы введённые в команду аргументы
        (передаваемые в функцию команды)
        Если параметр modify=False, то он не изменяет передаваемые в основную функцию в логике команды-родителя
        аргументы, а, например, производит вывод в консоль или модифицированный вывод в консоль.
        Например: sum - суммирует числа и выводит результат, -s - выводит слагаемые
        sum -s 1 2 3 >>> [1, 2, 3] 6
        Или: -p - фильтрует числа, оставляя только положительные (не выводит в консоль, работает только с логикой)
        1. sum -p -s 1 -2 3 -4 -5 >>> [1, 3] 4 - если для -p modify=True
        2. sum -p -s 1 -2 3 -4 -5 >>> [1, -2, 3, -4, -5] -7 - если для -p modify=False
        Во втором случае работа параметра не повлияла на реальные аргументы для основной функции
        :param execute_command_action: если хотя бы у одного из параметров
        execute_command_action был равен False, то в самом конце, после выполнения функций всех параметров,
        функция команды не будет выполнена
        :param return_result: если True, то результат выполнения функции параметра будет добавлен в общий result
        :param use_command_args: будет ли функция параметра принимать на вход аргументы, введённые
        для функции команды (например, для их модификации или вывода в консоль)
        :param arg_types: Типы аргументов, используемых параметром
        Например: -lb <int> - фильтрует числа по установленной нижней границе
        sum -lb 5 -s 1 3 5 7 9 >>> [5, 7, 9] 21
        :param usage: Описание использования для пользователя
        Например: "-lb <lower bound>", "-b <lower bound> <upper bound>"
        """
        self.description = description
        self.action = action
        self.modify = modify
        self.execute_command_action = execute_command_action
        self.return_result = return_result
        self.use_command_args = use_command_args
        self.arg_types = arg_types
        self.usage = usage
