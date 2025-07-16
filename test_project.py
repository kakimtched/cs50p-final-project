import sys
from pathlib import Path
from project import (
    fetch_html,
    extract_weeks,
    load_cache,
    save_cache,
    parse_arguments,
    display_week,
    display_week_clickable,
    print_cowsay_welcome,
)

CACHE_FILE = Path("cs50p_cache.html")


def test_fetch_html_success():
    html = fetch_html("https://cs50.harvard.edu/python/2022/weeks/")
    assert html is not None
    assert "<html" in html


def test_fetch_html_fail():
    html = fetch_html("https://thisdoesnotexist.booomboom")
    assert html is None


def test_extract_weeks_none():
    assert extract_weeks(None) is None


def test_extract_weeks_bad_html():
    bad_html = "<html><body>No syllabus here</body></html>"
    assert extract_weeks(bad_html) is None


def test_extract_weeks_good_html():
    html = """
    <main class="col-lg">
        <ol>
            <li><a href="/w0">Func</a></li>
            <li><a href="/w1">Vars</a></li>
        </ol>
    </main>
    """
    weeks = extract_weeks(html)
    assert weeks is not None
    assert len(weeks) == 2
    assert weeks[0] == (0, "Func", "/w0")
    assert weeks[1] == (1, "Vars", "/w1")


def test_save_and_load_cache():
    content = "<html>cached content</html>"
    save_cache(content)
    loaded = load_cache()
    assert loaded == content

    CACHE_FILE.unlink()


def test_parse_args_list():
    sys.argv = ["project.py", "--list"]
    args = parse_arguments()
    assert args.list is True
    assert args.week is None


def test_parse_args_week():
    sys.argv = ["project.py", "--week", "1"]
    args = parse_arguments()
    assert args.week == 1
    assert args.list is False


def test_display_week_runs():
    display_week(1, "Test Week", "http://example.com")


def test_display_week_no_url():
    display_week(2, "No URL")


def test_display_week_clickable():
    display_week_clickable(3, "Clickable Week", "http://example.com")


def test_print_cowsay_welcome():
    print_cowsay_welcome("Welcome Test")
