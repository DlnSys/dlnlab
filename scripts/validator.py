import os

from scripts.catalog import load_catalog
from scripts.config import load_config
from scripts.colors import YELLOW, RESET


def validate_catalog():
    catalog = load_catalog()
    config = load_config()
    base = os.path.dirname(__file__) + "/.."
    warnings = []

    for challenge in catalog:
        name = challenge.get("name", "?")
        runtime = challenge.get("runtime", "")

        if runtime == "file":
            file_field = challenge.get("file" , "")
            files = file_field if isinstance(file_field, list) else [file_field]
            category = challenge.get("category", challenge.get("theme", "")).strip()
            challenges_dir = os.path.join(base, config["challenges_dir"], category, name)
            for f in files:
                if not f:
                    continue
                full_path = os.path.join(challenges_dir, f)
                if not os.path.exists(full_path):
                    warnings.append(f"  {name} — missing file: {f}")

        elif runtime in ("docker", "netcat"):
            compose_path = os.path.join(base, config["boxes_dir"], name, "docker-compose.yml")
            if not os.path.exists(compose_path):
                warnings.append(f"  {name} — missing docker-compose.yml")

    if warnings:
        print(f"\n{YELLOW}[!] Catalog warnings:{RESET}")
        for w in warnings:
            print(f"{YELLOW}{w}{RESET}")
        print()