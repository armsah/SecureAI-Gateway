from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "docs/problem-statement.md",
    "docs/data-classification.md",
    "docs/non-functional-requirements.md",
    "docs/architecture/README.md",
    "docs/architecture/sequence.md",
    "docs/adr/0001-platform-boundaries.md",
    "docs/adr/0002-deterministic-policy.md",
    "docs/security/threat-model.md",
    "docs/security/risk-policy.md",
    "docs/security/authorization-matrix.md",
    "docs/evaluation/specification.md",
]

STRIDE_CATEGORIES = [
    "spoofing",
    "tampering",
    "repudiation",
    "information disclosure",
    "denial of service",
    "elevation of privilege",
]


def validate_required_files():
    errors = []

    for relative_path in REQUIRED_FILES:
        file_path = ROOT / relative_path

        if not file_path.is_file():
            errors.append(f"Missing file: {relative_path}")

        elif file_path.stat().st_size == 0:
            errors.append(f"Empty file: {relative_path}")

    return errors


def validate_markdown_links():
    errors = []

    for relative_path in REQUIRED_FILES:
        if not relative_path.endswith(".md"):
            continue

        file_path = ROOT / relative_path

        if not file_path.is_file():
            continue

        content = file_path.read_text(encoding="utf-8")

        links = re.findall(
            r"!?\[[^\]]*\]\(([^)]+)\)",
            content
        )

        for link in links:
            target = link.strip().split("#", 1)[0]

            if not target:
                continue

            if target.startswith(
                ("http://", "https://", "mailto:")
            ):
                continue

            target = target.split(" ", 1)[0]

            resolved_path = file_path.parent / target

            if not resolved_path.exists():
                errors.append(
                    f"Broken Markdown link in "
                    f"{relative_path}: {link}"
                )

    return errors


def validate_threat_model():
    errors = []

    path = ROOT / "docs/security/threat-model.md"

    if not path.is_file() or path.stat().st_size == 0:
        return errors

    content = path.read_text(
        encoding="utf-8"
    ).lower()

    for category in STRIDE_CATEGORIES:
        if category not in content:
            errors.append(
                "Threat model missing STRIDE category: "
                f"{category}"
            )

    return errors


def validate_architecture():
    errors = []

    path = ROOT / "docs/architecture/README.md"

    if not path.is_file() or path.stat().st_size == 0:
        return errors

    content = path.read_text(
        encoding="utf-8"
    ).lower()

    required_terms = [
        "domain",
        "application",
        "infrastructure",
        "api",
    ]

    for term in required_terms:
        if term not in content:
            errors.append(
                "Architecture documentation missing term: "
                f"{term}"
            )

    return errors


def main():
    print("=" * 60)
    print("SecureAI Gateway — P0 Validation")
    print("=" * 60)

    errors = []

    errors.extend(validate_required_files())
    errors.extend(validate_markdown_links())
    errors.extend(validate_threat_model())
    errors.extend(validate_architecture())

    if errors:
        print("\nVALIDATION FAILED\n")

        for error in errors:
            print(f"[ERROR] {error}")

        print(f"\nTotal errors: {len(errors)}")

        sys.exit(1)

    print("\nVALIDATION PASSED")
    print(
        f"\nValidated {len(REQUIRED_FILES)} required files."
    )
    print("Markdown links: PASS")
    print("Security documentation: PASS")
    print("Architecture documentation: PASS")
    print("\nP0 documentation integrity verified.")

    sys.exit(0)


if __name__ == "__main__":
    main()