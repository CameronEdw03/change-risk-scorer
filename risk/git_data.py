import subprocess
from dataclasses import dataclass

@dataclass 
class FileChange:
    path: str 
    added: int 
    deleted: int 



#return each file changed between base and head with line counts
def get_changed_files(repo: str, base: str, head: str) -> list[FileChange]:
    output = run_git(repo, "diff", "--numstat", f"{base}...{head}")
    changes = []
    for line in output.splitlines():
        added, deleted, path = line.split("\t", 2)
        if added == "-": 
            added, deleted = "0", "0"
        changes.append(FileChange(path, int(added), int(deleted)))
    return changes


#retun total files changed, lines. added, and lines deleted
def summarize(changes: list[FileChange]) -> dict:
    file_count = len(changes)
    total_added = 0
    total_deleted = 0

    for change in changes: 
        total_added += change.added
        total_deleted += change.deleted

    return {"files": file_count, "added": total_added, "deleted": total_deleted}





#Run a git command inside `repo` and return its output as text.
def run_git(repo: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout