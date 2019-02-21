**Progress is being made towards 0.1.0 - if you are interested in contributing, please check out our open issues. Pull requests that pass review are accepted, and work is being done on specific guidelines for contributing, but don't let that stop you.**

lamia
=====

Distributed blogging, polls, and status updates powered by activitypub, python, the gay agenda, and snake women.

**Project Status:** currently in rapid development.

**Interested in joining the core team? Show us what you can do.**

Documents
---------

* [Philosophy](docs/philosophy.md) - general project philosophy
* [Roadmap](docs/roadmap.md) - current project roadmap, basically a (hopeful) timeline
* [Goals](docs/goals.md) - current project goals and ambitions
* [Code](docs/code.md) - code standards, please read if you want to contribute
* [Glossary](docs/glossary.md) - dictionary for project terms

Primary Team
------------

* [scarly](https://computerfairi.es/@scarly) - project manager, lead developer
* [maple](https://computerfairi.es/@maple) - layouts, css, admin insights
* [Chel](https://computerfairi.es/@Chel) - interface design, user experience, project secretary

Installation Instructions
-------------------------

We'll clean these up later on, but for now this is as good as it gets.

### Requirements

* Python 3.7+
* PostgreSQL

### Create a config file

This file should be named `lamia.config`. The contents are just environment variables.
[Click here](docs/configuration.md) if you want to know more about these options, or the other options that can be set.

```
DB_ECHO=False
DB_DSN="postgresql://user:password@hostname/database"
SITE_NAME="A Lamia Social"
BASE_URL="http://your_hostname"
SECRET_KEY=your_secret_key
TEMPLATE_RELOAD=True
```

### Steps

1. Go to the place you want to install lamia: `cd /the/place/you/want/to/put/lamia`
2. Download the current repository: `git clone https://github.com/Scarly-Cat/lamia.git`
3. Enter the lamia directory: `cd lamia`
4. Grab the requirements (may be pip3 depending on your python version): `pip install requirements.txt`
5. Hopefully the above works.
6. Run `./lamia-cli build-babel` to initalize the translations system
7. `pip install uvicorn`
8. `uvicorn lamia:app`

Other Contributors
------------------

* [MrsRemi](https://www.deviantart.com/mrsremi) - created the first drawing of [Lamilia](docs/Lamilia.png)
* [Nuclear Baked Potato](https://cybre.space/@TheHottestPotato) - general co-conspirator, developer, tasty root vegetable, documentation wrangler
