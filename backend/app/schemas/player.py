import json

Position = dict[str, float]

def parse_position_message(message: str) -> Position:
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return _parse_legacy_position(message)

    return {
        "x": float(data["x"]),
        "y": float(data["y"]),
        "z": float(data["z"]),
    }


def _parse_legacy_position(message: str) -> Position:
    parts = message.split(",")

    return {
        "x": float(parts[0].split(":")[1]),
        "y": float(parts[1].split(":")[1]),
        "z": float(parts[2].split(":")[1]),
    }
