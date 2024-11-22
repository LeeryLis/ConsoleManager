from typing import Callable, Optional, Any
from tools.console import Param

from rich.text import Text


class Command:
    def __init__(
            self,
            *,
            aliases: list[str],
            description: str,
            action: Callable[..., Any],
            usage: str = "",
            arg_types: Optional[list[type]] = None,
            accepts_varargs: bool = False,
            accepts_optional_args: bool = False,
            params: dict[str, Param] = None
    ) -> None:
        """
        :param aliases: "Имена" команды, по которым она вызывается в консоли
        :param description: Описание команды для пользователя
        :param action: Вызываемая функция
        :param usage: Описание использования для пользователя
        :param arg_types: Типы передаваемых в вызываемую функцию аргументов (соответствуют сигнатуре)
        :param accepts_varargs: Включение произвольного числа аргументов
        (Например: sum(*numbers: int) : sum 1, sum 1 2, sum 1 2 3)
        :param accepts_optional_args: Включение необязательности наличия всех аргументов (функция может иметь разную
        логику относительно числа переданных аргументов, как: help, help [command], help [command] [param])
        Или: array(cols: int, rows: int = 1) - первый аргумент совершенно точно должен быть приведён к int,
        а второй аргумент может не передаваться, чтобы использовать значение по умолчанию
        :param params: Словарь параметров команды. Нужно для лёгкого добавления разной логики для одной и той же
        команды, как: print -all, print -names, print -zero. Или: sum 1 2 -10 >>> -7, sum -n 1 2 -10 >>> -10
        sum -p 1 2 -10 >>> 3
        """
        self.aliases = aliases
        self.description = description
        self.action = action
        self.usage = usage
        self.arg_types = arg_types if arg_types else []
        self.accepts_varargs = accepts_varargs
        self.accepts_optional_args = accepts_optional_args
        self.params = params if params else None

    def _get_used_params(self, *args: str) -> tuple[int, list[tuple[Param, Optional[list[Any]]]]] | Text | None:
        if not self.params:
            return 0, []

        used_params = []
        i = 0
        while len(args) > i:
            param_obj = self.params.get(args[i])
            if not param_obj:
                break

            if not param_obj.arg_types:
                used_params.append((param_obj, None))
                i += 1
                continue

            start_param_args = i + 1
            end_param_args = start_param_args + len(param_obj.arg_types)
            if len(args) < end_param_args:
                return Text(f"Error: Not enough args for param {args[i]}. Usage: {param_obj.usage}. "
                            f"Expected types: {[t.__name__ for t in param_obj.arg_types]}", style="red")

            param_args: list[str] = [param_arg for param_arg in args[start_param_args:end_param_args]]
            try:
                typed_param_args = [arg_type(param_arg) for param_arg, arg_type in zip(param_args, param_obj.arg_types)]
            except ValueError as e:
                return Text(f"Error: {e}. Usage: {param_obj.usage}. "
                            f"Expected types: {[t.__name__ for t in param_obj.arg_types]}", style="red")

            used_params.append((
                param_obj,
                typed_param_args
            ))

            i += 1 + len(param_obj.arg_types)

        return i, used_params

    def _get_typed_args(self, *args: str) -> list[Any] | ValueError:
        if not self.accepts_varargs:
            typed_args = [arg_type(arg) for arg, arg_type in zip(args, self.arg_types)]
        else:
            fixed_args = [arg_type(arg) for arg, arg_type in zip(args[:len(self.arg_types) - 1], self.arg_types)]
            vararg_type = self.arg_types[-1]
            varargs = [vararg_type(arg) for arg in args[len(self.arg_types) - 1:]]

            typed_args = [*fixed_args, *varargs]

        return typed_args

    def execute(self, *args: str) -> Any:
        if not args:
            if not self.accepts_optional_args and self.arg_types:
                return [Text(f"Usage:", style="green"), Text(f"{self.usage}")]
            return self.action()

        # Разбор переданных аргументов для нахождения параметров и их аргументов
        used_params = []
        i = 0
        while len(args) > i and self.params:
            param_obj = self.params.get(args[i])
            if not param_obj:
                break

            if not param_obj.arg_types:
                used_params.append((param_obj, None))
                i += 1
                continue

            start_param_args = i + 1
            end_param_args = start_param_args + len(param_obj.arg_types)
            if len(args) < end_param_args:
                return Text(f"Error: Not enough args for param {args[i]}. Usage: {param_obj.usage}. "
                            f"Expected types: {[t.__name__ for t in param_obj.arg_types]}", style="red")

            param_args: list[str] = [param_arg for param_arg in args[start_param_args:end_param_args]]
            try:
                typed_param_args = [arg_type(param_arg) for param_arg, arg_type in zip(param_args, param_obj.arg_types)]
            except ValueError as e:
                return Text(f"Error: {e}. Usage: {param_obj.usage}. "
                            f"Expected types: {[t.__name__ for t in param_obj.arg_types]}", style="red")

            used_params.append((
                param_obj,
                typed_param_args
            ))

            i += 1 + len(param_obj.arg_types)

        start_args = i

        try:
            typed_args = self._get_typed_args(*args[start_args:])
        except ValueError as e:
            return Text(f"Error: {e}. Expected types: {[t.__name__ for t in self.arg_types]}", style="red")

        if not used_params:
            return self.action(*typed_args)

        result = []
        execute_command_action = True
        actual_args = typed_args
        for param, param_args in used_params:
            execute_command_action = execute_command_action and param.execute_command_action

            if param.use_command_args:
                param_result = param.action(*param_args, *actual_args) if param_args else param.action(*actual_args)
            else:
                param_result = param.action(*param_args) if param_args else param.action()

            if param.modify:
                actual_args = param_result

            if param.return_result:
                result.append(param_result)

        if execute_command_action:
            result.append(self.action(*actual_args))
        return result, True
