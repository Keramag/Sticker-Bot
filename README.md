# Sticker-Bot

A Telegram bot that helps a teacher track reward stickers for students.
This repository is a **teaching template**: the plumbing is done for you, and
you write each command in its own small file.

## What you build

| Command        | What it should do                                   | Status                  |
| -------------- | --------------------------------------------------- | ----------------------- |
| `/help`        | Reply with a short description of the bot           | scaffold (you fill in)  |
| `/addstudent`  | Ask for a name, then save a new student             | **worked FSM example**  |
| `/award`       | Pick a student (buttons), pick an amount, add it    | scaffold (you fill in)  |
| `/leaderboard` | Show all students sorted by sticker count           | scaffold (you fill in)  |

There are two ways to write a multi-step conversation here. `/addstudent` is a
finished example of the **real aiogram FSM** way; the others use the simpler
`ctx.ask()` / `ctx.choose()` helpers. Start with `Code/examples/` to learn FSM
on its own, then compare it with `Code/commands/addstudent.py`.

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
    addstudent.py     # finished example, written with a real aiogram FSM
    award.py
    leaderboard.py
  examples/           # learning material — read these, run them on their own
    fsm_example.py
    README.md
```

## The 3 tools you use in a command

Every command receives `ctx` ("the conversation"). It gives you:

```python
await ctx.say("some text")            # send a message
name = await ctx.ask("Your name?")    # ask, then wait for a typed reply
pick = await ctx.choose("Pick:", [1, 2, 3])   # show buttons, wait for a tap
```

For `choose`, you can show nice labels for objects:

```python
students = storage.list_students()
student = await ctx.choose("Select student:", students, label=lambda s: s.name)
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
   async def remove(ctx):
       await ctx.say("TODO: write me!")
   ```

3. Restart the bot. That's it — the framework finds the file automatically.

> By default commands are **teacher-only**. Add `teacher_only=False` to let
> anyone use a command (like `/help` and `/leaderboard`).

## Running it locally

You need a bot token from [@BotFather](https://t.me/BotFather) and **Python 3.12**.

> **Why 3.12 and not the newest Python?** The pinned `aiogram 3.13.1` depends on
> `pydantic-core`, which only ships prebuilt wheels up through Python 3.12. On
> newer versions (e.g. 3.14) installation falls back to compiling from Rust
> source and fails. 3.12 also matches the production Docker image, so local
> behaves like prod.

### Recommended: [uv](https://docs.astral.sh/uv/)

`uv` is a fast, all-in-one Python tool. It creates the virtual environment and
installs the dependencies for you — no extra config files needed. Install it
once with `brew install uv` (or `curl -LsSf https://astral.sh/uv/install.sh | sh`),
then:

```bash
# 1. Create a virtual environment with Python 3.12 (uv downloads it if you don't have it)
uv venv --python 3.12

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

If you already have Python 3.12 installed and would rather not use uv:

```bash
python3.12 -m venv .venv
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
