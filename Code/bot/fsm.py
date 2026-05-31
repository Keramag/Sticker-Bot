"""A tiny finite state machine (FSM) for multi-step conversations.

A conversation has STEPS. After `/addstudent` the bot is "waiting for a name";
once the name arrives it goes back to "no step at all". A bot normally reacts to
every message the same way, so it needs to remember, for each chat:

    1. which step the chat is on   -> the STATE   (a short text label)
    2. any answers collected so far -> the DATA    (a little dict)

That is the WHOLE machine: two dictionaries and a few helper functions. Nothing
is hidden — you can literally `print(_states)` to watch it change. Picture it as
a diagram:

        /addstudent            (teacher types a name)
   no step ----------> awaiting_name ----------> no step
        set_state(...)                  clear(...)

How you use it in a command file:

    from bot import bot
    from bot.fsm import set_state, waiting_for, clear

    @bot.message_handler(commands=["addstudent"])
    def addstudent(message):
        bot.send_message(message.chat.id, "Enter student name:")
        set_state(message.chat.id, "awaiting_name")   # move to the next step

    # This handler runs ONLY when the chat is on the "awaiting_name" step.
    @bot.message_handler(func=lambda m: waiting_for(m, "awaiting_name"))
    def got_name(message):
        ...                                            # message.text IS the name
        clear(message.chat.id)                         # conversation finished
"""

# chat_id -> the step this chat is on, e.g. "awaiting_name".
# A chat that is missing from here is not in any conversation.
_states: dict[int, str] = {}

# chat_id -> answers gathered during the conversation, e.g. {"student_id": 4}.
_data: dict[int, dict] = {}


def set_state(chat_id: int, state: str) -> None:
    """Move this chat onto a step (a state)."""
    _states[chat_id] = state


def get_state(chat_id: int) -> str | None:
    """Which step is this chat on? None means 'not in a conversation'."""
    return _states.get(chat_id)


def set_data(chat_id: int, key: str, value) -> None:
    """Remember one answer to use in a later step (e.g. the chosen student)."""
    _data.setdefault(chat_id, {})[key] = value


def get_data(chat_id: int, key: str):
    """Read back an answer saved earlier in this conversation (or None)."""
    return _data.get(chat_id, {}).get(key)


def clear(chat_id: int) -> None:
    """Conversation finished (or cancelled): forget this chat's step and data."""
    _states.pop(chat_id, None)
    _data.pop(chat_id, None)


def waiting_for(message, state: str) -> bool:
    """True when this chat is on `state` AND the message is a normal reply.

    Use it in a handler's `func=` to catch the reply for a step:

        @bot.message_handler(func=lambda m: waiting_for(m, "awaiting_name"))

    A message that starts with "/" is a new command, not an answer, so we let it
    fall through to its own command handler instead of treating it as the reply.
    """
    if (message.text or "").startswith("/"):
        return False
    return get_state(message.chat.id) == state
