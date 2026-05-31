# Sticker-Bot

A Telegram bot that helps a teacher track reward stickers for students.
This repository is a **teaching template**: the plumbing is done for you, and
you write each command in its own small file.

## What you build

| Command        | What it should do                                   | Status                  |
| -------------- | --------------------------------------------------- | ----------------------- |
| `/help`        | Reply with a short description of the bot           | scaffold (you fill in)  |
| `/addstudent`  | Ask for a name, then save a new student             | **worked example**      |
| `/award`       | Pick a student (buttons), pick an amount, add it    | scaffold (you fill in)  |
| `/leaderboard` | Show all students sorted by sticker count           | scaffold (you fill in)  |

`/addstudent` is fully written for you as a worked example — copy its style for
the others. Every command, including multi-step ones, is plain top-to-bottom
code using the `ctx.say()` / `ctx.ask()` / `ctx.choose()` helpers (see below).
No `async`/`await`, no states to manage.

## Where you write code

You only edit the files in **`Code/commands/`** — one file per command. Each
file has `# TODO` steps with hints. Fill them in!

```
Code/
  index.py            # start-up wiring — you don't need to touch this
  bot/
    framework.py      # the mini-framework — you don't need to touch this
    storage.py        # database functions — ready to use, no changes needed
  commands/           # ← YOU WORK HERE
    help.py
    addstudent.py     # finished example — copy this style
    award.py
    leaderboard.py
  examples/           # learning material — read these, run them on their own
    conversation_example.py
    README.md
```

## The 3 tools you use in a command

Every command receives `ctx` ("the conversation"). It gives you:

```python
ctx.say("some text")            # send a message
name = ctx.ask("Your name?")    # ask, then wait for a typed reply
pick = ctx.choose("Pick:", [1, 2, 3])   # show buttons, wait for a tap
```

For `choose`, you can show nice labels for objects:

```python
students = storage.list_students()
student = ctx.choose("Select student:", students, label=lambda s: s.name)
```

## Saving and reading data (the storage layer)

`Code/bot/storage.py` is finished for you. Import it and call its functions:

```python
from bot import storage

student = storage.add_student("John Smith")   # add a student
total   = storage.award_stickers(student.id, 2)  # add stickers, get new total
all     = storage.list_students()             # everyone (sorted by name)
board   = storage.get_leaderboard()           # everyone (sorted by stickers)
one     = storage.get_student(student.id)     # a single student, or None
```

Each `Student` has `.id`, `.name`, and `.sticker_count`. Data is saved in an
SQLite file under the data folder, so it survives bot restarts.

## Adding a brand-new command

1. Create a new file in `Code/commands/`, e.g. `Code/commands/remove.py`.
2. Write:

   ```python
   from bot.framework import command

   @command("remove", description="Remove a student")
   def remove(ctx):
       ctx.say("TODO: write me!")
   ```

3. Restart the bot. That's it — the framework finds the file automatically.

> By default commands are **teacher-only**. Add `teacher_only=False` to let
> anyone use a command (like `/help` and `/leaderboard`).

## Running it locally

You need a bot token from [@BotFather](https://t.me/BotFather) and Python 3.10 or
newer — including the very latest release.

> **Which Python?** Any recent Python 3 (3.10+) works, including the newest one,
> because `pyTelegramBotAPI` is pure Python with no compiled dependencies. The
> production Docker image uses 3.12; if you want your local setup to match it
> exactly, add `--python 3.12` to the `uv venv` command below.

### Recommended: [uv](https://docs.astral.sh/uv/)

`uv` is a fast, all-in-one Python tool. It creates the virtual environment and
installs the dependencies for you — no extra config files needed. Install it
once with `brew install uv` (or `curl -LsSf https://astral.sh/uv/install.sh | sh`),
then:

```bash
# 1. Create a virtual environment (uses your default Python)
uv venv

# 2. Install dependencies into that environment
uv pip install -r requirements.txt

# 3. Run the bot
BOT_TOKEN="123:abc" .venv/bin/python Code/index.py
```

> **Using the fish shell?** The `VAR=value command` form above is bash/zsh only.
> In fish, run step 3 as:
> ```fish
> env BOT_TOKEN=123:abc .venv/bin/python Code/index.py
> ```

Stop the bot with `Ctrl+C`. After the first setup you only need step 3 to start
it again.

### Alternative: plain venv + pip

If you already have Python installed and would rather not use uv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
BOT_TOKEN="123:abc" python Code/index.py
```

### Options

Set `TEACHER_ID` to your own Telegram user id to lock management commands to just
you (e.g. `BOT_TOKEN=... TEACHER_ID=... .venv/bin/python Code/index.py`). Leave it
unset while testing.

Deployment (Docker + GitHub Actions + Portainer) is already configured — see
`docker-compose.yml` and `.github/workflows/deploy.yml`.
