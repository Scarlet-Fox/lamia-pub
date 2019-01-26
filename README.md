lamia
=====

Distributed blogging, polls, and status updates powered by activitypub, python, the gay agenda, and snake women.

**Project Status:** currently in rapid development.

* You may want to hold off on forking or making pull requests
* Everything is chaos
* lamia is a moving target
* Consider - too much activity will not help me finish ^_^;

**Interested in helping? Send a message to [Chel](https://computerfairi.es/@Chel)!**

Documents
---------

* [Philosophy](docs/philosophy.md) - general project philosophy
* [Roadmap](docs/roadmap.md) - current project roadmap, basically a (hopeful) timeline
* [Goals](docs/goals.md) - current project goals and ambitions
* [Code](docs/code.md) - code standards, please read if you want to contribute
* [Glossary](docs/glossary.md) - dictionary for project terms

Current Team
------------

* scarly - project manager, lead developer
* [Chel](https://computerfairi.es/@Chel) - interface design, user experience, project secretary

Installation Instructions
-------------------------

We'll clean these up later on, but for now this is as good as it gets.

### Requirements

* Python 3.7+

### Create a config file

This file should be named `lamia.config`. The contents are just environment variables.

```
DB_ECHO=False
DB_DSN="postgresql://user:password@database_address/database_table"
INSTANCE_NAME="A Lamia Social"
SECRET_KEY=your_secret_key
TEMPLATE_RELOAD=True
```

### Steps

1. Go to the place you want to install lamia: `cd /the/place/you/want/to/put/lamia`
2. Download the current repository: `git clone https://github.com/Scarly-Cat/lamia.git`
3. Enter the lamia directory: `cd lamia`
4. Grab the requirements (may be pip3 depending on your python version): `pip install requirements.txt`
5. Hopefully the above works.
6. `pip install uvicorn`
7. `uvicorn lamia:app`

Other Contributors
------------------

* [MrsRemi](https://www.deviantart.com/mrsremi) - created the first drawing of Lamilia

