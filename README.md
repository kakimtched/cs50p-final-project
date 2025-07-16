# 🐍 CS50P Syllabus CLI Tool


> **Note:** This tool is a personal project created for learning purposes
> and is not an official CS50 product or affiliated with Harvard University.

---

## Description

This is my final project for CS50’s Introduction to Programming with Python.
It’s a simple command-line tool that lets you browse the CS50P syllabus right from your terminal.
It fetches and caches the course webpage, then displays either a list of all weeks or detailed info about a specific one.
The output is styled using rich, and you're greeted by a fun cowsay message when you start the tool.

I built this project to practice working with web requests, parsing HTML, caching files, handling command-line arguments, and creating clear, user-friendly terminal output.

---

## How It Works

When you run the program, it does the following:

1. Checks if a cached version of the syllabus exists and is still valid (6-hour limit).
2. If not, it downloads the syllabus from the CS50P website.
3. Parses the HTML using BeautifulSoup to extract week titles and links.
4. Displays the results in the terminal with clean formatting, including **clickable links** that open the corresponding web pages in your default browser.

You can either list all the weeks or show details for one specific week.

---

## How to Use

To get started, **clone the repository**:

```bash
git clone https://github.com/kakimtched/cs50p-final-project.git
cd cs50p-final-project
pip install -r requirements.txt
```

To list all course weeks:

```bash
python project.py --list
```

To see details for a specific week (for example, week 3):

```bash
python project.py --week 3
```

---

## Files

- `project.py`: The main Python script that runs the program.
- `cs50p_cache.html`: The cache file that stores a local copy of the syllabus. It is created automatically the first time the syllabus is fetched.
- `requirements.txt`: Lists all required Python packages.
- `README.md`: This file.
