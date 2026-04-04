import os
import re


def get_crm_data_path():
    env_override = os.getenv("CRM_DATA_PATH")
    if env_override:
        return os.path.abspath(env_override)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    logic_root = os.path.abspath(os.path.join(script_dir, "../"))
    env_path = os.path.join(logic_root, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("CRM_DATA_PATH="):
                    path = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return os.path.abspath(os.path.join(logic_root, path)) if not os.path.isabs(path) else path
    return os.getcwd()


CRM_DATA_PATH = get_crm_data_path()
LEGACY_ACCOUNT_SLUGS = [
    "917Ventures",
    "Aboitiz-Group",
    "AboitizPower",
    "Archipelago Capital Partners",
    "Citi",
    "Energeia-USA",
    "Finbots-ai",
    "ForumCFO",
    "Kaizen-Leadership-Asia",
    "Mazorda",
    "Michael-Page",
    "RFC",
    "SolViva-Energy",
]


def iter_files():
    for root, _, files in os.walk(CRM_DATA_PATH):
        for file_name in files:
            if file_name.startswith(".!"):
                continue
            if not (file_name.endswith(".md") or file_name.endswith(".json")):
                continue
            yield os.path.join(root, file_name)


def replace_links(content, slug):
    escaped = re.escape(slug)
    replacements = [
        (rf"\[\[\s*Accounts/{escaped}\s*\]\]", f"[[Organizations/{slug}]]"),
        (rf"\[\[\s*Accounts/{escaped}\|([^\]]+)\]\]", rf"[[Organizations/{slug}|\1]]"),
        (rf"\[\[\s*{escaped}\s*\]\]", f"[[Organizations/{slug}]]"),
        (rf"\[\[\s*{escaped}\|([^\]]+)\]\]", rf"[[Organizations/{slug}|\1]]"),
    ]
    updated = content
    for pattern, replacement in replacements:
        updated = re.sub(pattern, replacement, updated)
    return updated


def main():
    changed = []
    for path in iter_files():
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            original = handle.read()
        updated = original
        for slug in LEGACY_ACCOUNT_SLUGS:
            updated = replace_links(updated, slug)
        if updated != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(updated)
            changed.append(path)

    print("updated-files:", len(changed))
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
