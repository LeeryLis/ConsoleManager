from rich.text import Text
from rich.console import Console

from src.logic import MathFuncs
from src.tools.console import BasicConsole, ConsoleManager, Param, ParamType

class ConsoleMathFuncs(BasicConsole):
    def __init__(self, original: MathFuncs):
        self.original = original
        self.console = Console()

    def _register_commands(self, console_manager: ConsoleManager) -> None:
        console_manager.register_command(
            action=self.original.sum_func,
            aliases=["sum"],
            description="Суммировать произвольное количество целых чисел",
            usage="sum [param_1] ... [param_N] <int_1> ... <int_N>",
            params={
                "-s": Param(
                    description="Вывести числа, участвующие в суммировании",
                    action=lambda *numbers: self.console.print(numbers),
                    param_type=ParamType.NO_MODIFY
                ),
                "-n": Param(
                    description="Отфильтровать: только отрицательные числа",
                    action=lambda *numbers: list(filter(lambda n: n < 0, numbers)),
                    param_type=ParamType.ARG_MODIFY
                ),
                "-p": Param(
                    description="Отфильтровать: только положительные числа",
                    action=lambda *numbers: list(filter(lambda n: n > 0, numbers)),
                    param_type=ParamType.ARG_MODIFY
                ),
                "-lb": Param(
                    description="Отфильтровать: по нижней границе",
                    action=lambda lb, *numbers: list(filter(lambda n: n >= lb, numbers)),
                    usage="-lb <lower bound>",
                    param_type=ParamType.ARG_MODIFY,
                    arg_number=1
                ),
                "-ub": Param(
                    description="Отфильтровать: по верхней границе",
                    action=lambda ub, *numbers: list(filter(lambda n: n <= ub, numbers)),
                    usage="-ub <upper bound>",
                    param_type=ParamType.ARG_MODIFY,
                    arg_number=1
                ),
                "-b": Param(
                    description="Отфильтровать: по нижней и верхней границе",
                    action=lambda lb, ub, *numbers: list(filter(lambda n: lb <= n <= ub, numbers)),
                    usage="-b <lower bound> <upper bound>",
                    param_type=ParamType.ARG_MODIFY,
                    arg_number=2
                ),
                "-text": Param(
                    description="Добавить текст в вывод",
                    action=lambda title: Text(title.replace("\\n", "\n")),
                    usage="-text <text>",
                    param_type=ParamType.NO_MODIFY,
                    arg_number=1
                ),
                "-sort": Param(
                    description="Отсортировать числа по возрастанию",
                    action=lambda *numbers: sorted(numbers),
                    param_type=ParamType.ARG_MODIFY
                ),
                "-sub": Param(
                    description="Вычесть число из результата",
                    action=self.sub_number,
                    param_type=ParamType.RESULT_MODIFY,
                    arg_number=1
                )
            }
        )

    def sub_number(self, number: int, result: int) -> int:
        return result - number


if __name__ == "__main__":
    ConsoleMathFuncs(MathFuncs()).run("MathFunc")
