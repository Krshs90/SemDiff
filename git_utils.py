import subprocess
import re

MAX_DIFF_CHARS = 100000


def get_staged_diff() -> str:
    """Run `git diff --staged` and capture the output."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True,
        )
        diff_text: str = result.stdout

        if len(diff_text) > MAX_DIFF_CHARS:
            diff_text = (
                diff_text[:MAX_DIFF_CHARS]
                + "\n\n... [DIFF TRUNCATED — too large for context window. "
                + f"Showing first {MAX_DIFF_CHARS:,} characters out of {len(result.stdout):,}.]"
            )
        return diff_text
    except subprocess.CalledProcessError as e:
        return ""


# Files that indicate architectural risk when modified.
RISK_PATTERNS = [
    r"config\.py",
    r"settings\.py",
    r"\.env",
    r".*\.sql$",
    r"schema\.py",
    r"models\.py",
    r"alembic/.*",
    r"migrations/.*",
    r"docker-compose.*",
    r"Dockerfile",
    r"\.github/workflows/.*",
]


def check_for_breaking_changes(diff_text: str) -> bool:
    """Scans the git diff for architectural risk files."""
    files_touched = re.findall(r"diff --git a/(.*?) b/", diff_text)

    for file in files_touched:
        for pattern in RISK_PATTERNS:
            if re.match(pattern, file, re.IGNORECASE):
                return True

    return False
