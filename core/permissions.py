from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()


def get_manual_permission_options(registry):
    return {
        name: details["description"]
        for name, details in registry.items()
    }


def configure_permissions(registry):
    console.print(
        "[bold]A. Always Ask[/bold]\n"
        "Ask before every action.\n\n"
        "[bold]B. Manual Perm Settings[/bold]\n"
        "Configure individual function permissions.\n\n"
        "[bold]C. Always Allow[/bold]\n"
        "Perform allowed actions without asking."
    )

    choice = Prompt.ask(
        "Permission mode",
        choices=["A", "B", "C"],
        case_sensitive=False,
    ).upper()

    mode = {
        "A": "always_ask",
        "B": "manual",
        "C": "always_allow",
    }[choice]

    manual_permissions = {}

    if mode == "manual":
        for function_name, description in (
            get_manual_permission_options(registry).items()
        ):
            console.print(f"\n[cyan]{function_name}[/cyan]")
            console.print(description)

            permission = Prompt.ask(
                "Permission",
                choices=["auto", "ask", "deny"],
                default="ask",
            )

            manual_permissions[function_name] = permission

    return {
        "permission_mode": mode,
        "manual_permissions": manual_permissions,
    }


def authorize_action(bot, function_name, arguments):
    mode = bot.get("permission_mode", "always_ask")

    if mode == "always_allow":
        return True

    if mode == "always_ask":
        return Confirm.ask(
            f"Allow {bot['name']} to execute "
            f"{function_name} with {arguments}?",
            default=False,
        )

    if mode == "manual":
        permission = bot.get(
            "manual_permissions", {}
        ).get(function_name, "ask")

        if permission == "auto":
            return True

        if permission == "deny":
            console.print("[yellow]Action denied by settings.[/yellow]")
            return False

        if permission == "ask":
            return Confirm.ask(
                f"Allow {bot['name']} to execute "
                f"{function_name} with {arguments}?",
                default=False,
            )

    console.print("[red]Unknown permission mode. Denied.[/red]")
    return False


def validate_function_arguments(registry, function_name, arguments):
    details = registry[function_name]
    parameters = details["parameters"]

    if not isinstance(arguments, dict):
        return False, "Arguments must be a JSON object."

    unknown = set(arguments) - set(parameters)

    if unknown:
        return False, f"Unknown arguments: {', '.join(unknown)}"

    missing = set(parameters) - set(arguments)

    if missing:
        return False, f"Missing arguments: {', '.join(missing)}"

    for name, info in parameters.items():
        value = arguments[name]

        if type(value) is not info["type"]:
            return False, (
                f"Argument '{name}' must be "
                f"{info['type'].__name__}."
            )

        if isinstance(value, str) and not value.strip():
            return False, f"Argument '{name}' cannot be empty."

    if details.get("validate") == "folder_name":
        name = arguments["name"]

        if name in {".", ".."} or "/" in name or "\\" in name:
            return False, "Use a folder name, not a path."

    return True, ""