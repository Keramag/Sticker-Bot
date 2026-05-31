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
the others. Commands are plain [pyTelegramBotAPI](https://pytba.readthedocs.io/)
handlers (no `async`/`await`). Multi-step conversations use a tiny finite state
machine (FSM) that remembers which step each chat is on — it's just a dictionary,
and it lives in plain sight in `Code/bot/fsm.py`.

## Where you write code

You only edit the files in **`Code/commands/`** — one file per command. Each
file has `# TODO` steps with hints. Fill them in!

```
Code/
  index.py            # start-up wiring — you don't need to touch this
  bot/
    __init__.py       # creates the shared `bot` — you don't need to touch this
    fsm.py            # the tiny finite state machine — read it, it's ~25 lines
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

## How a command works

Each command file imports the shared `bot` and hangs a handler on it. The handler
receives the Telegram `message` and replies with `bot.send_message(...)`:

```python
from bot import bot

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, "Hi, I am a sticker tracking bot")
```

### Multi-step conversations (the FSM)

When a command needs more than one message (ask, then wait for the answer), use
the tiny FSM helpers from `bot/fsm.py` to remember the step:

```python
from bot import bot
from bot.fsm import set_state, waiting_for, clear

@bot.message_handler(commands=["addstudent"])
def addstudent(message):
    bot.send_message(message.chat.id, "Enter student name:")
    set_state(message.chat.id, "awaiting_name")     # move to the next step

# runs ONLY while the chat is on the "awaiting_name" step
@bot.message_handler(func=lambda m: waiting_for(m, "awaiting_name"))
def addstudent_got_name(message):
    bot.send_message(message.chat.id, f"Got {message.text}")
    clear(message.chat.id)                          # conversation finished
```

The full helper set is `set_state` / `get_state` / `set_data` / `get_data` /
`clear` / `waiting_for`. Use `set_data` / `get_data` to remember an answer across
steps (e.g. which student you picked in `/award`). For tappable buttons, see the
worked notes in `Code/commands/award.py`.

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
   from bot import bot

   @bot.message_handler(commands=["remove"])
   def remove(message):
       bot.send_message(message.chat.id, "TODO: write me!")
   ```

3. Add one line to `Code/index.py` so the file gets imported (that's what turns
   the command on): `import commands.remove`. Optionally add a `BotCommand` entry
   to `set_my_commands` so it shows in the "/" menu. Then restart the bot.

> Commands are open to everyone by default. To make one teacher-only, check at
> the top of the handler:
> ```python
> from bot import bot, is_teacher
>
> if not is_teacher(message.from_user.id):
>     bot.send_message(message.chat.id, "Teacher only.")
>     return
> ```
> (`/addstudent` and `/award` already do this; `/help` and `/leaderboard` don't.)

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
