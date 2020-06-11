# The Threat Hunting Environment

You are a Threat Hunter. While investigating, did you find yourself with more than 20 tabs opened in your browser, scattered .txt files with data and some terminals showing up in the background?

theTHE centralizes all the information on an investigation in a single project and shares its results with your team (and with nobody else). theTHE caches your API responses, so you don't need to repeat the requests. Don’t share your keys, let the users make calls to the services.

theTHE also contains some command-line tools integrated so you don't have to open a terminal and pipe the results in a .txt file.

Your feedback is welcome.

### What's new

See [releases](https://github.com/ElevenPaths/thethe/releases)

---

### Installation

There is a [**install.sh**](https://raw.githubusercontent.com/ElevenPaths/thethe/master/install.sh) script to ease installation. Either download and execute it by doing:

```bash
curl -sSL https://raw.githubusercontent.com/ElevenPaths/thethe/master/install.sh | bash
```

or clone this repository with:

```bash
git clone --recurse-submodules https://github.com/ElevenPaths/thethe
```

and inside **thethe** directory, move the install script one level up and execute it:

```bash
mv thethe/install.sh
./install.sh
```

You **MUST** have a .env file with the following structure in thethe root directory:

```bash
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
MONGO_INITDB_DATABASE=thethe
THETHE_SECRET=
```

- Select a **secure** user/pass/secret combination at your own for each value.
- Leave **MONGO_INITDB_DATABASE** with "thethe" value.

---

### Running thethe

Inside thethe directory:

```bash
./start.sh
```

Are you a developer?

```bash
./start dev
```

---

### API keys

There are not API keys stored by default on the system.

To add an API key, there is an option in the user menu (upper-right corner) to manage your keys.

---

### Database backups and restoration

Mongodb has a bind volume to ease external storage and backups in a folder **mongodb_data**

In any case, we have provided you with a couple of scripts to backup (a compressed file) and restore data from your mongo container.

Inside **utils** folder:

Make a backup

```bash
backup_thethe_db.sh
```

Restore from a backup

```bash
restore_thethe_db.sh
```

backup filename is **db.dump.gz**

---

### External storage

There is a folder called **external** for everything theTHE should store outside a database: files, images, etc.

Backup this folder according to your backup policy.

---

### Updating thethe

See [updating thethe](https://github.com/ElevenPaths/thethe/wiki/How-to-update-thethe)

---

### Development environment

If you want to collaborate with the project, a development version is provided:

Get the repositories:

```bash
git clone --recurse-submodules https://github.com/ElevenPaths/thethe.git
```

and only for the first time...

```bash
cd thethe_frontend
npm install
cd ..
```

Now you have a dev environment. Every time you need to code, just run thethe with:

```bash

./start.sh dev

```

---

### More info

Website: [https://thethe.e-paths.com](https://thethe.e-paths.com/)

License: [https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE](https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE)
