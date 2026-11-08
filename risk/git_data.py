import subprocess
from dataclasses import dataclass
from datetime import datetime

@dataclass 
class FileChange:
    path: str 
    added: int 
    deleted: int 

@dataclass
class CommitInfo:
    sha: str 
    author: str
    timestamp: datetime
#return the sha, author, and timestamp of a commit
def get_commit_info(repo: str, ref: str) -> CommitInfo:
    output = run_git(repo, "log", "-1", "--format=%H%n%an%n%aI", ref)
    sha, author, time_text = output.splitlines()
    timestamp = datetime.fromisoformat(time_text)
    return CommitInfo(sha, author, timestamp)

FIX_WORDS=["fix", "revert", "hotfix", "bug", "🐛"]

#return how many recent commits to a file look like fixes.
def get_fix_count(repo: str, path: str, since: str = "6 months ago") -> int:
    output = run_git(repo, "log", f"--since={since}", "--format=%s", "--", path)
    messages = output.splitlines()
    count = 0
    for message in messages:
        lowered = message.lower()
        if any(word in lowered for word in FIX_WORDS):
            count += 1
    return count 

#return a fix count for each changed file
def get_hotspots(repo: str, changes: list[FileChange]) -> dict:
    hotspots = {}

    for change in changes:
        hotspots[change.path] = get_fix_count(repo, change.path)
    return hotspots 

    

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


#return total files changed, lines added, and lines deleted
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