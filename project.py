from rich_argparse import RawDescriptionRichHelpFormatter
import argparse
import sys
import time
from pathlib import Path
import cowsay
import requests
from bs4 import BeautifulSoup
from rich.console import Console

# Exceptions are silenced intentionally to avoid overcomplicating error handling
# and to maintain simplicity in this project.

CS50P_URL = "https://cs50.harvard.edu/python/2022/weeks/"
CACHE_FILE = Path("cs50p_cache.html")
CACHE_EXPIRY = 6 * 60 * 60  # 21600 seconds / 6 hours cache duration

console = Console()


def fetch_html(url, timeout=10):
    """Fetch HTML from URL, or return None if failed."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def extract_weeks(html):
    """Parse syllabus HTML and return a list of (index, title, link).
    Return None if html is None or if parsing failed.
    """
    if not html:
        return None

    try:
        soup = BeautifulSoup(html, "lxml")
        main_content = soup.find("main", class_="col-lg")

        weeks = []
        for index, li in enumerate(main_content.find("ol").find_all("li")):
            title = li.a.get_text(strip=True)
            link = li.a["href"]
            weeks.append((index, title, link))
        return weeks

    except Exception:
        return None


def load_cache():
    """Load cached HTML if cache file exists and is still valid, else return None."""
    try:
        if not CACHE_FILE.exists():
            return None
        cache_age_seconds = time.time() - CACHE_FILE.stat().st_mtime
        if cache_age_seconds > CACHE_EXPIRY:
            return None
        return CACHE_FILE.read_text(encoding="utf-8")
    except OSError:
        return None


def save_cache(html):
    """Save HTML content to cache file, return None if failed."""
    try:
        CACHE_FILE.write_text(html, encoding="utf-8")
    except OSError:
        pass


def parse_arguments():
    """Parse CLI arguments with mutually exclusive group and require one."""
    script = Path(sys.argv[0]).name

    parser = argparse.ArgumentParser(
        usage=argparse.SUPPRESS,
        description=(
            "🐍 [bold green]CS50P Syllabus CLI Tool[/bold green]\n\n"
            "Usage:\n"
            f"  - list all weeks:        python {script} --list\n"
            f"  - show a specific week:  python {script} --week <WEEK_NUM>\n"
            "\n"
        ),
        formatter_class=RawDescriptionRichHelpFormatter,
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-w", "--week", type=int, help="show details for a specific week"
    )
    group.add_argument("-l", "--list", action="store_true", help="list all weeks")

    if len(sys.argv) == 1:
        console.print()
        parser.print_help()
        console.print()
        sys.exit(0)

    return parser.parse_args()


def display_week(index, title, url=None):
    """Print the week index and title, print URL if given."""
    console.print(f"[yellow]{index}.[/yellow] {title}")
    if url:
        console.print(url)
    console.print()


def display_week_clickable(index, title, url):
    console.print(f"[yellow]{index}.[/yellow] [link={url}]{title}[/link]")
    console.print()


def print_cowsay_welcome(msg="Welcome to CS50P!"):
    cow_output = cowsay.cowsay(msg, "eyes")
    lines = cow_output.split("\n")

    speech_end = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("-------"):
            speech_end = i
            break

    speech_lines = lines[: speech_end + 1]
    cow_lines = lines[speech_end + 1 :]

    for line in speech_lines:
        console.print(line)
    for line in cow_lines:
        console.print(f"[bold green]{line} [/bold green]")


def main():
    """
    Main entry point for the CS50P Syllabus CLI Tool.

    - Parses command-line arguments.
    - Loads syllabus HTML from cache if available, otherwise fetches from the web.
    - Extracts week titles and links.
    - Shows either a list of all weeks or details for a selected week.
    - Handles errors and prints user-friendly messages.
    """
    try:
        args = parse_arguments()

        console.print(
            "\n🐍 [bold green]CS50’s Introduction to Programming with Python[/bold green]\n"
        )

        print_cowsay_welcome()

        html = load_cache()
        if not html:
            with console.status(
                "[bright_green]Loading syllabus...[/bright_green]", spinner="dots"
            ):
                html = fetch_html(CS50P_URL)
                if html:
                    save_cache(html)

        if not html:
            console.print("[bold red]Failed to fetch syllabus:[/bold red]\n")
            sys.exit(1)

        weeks = extract_weeks(html)
        if not weeks:
            console.print("[bold red]No weeks found. Exiting.[/bold red]\n")
            sys.exit(1)

        if args.list:
            console.print("[bold underline]Weeks[/bold underline]\n")
            for index, title, link in weeks:
                full_url = CS50P_URL + link
                display_week_clickable(index, title, full_url)
        elif args.week is not None:
            if 0 <= args.week < len(weeks):
                index, title, link = weeks[args.week]
                full_url = CS50P_URL + link
                console.print()
                display_week(index, title, full_url)
                console.print()
            else:
                console.print(
                    f"\n[bold red]invalid_week_number: expected 0 <= week <= {len(weeks) - 1}[/bold red]\n"
                )
                sys.exit(1)

    except Exception as e:
        console.print(f"\n[bold red]Try to fix this -> : [/bold red]{e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
