from rich import box
from rich.color import Color
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text


console = Console()


def print_banner():
    banner = r"""
   ____                                 _
  / __ \                     /\        | |
 | |  | |_ __   ___ _ __    /  \  _   _| |_ ___
 | |  | | '_ \ / _ \ '_ \  / /\ \| | | | __/ _ \
 | |__| | |_) |  __/ | | |/ ____ \ |_| | || (_) |
  \____/| .__/ \___|_| |_/_/    \_\__,_|\__\___/
        | |
        |_|
    """

    console.print(banner, style="bold cyan")


def normalize_color(value):
    value = value.strip()

    import re

    rgb_match = re.fullmatch(
        r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
        value,
        re.IGNORECASE,
    )

    if rgb_match:
        channels = [int(channel) for channel in rgb_match.groups()]

        if any(channel > 255 for channel in channels):
            raise ValueError("RGB values must be between 0 and 255.")

        return "#{:02x}{:02x}{:02x}".format(*channels)

    if re.fullmatch(r"\s*\d+\s*,\s*\d+\s*,\s*\d+\s*", value):
        channels = [int(part.strip()) for part in value.split(",")]

        if any(channel > 255 for channel in channels):
            raise ValueError("RGB values must be between 0 and 255.")

        return "#{:02x}{:02x}{:02x}".format(*channels)

    Color.parse(value)
    return value


def show_bot_panel(bot):
    console.print(
        Panel(
            f"[bold]Bot:[/bold] {bot['name']}\n"
            f"[bold]Model:[/bold] {bot.get('model', '')}\n"
            f"[bold]Permissions:[/bold] "
            f"{bot.get('permission_mode', 'always_ask')}\n"
            "Type /exit to leave this conversation.",
            border_style=bot.get("color", "#10a37f"),
            expand=False,
        )
    )


def show_bot_response(name, color, answer):
    console.print()
    console.print(
        Panel(
            answer or "[dim]No message from the bot.[/dim]",
            title=Text(name, style=f"bold {color}"),
            border_style=color,
        )
    )


def show_action_results(results):
    for result in results:
        console.print(f"[cyan]OpenAuto:[/cyan] {result}")

def show_bot_creation_header():
    console.print(
        Panel(
            "[bold cyan]BOT CREATION[/bold cyan]\n"
            "Configure your new OpenAuto bot.",
            box=box.DOUBLE,
            expand=False,
        )
    )


def show_bot_table(bots):
    if not bots:
        console.print("[yellow]No bots created yet.[/yellow]")
        console.print("Use [bold]create[/bold] to create one.")
        return

    table = Table(
        title="YOUR BOTS",
        box=box.ROUNDED,
        show_lines=True,
    )

    table.add_column("Name")
    table.add_column("Color")
    table.add_column("Job")
    table.add_column("AI Model")
    table.add_column("Permissions")

    for bot in bots.values():
        color = bot.get("color", "#10a37f")

        table.add_row(
            Text(bot.get("name", "Unnamed"), style=color),
            color,
            bot.get("job", ""),
            bot.get("model", ""),
            bot.get("permission_mode", "always_ask"),
        )

    console.print(table)


def show_bot_created(bot):
    console.print(
        Panel(
            f"[bold green]Bot created![/bold green]\n\n"
            f"Name: {bot['name']}\n"
            f"Color: {bot['color']}\n"
            f"Job: {bot['job']}\n"
            f"AI model: {bot['model']}\n"
            f"Permission mode: {bot['permission_mode']}\n\n"
            f"Chat using: talk {bot['name']}",
            title="OpenAuto",
            border_style=bot["color"],
            expand=False,
        )
    )