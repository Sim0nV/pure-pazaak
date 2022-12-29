<p align="center"><img src="https://user-images.githubusercontent.com/78996965/206857624-98aba1e4-3e8b-414f-ba25-2283d549ffb4.png" width="175" height="175"></a></p>

<h1 align="center">Pure Pazaak</h1>
<p align="center"></p>
<h3 align=center>A recreation of the card game Pazaak from Star Wars: Knights of the Old Republic</br>Built with <a href=https://github.com/Rapptz/discord.py>discord.py</a></h3>

---

<p align="center">
  <a href="https://discord.com/api/oauth2/authorize?client_id=855632523060707378&permissions=274914659328&scope=bot%20applications.commands">
     <img src="https://img.shields.io/static/v1?label=Invite%20Me&message=Pure%20Pazaak%232096&plastic&color=5865F2&logo=discord">
  </a>
  <a href="https://www.python.org/">
     <img src="https://img.shields.io/badge/python-3.9.5-blue" alt="Python: 3.9.5">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
  </a>
  <a href="https://www.codefactor.io/repository/github/sim0nv/pure-pazaak">
    <img src="https://www.codefactor.io/repository/github/sim0nv/pure-pazaak/badge" alt="Codefactor Grade">
  </a>
  <a href="https://github.com/Sim0nV/pure-pazaak/blob/master/LICENSE.txt">
      <img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License: AGPL-3.0">
  </a>
</p>

<p align="center">
  <a href="#-features">Features</a>
  •
  <a href="#-dependencies">Dependencies</a>
  •
  <a href="#%EF%B8%8F-configuration">Configuration</a>
  •
  <a href="#%EF%B8%8F-self-hosting">Self-Hosting</a>
  •
  <a href="#%EF%B8%8F-self-hosting">Usage</a>
</p>

## 🃏 Features

<p align="center">
  <a href="https://streamable.com/enoapv">
  <img src="https://user-images.githubusercontent.com/78996965/207284997-cfa944d8-aad9-4bf8-a1ed-0c2375fae55a.gif">
</p>
<p align="center">
  <a href="https://streamable.com/enoapv">
  Check out our launch trailer to see these features in action!
</p>

- Pazaak matches between users, sent through DMs to hide player cards
- Match spectating via server channel embed
- Randomized embed thumbnails
- Toggleable match sound effects
- Saves user and match stats to MongoDB
- The following commands:

| Command                                | Action                                                                                                    |
| :------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| `/pazaak [<@user>]`</br>`$p [<@user>]` | Challenges the mentioned user to a Pazaak match or shows usage embed                                      |
| `/rules`</br>`$pazaak_rules`           | DMs the Pazaak ruleset                                                                                    |
| `/sfx`</br>`$pazaak_sfx`               | Toggles Pazaak sound effects                                                                              |
| `/stats [<@user>]`</br>`$ps [<@user>]` | Displays the stats of yourself or the mentioned user,</br>including your match record with mentioned user |
| `/help`</br>`$pazaak_help`             | Shows a complete list of commands for Pure Pazaak                                                         |
| `/acknowledgements`                    | Outputs credits and special thanks                                                                        |

## 📄 Dependencies

- [Python 3.9.5](https://www.python.org/)
- [discord.py 2.1.0 (with Voice Support)](https://github.com/Rapptz/discord.py)
- [Motor 3.1.1](https://github.com/mongodb/motor)
- [python-dotenv 0.21.0](https://github.com/theskumar/python-dotenv)
- [ffmpeg 5.1.2](https://ffmpeg.org/)

Dependencies may be installed by running:

```
$ pip install -r requirements.txt
```

## ⚙️ Configuration

Pure Pazaak is configurable with the following environment variables:

- **`IS_DEBUG_MODE`**: If set to `True` the bot uses the `DEV_BOT_TOKEN` environment variable to run, refers to the `DEV_DB_COLLECTION` for the database, sets log level to `INFO`, and allows players to challenge themselves. Otherwise, if set to `False`, the bot uses the respective `PROD_...` environment variables.<br/>
  Default: `False`

- **`SHOULD_SYNC_COMMANDS`**: If set to `True` the bot will sync app commands. If `False`, it will skip syncing.<br/>
  Default: `False`

## 🖥️ Self-Hosting

Create a Discord app through the [developer portal](https://discord.com/developers/applications),
then create a `.env` file in the root using `.env.example` as reference.

The public Pure Pazaak bot uses images, gifs, sounds, and a database,
but the bot will still run without needing to include those in the `.env` file!
See `.env.barebones.example` for an example `.env` file which will run with just the bot token.

## ▶️ Usage

Once the dependencies are installed and the `.env` is properly configured, run the bot using:

```
$ python main.py
```
