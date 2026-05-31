# Learning examples

Standalone code you can read and run to learn one idea at a time. These files
are **not** part of the bot — nothing here is loaded when the bot starts.

## `conversation_example.py` — remembering what you're waiting for (a tiny FSM)

A bot conversation has steps: after `/hello` the bot waits for your **name**. But
a bot reacts to messages one at a time, so how does it know the next message is
the answer? It has to **remember which step the chat is on**.

That memory is a finite state machine (FSM), and in the example it is just one
dictionary:

```python
states = {chat_id: "awaiting_name"}
```

| Step                     | What the next message means |
| ------------------------ | --------------------------- |
| (no step)                | maybe a command like /hello |
| `awaiting_name`          | the person's name           |

`/hello` sets the step to `awaiting_name`; the second handler runs only while the
chat is on that step, so it knows the message is the answer, then clears the step.

### Run it

Get a token from [@BotFather](https://t.me/BotFather), then:

```bash
BOT_TOKEN="123:abc" python Code/examples/conversation_example.py
```

Send `/hello` to your bot and follow along. Add `print(states)` inside the
handlers to literally watch the machine change step.

## This vs. the real bot

The example keeps its `states` dict right there in the file so you can see every
gear. The bot does the exact same thing, just tidied into reusable helpers in
[`Code/bot/fsm.py`](../bot/fsm.py) — `set_state`, `get_state`, `set_data`,
`get_data`, `clear`, and `waiting_for`. See them used in the worked
[`Code/commands/addstudent.py`](../commands/addstudent.py).
