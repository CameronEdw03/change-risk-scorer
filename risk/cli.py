import click
from risk.git_data import get_changed_files, get_commit_info, get_hotspots, summarize

@click.command()
@click.option("--repo", default=".", help="Path to the git repo to analyze.")
@click.option("--base", required=True, help="Commit to compare against, e.g. HEAD~5 or main.")
@click.option("--head", default="HEAD", help="Commit with the changes.")
def main(repo, base, head):
    changes = get_changed_files(repo, base, head)
    summary = summarize(changes)
    commit = get_commit_info(repo, head)

    click.echo(f"Commit:  {commit.sha[:7]} by {commit.author}")
    click.echo(f"When:    {commit.timestamp.strftime('%A %H:%M')}")
    click.echo(f"Size:    {summary['files']} files, +{summary['added']} / -{summary['deleted']} lines")

    hotspots = get_hotspots(repo, changes)

    click.echo("")
    click.echo("Hotspots (fix commits in last 6 months):")
    for path, count in sorted(hotspots.items(), key=lambda item: item[1], reverse=True):
        if count > 0:
            click.echo(f"   {path:<40} {count}")

 


if __name__ == "__main__":
    main()
