#!/usr/bin/env python3
# Generated with AI: Assisted-by: Microsoft 365 Copilot:GPT-5

import argparse
from pathlib import Path

import pathspec
from titlecase import titlecase

# Valid reStructuredText section adornment characters
RST_ADORNMENTS = set("=-`:'\"~^_*+#<>")


def load_gitignore(root):
    """Load .gitignore patterns from the search root if present."""
    gitignore = root / ".gitignore"

    if not gitignore.exists():
        return None

    with gitignore.open("r", encoding="utf-8") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f)


def is_gitignored(path, root, spec):
    """Return True if path matches .gitignore."""
    if spec is None:
        return False

    relpath = path.relative_to(root).as_posix()
    return spec.match_file(relpath)


def is_excluded_top_level(path, root, excluded_dirs):
    """Return True if path is under an excluded top-level directory."""
    rel_parts = path.relative_to(root).parts

    if not rel_parts:
        return False

    return rel_parts[0] in excluded_dirs


def is_rst_heading(lines, index):
    """Return True if lines[index] is an RST heading."""
    if index >= len(lines) - 1:
        return False

    title = lines[index].rstrip()
    underline = lines[index + 1].rstrip()

    if not title or not underline:
        return False

    if len(set(underline)) != 1:
        return False

    if underline[0] not in RST_ADORNMENTS:
        return False

    return len(underline) >= len(title)


def process_rst_file(path, dry_run=False):
    lines = path.read_text(encoding="utf-8").splitlines()

    modified = False

    for i in range(len(lines) - 1):
        if not is_rst_heading(lines, i):
            continue

        old_title = lines[i]
        new_title = titlecase(old_title)

        if new_title == old_title:
            continue

        if dry_run:
            print(f"{path}:{i + 1}")
            print(f"  - {old_title}")
            print(f"  + {new_title}")
        else:
            lines[i] = new_title

        modified = True

    if modified and not dry_run:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Updated: {path}")


def process_markdown_lines(path, lines, dry_run=False):
    modified = False

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        if not stripped.startswith("#"):
            continue

        hashes, sep, title = stripped.partition(" ")

        if not sep:
            continue

        new_title = titlecase(title)

        if new_title == title:
            continue

        if dry_run:
            print(f"{path}:{i + 1}")
            print(f"  - {title}")
            print(f"  + {new_title}")
        else:
            indent = line[: len(line) - len(stripped)]
            lines[i] = f"{indent}{hashes} {new_title}"

        modified = True

    return modified


def process_md_file(path, dry_run=False):
    lines = path.read_text(encoding="utf-8").splitlines()

    modified = process_markdown_lines(
        path,
        lines,
        dry_run=dry_run,
    )

    if modified and not dry_run:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Updated: {path}")


def process_readme_file(path, dry_run=False):
    """
    Process README files without an extension as Markdown.
    """
    lines = path.read_text(encoding="utf-8").splitlines()

    modified = process_markdown_lines(
        path,
        lines,
        dry_run=dry_run,
    )

    if modified and not dry_run:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Updated: {path}")


def should_process_file(path):
    if path.suffix.lower() in {".md", ".rst"}:
        return True

    return path.name.lower() == "readme"


def process_file(path, dry_run=False):
    suffix = path.suffix.lower()

    if suffix == ".rst":
        process_rst_file(path, dry_run)
    elif suffix == ".md":
        process_md_file(path, dry_run)
    elif path.name.lower() == "readme":
        process_readme_file(path, dry_run)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert Markdown and reStructuredText headings to title case "
            "while respecting .gitignore exclusions."
        ),
        epilog="""
Examples:
  %(prog)s .
  %(prog)s docs
  %(prog)s ~/projects/my-docs

Preview changes:
  %(prog)s docs --dry-run

Exclude top-level directories:
  %(prog)s . --exclude build
  %(prog)s . --exclude build --exclude dist --exclude venv

README files without extensions are processed as Markdown:
  README
  readme
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "path",
        help="Directory to recursively search",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show proposed changes without modifying files",
    )

    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="DIR",
        help="Exclude a top-level directory (may be specified multiple times)",
    )

    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()

    if not root.exists():
        parser.error(f"Path does not exist: {root}")

    gitignore_spec = load_gitignore(root)

    excluded_dirs = {
        Path(d).parts[0]
        for d in args.exclude
        if Path(d).parts
    }

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        if ".git" in file_path.parts:
            continue

        if is_excluded_top_level(
            file_path,
            root,
            excluded_dirs,
        ):
            continue

        if is_gitignored(
            file_path,
            root,
            gitignore_spec,
        ):
            continue

        if not should_process_file(file_path):
            continue

        process_file(
            file_path,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()