# Learning examples

Standalone code you can read and run to learn one idea at a time. These files
are **not** part of the bot — nothing here is loaded when the bot starts.

## `conversation_example.py` — asking a question and waiting for the answer

A bot conversation has steps: after `/hello` the bot waits for your **name**.
But a bot normally reacts to messages one at a time, so how does it know the
next message is the answer to its question?

pyTelegramBotAPI gives you one tool for this:

| Tool                                          | What it does                                              |
| --------------------------------------------- | --------------------------------------------------------- |
| `bot.register_next_step_handler(message, fn)` | "Send the NEXT message from this chat to `fn` instead."   |

That's the whole trick. You ask a question, then register the function that
should handle the reply.

### Run it

Get a token from [@BotFather](https://t.me/BotFather), then:

```bash
BOT_TOKEN="123:abc" python Code/examples/conversation_example.py
```

Send `/hello` to your bot and follow along.

## This vs. the `ctx.ask()` helper

The example above is the **raw** way: you split the conversation across two
functions (`start` asks, `got_name` handles the reply) and pass control between
them with `register_next_step_handler`.

The bot gives you a friendlier shortcut, `ctx.ask()` / `ctx.choose()`, that does
the same thing but lets you write the whole flow as simple top-to-bottom code:

```python
name = ctx.ask("Enter student name:")   # asks AND waits for the reply, in one line
ctx.say(f"Hello, {name}!")
```

See it in action in `Code/commands/addstudent.py` (the `/addstudent` command).
Start with `ctx.ask()` for your own commands — peek at this example only when
you're curious what it's doing underneath.
