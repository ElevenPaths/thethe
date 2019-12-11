# The Threat Hunting Enviroment

## Installation

First, clone this repository with:

```bash
git clone https://github.com/ElevenPaths/thethe.git
```

Last, build the images and run the containers

```bash
docker-compose up -d
```

You should see **thethe** in [http://localhost](http://localhost) after a :coffee:

## Default user

By default, there is only one user **admin** with password **admin**

Change the **admin** password as soon as you login into **thethe** the very first time.

---

## Database backups and restoration

Inside **utils** folder, there a couple of scripts that will let you dump and restore the database:

Make a backup

```bash
backup_thethe.sh
```

Restore from a backup

```bash
restore_thethe.sh <restoration_file>
```

---

## Development enviroment

If you want to collaborate with the project a development version is provided:

### Get the repository

```bash
git clone https://github.com/ElevenPaths/thethe.git
```

### Docker (don't forget your :coffee:)

```bash
docker-compose -f docker-compose_dev.yml up -d
```

### Run the frontend

```bash
cd frontend
npm install
npm run serve
```

---

## More info

Site: [https://thethe.e-paths.com](https://thethe.e-paths.com/)

License: [https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE](https://raw.githubusercontent.com/ElevenPaths/thethe/master/LICENSE)
