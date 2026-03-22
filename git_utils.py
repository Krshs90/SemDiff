import subprocess
import re

# Context window limit approx 32k tokens, say 100k chars to be safe.
MAX_DIFF_LENGTH = 100000

def get_staged_diff() -> str:
    """Run `git diff --staged` and capture the output."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged'],
            capture_output=True,
            text=True,
            check=True
        )
        diff_text = result.stdout
        if not isinstance(diff_text, str):
            diff_text = str(diff_text)
            
        if len(diff_text) > 100000:
            diff_text = diff_text[:100000] + "\n\n... [DIFF TRUNCATED TO FIT CONTEXT WINDOW]"  # type: ignore
        return diff_text
    except subprocess.CalledProcessError as e:
        print(f"Git diff failed: {e.stderr}")
        return ""

def check_for_breaking_changes(diff_text: str) -> bool:
    """Scans the git diff for architectural risk files."""
    # Look for diff file headers (diff --git a/... b/...)
    # Or simply regex match filenames touched.
    # We look for config.py, db schema files (.sql, models.py, schema.py)
    
    risk_patterns = [
        r'config\.py',
        r'settings\.py',
        r'.*\.sql$',
        r'schema\.py',
        r'models\.py',
        r'alembic/.*',
        r'migrations/.*',
    ]
    
    # Extract filenames from diff
    files_touched = re.findall(r'diff --git a/(.*?) b/', diff_text)
    
    for file in files_touched:
        for pattern in risk_patterns:
            if re.match(pattern, file, re.IGNORECASE):
                return True
                
    return False
