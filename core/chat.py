import base64
import io
import json
import urllib.request
import urllib.error

from functions.control import see
from core.registry import FUNCTION_REGISTRY
from core.permissions import (
    authorize_action,
    validate_function_arguments,
)


OLLAMA_URL = "http://localhost:11434/api/chat"


def get_function_descriptions():
    lines = []

    for name, details in FUNCTION_REGISTRY.items():
        parameters = ", ".join(
            f"{param}: {info['description']}"
            for param, info in details["parameters"].items()
        )

        lines.append(
            f"- {name}({parameters}): {details['description']}"
        )

    return "\n".join(lines)


def send_message(model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": 512,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=900) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["message"]


def handle_function_requests(response, bot):
    marker = "FUNCTION_CALLS:"

    if marker not in response:
        return response.strip(), [], [], []

    answer, function_text = response.split(marker, 1)

    results = []
    images = []
    tool_outputs = []

    try:
        requests = json.loads(function_text.strip())

        if not isinstance(requests, list):
            raise ValueError("Expected a JSON list of function calls.")

    except (json.JSONDecodeError, ValueError) as exc:
        return answer.strip(), [
            f"Invalid function-call JSON: {exc}"
        ], [], []

    for request_data in requests:
        if not isinstance(request_data, dict):
            results.append("Rejected: function request must be an object.")
            continue

        function_name = request_data.get("function")
        arguments = request_data.get("arguments")

        if not isinstance(function_name, str):
            results.append("Rejected: function name must be a string.")
            continue

        details = FUNCTION_REGISTRY.get(function_name)

        if details is None:
            results.append(f"Rejected: unknown function {function_name!r}.")
            continue

        valid, error = validate_function_arguments(
            FUNCTION_REGISTRY,
            function_name,
            arguments,
        )

        if not valid:
            results.append(f"Rejected: {error}")
            continue

        if not authorize_action(bot, function_name, arguments):
            results.append(f"Not executed: {function_name}.")
            continue

        try:
            result = details["function"](**arguments)

            if function_name == "see":
                image_buffer = io.BytesIO()
                result.save(image_buffer, format="PNG")

                images.append(
                    base64.b64encode(
                        image_buffer.getvalue()
                    ).decode("ascii")
                )

                results.append("Screenshot captured successfully.")

            elif result is False:
                results.append(f"Failed: {function_name}.")

            elif function_name == "list_contents":
                if result:
                    contents = "\n".join(
                        f"- {item}" for item in result
                    )
                    results.append(
                        f"Contents of {arguments['folder']}:\n{contents}"
                    )
                else:
                    results.append(
                        f"The folder {arguments['folder']} is empty."
                    )

            elif function_name in {"search_web", "search_videos"}:
                tool_outputs.append(
                    f"Results from {function_name}:\n"
                    + json.dumps(
                        result,
                        ensure_ascii=False,
                        indent=2,
                        default=str,
                    )
                )

                results.append(
                    f"Search completed: {len(result)} results returned."
                )

            else:
                results.append(f"Executed: {function_name}.")

        except Exception as exc:
            results.append(f"Failed: {function_name}: {exc}")

    return answer.strip(), results, images, tool_outputs