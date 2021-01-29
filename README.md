# mkBot

A multipurpose IRC bot.

## Configuration

In order for the bot to run, a ``config.ini`` file must be created in the [data](data) directory, and must contain the
following sections and options:

```ini
[bot]
server = xyz
port = xyz
nick = xyz
pass = xyz

[esix]
agent = xyz
name = xyz
key = xyz
```

## Channels

To choose which channels to connect to, create a ``channels.ini`` in the [data](data) directory with the following
structure.

```ini
[#channelName01]
[#channelName02]
[#channelName03]
```

It can have as many channels as you like, but they must include a ``#`` at the beginning of the name. 