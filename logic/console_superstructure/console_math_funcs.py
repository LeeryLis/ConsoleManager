from tools.console import BasicConsole
from tools.console import ConsoleManager, Command, Param

from logic import MathFuncs

from rich.text import Text

class ConsoleMathFuncs(BasicConsole):
    def __init__(self, original: MathFuncs):
        self.original = original

    def _register_commands(self, console_manager: ConsoleManager) -> None:
        console_manager.register_command(Command(
            aliases=["sum"],
            description="Суммировать произвольное количество целых чисел",
            action=self.original.sum_func,
            usage="sum [param_1] ... [param_N] <int_1> ... <int_N>",
            arg_types=[int],
            accepts_varargs=True,
            params={
                "-s": Param(
                    description="Вывести числа, участвующие в суммировании",
                    action=lambda *numbers: numbers,
                    modify=False,
                    return_result=True
                ),
                "-n": Param(
                    description="Отфильтровать: только отрицательные числа",
                    action=lambda *numbers: list(filter(lambda n: n < 0, numbers))
                ),
                "-p": Param(
                    description="Отфильтровать: только положительные числа",
                    action=lambda *numbers: list(filter(lambda n: n > 0, numbers))
                ),
                "-lb": Param(
                    description="Отфильтровать: по нижней границе",
                    action=lambda lb, *numbers: list(filter(lambda n: n >= lb, numbers)),
                    arg_types=[int],
                    usage="-lb <lower bound>"
                ),
                "-ub": Param(
                    description="Отфильтровать: по верхней границе",
                    action=lambda ub, *numbers: list(filter(lambda n: n <= ub, numbers)),
                    arg_types=[int],
                    usage="-ub <upper bound>"
                ),
                "-b": Param(
                    description="Отфильтровать: по нижней и верхней границе",
                    action=lambda lb, ub, *numbers: list(filter(lambda n: lb <= n <= ub, numbers)),
                    arg_types=[int, int],
                    usage="-b <lower bound> <upper bound>"
                ),
                "-text": Param(
                    description="Добавить текст в вывод",
                    action=lambda title: Text(title.replace("\\n", "\n")),
                    usage="-text <text>",
                    arg_types=[str],
                    modify=False,
                    return_result=True,
                    use_command_args=False
                ),
                "-sort": Param(
                    description="Отсортировать числа по возрастанию",
                    action=lambda *numbers: sorted(numbers)
                )
            }
        ))


if __name__ == "__main__":
    ConsoleMathFuncs(MathFuncs()).run("MathFunc")
