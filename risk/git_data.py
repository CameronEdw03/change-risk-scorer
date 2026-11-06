import subprocess



#Run a git command inside `repo` and return its output as text.
def run_git(repo: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout