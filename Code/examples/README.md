# Learning examples

Standalone code you can read and run to learn one idea at a time. These files
are **not** part of the bot — nothing here is loaded when the bot starts.

## `fsm_example.py` — Finite State Machines (FSM)

A bot conversation has steps: after `/hello` the bot waits for your **name**.
That "waiting for…" situation is a **state**, and the bot moves between states.
That collection of states and the moves between them is a **Finite State
Machine**.

aiogram gives you the building blocks:

| Tool                              | What it does                                 |
| --------------------------------- | -------------------------------------------- |
| `class X(StatesGroup)` + `State()`| Name the steps of the conversation           |
| `await state.set_state(X.step)`   | Move the user into a step                     |
| `@router.message(X.step)`         | A handler that runs *only* during that step   |
| `await state.clear()`             | End the conversation, forget the state        |

### Run it

Get a token from [@BotFather](https://t.me/BotFather), then:

```bash
pip install -r requirements.txt
BOT_TOKEN="123:abc" python Code/examples/fsm_example.py
```

Send `/hello` to your bot and follow along.

> **Going further:** for a flow with several steps you can carry answers from
> one step to the next with `await state.update_data(name=...)` and
> `await state.get_data()`. Skip this until you're comfortable with the basics.

## FSM vs. the `ctx.ask()` helper

This project gives you a shortcut, `ctx.ask()` / `ctx.choose()`, that lets you
write multi-step flows as simple top-to-bottom code without thinking about
states. That's great for getting started.

FSM is the **standard, lower-level way** every aiogram project uses. It's more
code, but it scales to complicated flows and is what you'll see in real
projects and tutorials online.

See both side by side:
- **`ctx.ask()` style:** `Code/commands/award.py`, `Code/commands/leaderboard.py`
- **Real FSM style:** `Code/commands/addstudent.py` (the `/addstudent` command)
