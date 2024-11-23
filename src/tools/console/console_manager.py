from typing import Any

import shlex
from rich.console import Console
from rich.table import Table
from rich.text import Text

from src.tools.console import Param
from src.tools.console import Command

class ConsoleManager:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_running = True
        self.commands: dict[str, Command] = {}
        self.register_command(Command(
            aliases=["h", "help"],
            description="Show help",
            action=self._print_help,
            usage="help [param] [command] [command param]",
            arg_types=[str, str],
            accepts_optional_args=True,
            params={
                "-p": Param(
                    description="Show help for all params of chosen command",
                    action=self._print_help_all_params,
                    arg_types=[str],
                    usage="-p <command>",
                    execute_command_action=False,
                    return_result=True
                )
            }
        ))
        self.register_command(Command(
            aliases=["s", "stop"],
            description="Stop this console manager",
            action=self.stop))

        self.console = Console()

    def register_command(self, command: Command) -> None:
        for alias in command.aliases:
            self.commands[alias] = command

    def _get_help_aliases(self) -> str:
        for command in self.commands.values():
            if command.action == self._print_help:
                return ", ".join(command.aliases)
        return ""

    def _print_help_all_params(self, command_name: str) -> Table | Text:
        command = self.commands.get(command_name)

        if not command:
            return Text("No such command", style="red")

        if not command.params:
            return Text("No any params")

        table = Table(title=f"{command_name} params", show_lines=True)
        table.add_column("Alias", style="cyan")
        table.add_column("Description", style="magenta")
        table.add_column("Usage", style="green")

        for alias, param in command.params.items():
            description = param.description
            usage_text = Text(param.usage) or "N/A"

            table.add_row(alias, description, usage_text)
        return table

    def _print_help(self, *args: str) -> Table | list[Text] | Text:
        def print_help_for_all() -> Table:
            table = Table(title="Available commands", show_lines=True)
            table.add_column("Aliases", style="cyan")
            table.add_column("Description", style="magenta")
            table.add_column("Usage", style="green")
            table.add_column("Params", style="yellow")

            printed_commands = set()
            for helped_command in self.commands.values():
                if helped_command in printed_commands:
                    continue
                aliases = ", ".join(helped_command.aliases)
                description = helped_command.description
                usage_text = Text(helped_command.usage) or "N/A"
                params_text = ", ".join(helped_command.params) if helped_command.params else "N/A"

                table.add_row(aliases, description, usage_text, params_text)
                printed_commands.add(helped_command)
            return table

        def print_help_for_command() -> Text | list[Text]:
            result = []

            command_name = args[0]
            helped_command = self.commands.get(command_name)

            if not helped_command:
                return Text(f"No such command: {command_name}", style="red")

            aliases = ", ".join(helped_command.aliases)
            result.append(Text("Command:", style="cyan"))
            result.append(Text(f"{aliases}"))

            if helped_command.description:
                result.append(Text("\nDescription:", style="magenta"))
                result.append(Text(f"{helped_command.description}"))

            if helped_command.usage:
                result.append(Text("\nUsage:", style="green"))
                result.append(Text(f"{helped_command.usage}"))

            if helped_command.params:
                result.append(Text("\nParams:", style="yellow"))
                result.append(Text(f"{', '.join(helped_command.params)}"))

            return result

        def print_help_for_command_param() -> Text | list[Text]:
            command_name = args[0]
            helped_command = self.commands.get(command_name)

            if not helped_command:
                return Text(f"No such command: {command_name}", style="red")

            if not helped_command.params:
                return Text(f"The command {command_name} has no any params", style="red")

            param_name = args[1]
            param = helped_command.params.get(param_name)

            if not param:
                return Text(f"The command {command_name} has no such param: {param_name}", style="red")

            result = []

            aliases = ", ".join(helped_command.aliases)
            result.append(Text("Command:", style="cyan"))
            result.append(Text(f"{aliases}"))

            result.append(Text("\nParam:", style="yellow"))
            result.append(Text(f"{param_name}"))

            result.append(Text("\nDescription:", style="magenta"))
            result.append(Text(f"{param.description}"))

            return result

        if len(args) == 0:
            return print_help_for_all()
        elif len(args) == 1:
            return print_help_for_command()
        elif len(args) == 2:
            return print_help_for_command_param()
        else:
            return Text("Too much arguments.", style="red")

    def stop(self) -> None:
        self.is_running = False

    def _verify_args(self, command_obj: Command, args: Any) -> bool:
        if not command_obj.arg_types:
            return True

        if command_obj.accepts_varargs:
            return len(args) >= len(command_obj.arg_types)

        return command_obj.accepts_optional_args or len(args) == len(command_obj.arg_types)

    def run(self) -> None:
        self.is_running = True
        while self.is_running:
            command_line = input(f"\n{self.name}: ").strip()
            if not command_line:
                continue

            command_name, *args = shlex.split(command_line)

            command_obj = self.commands.get(command_name)
            if not command_obj:
                self.console.print(
                    Text(f"Unknown command. Type {self._get_help_aliases()} for available commands.", style="red")
                )
                continue

            if not self._verify_args(command_obj, args):
                self.console.print(
                    Text("Usage:", style="green"),
                    Text(f"{command_obj.usage}")
                )
                continue

            result = command_obj.execute(*args)
            unpack = False
            if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], bool):
                result, unpack = result
            if result:
                if unpack or isinstance(result, list | tuple) and all([isinstance(elem, Text | Table) for elem in result]):
                    self.console.print(*result)
                else:
                    self.console.print(result)
