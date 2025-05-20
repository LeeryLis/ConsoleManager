from rich.text import Text
from rich.console import Console

from src.logic import MathFuncs
from src.tools.console import BasicConsole, ConsoleManager, Param, ParamType

class ConsoleMathFuncs(BasicConsole):
    def __init__(self, original: MathFuncs):
        self.original = original
        self.console = Console()

    def _register_commands(self, console_manager: ConsoleManager) -> None:
        param_add_text = Param(
            description="Добавить текст в вывод",
            action=lambda title: self.console.print(Text(title.replace("\\n", "\n")), end=""),
            usage="-text <text>",
            param_type=ParamType.NO_MODIFY,
            arg_number=1
        )

        console_manager.register_command(
            aliases=["sum"],
            description="Суммировать произвольное количество целых чисел",
            action=self.original.sum_func,
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
                "-text": param_add_text,
                "-sort": Param(
                    description="Отсортировать числа по возрастанию",
                    action=lambda *numbers: sorted(numbers),
                    param_type=ParamType.ARG_MODIFY
                )
            }
        )
        console_manager.register_command(
            aliases=["rand"],
            description="Сгенерировать список случайных чисел",
            action=lambda: Text(f"Необходимо ввести параметры", style="red"),
            usage="rand <param_1> [param_2] ... [param_N]",
            params={
                "-sort": Param(
                    description="Отсортировать числа по возрастанию",
                    action=lambda numbers: sorted(numbers),
                    param_type=ParamType.RESULT_MODIFY
                ),
                "-text": param_add_text,
                "-uniform": Param(
                    description="Использовать равномерное распределение",
                    action=self.generate_random_numbers_uniform,
                    usage="-uniform <count> <min value> <max value>",
                    param_type=ParamType.LOGIC,
                    arg_number=3
                ),
                "-normal": Param(
                    description="Использовать нормальное распределение",
                    action=self.generate_random_numbers_normal,
                    usage="-normal <count> <mean> <std_dev>",
                    param_type=ParamType.LOGIC,
                    arg_number=3
                ),
                "-exp": Param(
                    description="Использовать экспоненциальное распределение",
                    action=self.generate_random_numbers_exponential,
                    usage="-exp <count> <scale>",
                    param_type=ParamType.LOGIC,
                    arg_number=2
                )
            }
        )

    def generate_random_numbers_uniform(self, count: int, min_value: int, max_value: int) -> list[int] | Text:
        try:
            return self.original.generate_random_numbers_uniform(count, min_value, max_value)
        except ValueError as e:
            return Text(f"ValueError: {e}")

    def generate_random_numbers_normal(self, count: int, mean: int, std_dev: int) -> list[int] | Text:
        try:
            return self.original.generate_random_numbers_normal(count, mean, std_dev)
        except ValueError as e:
            return Text(f"ValueError: {e}")

    def generate_random_numbers_exponential(self, count: int, scale: float) -> list[int] | Text:
        try:
            return self.original.generate_random_numbers_exponential(count, scale)
        except ValueError as e:
            return Text(f"ValueError: {e}")


if __name__ == "__main__":
    ConsoleMathFuncs(MathFuncs()).run("MathFunc")
