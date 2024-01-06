# Club Penguin seasonal content rotation

This project aims at adding an automatic scheduled content rotation for a Club Penguin Private Server (CPPS) with historic Club Penguin seasonal content, such as catalogues, parties, events and room configurations. It relies on [rsync](https://linux.die.net/man/1/rsync) and hardlinks for storing all seasonal content and synchronizing it with the live server, and provides an easy user interface for manually deploying any content through [Script Server](https://github.com/bugy/script-server). Only AS2 CPPS is supported at this time.

This repository contains JSON files for downloading assets from the Club Penguin Archive in order to setup a desired piece of content. It also uses [JPEXS Free Flash Decompiler](https://github.com/jindrapetrik/jpexs-decompiler) (FFDec) for patching certain files in order to allow overlay between different types of contents, and also to apply a few fixes.

## Setup

Requirements:

- Python 3.10+
- Docker

This setup consists of first downloading the desired assets from the JSON source files, followed by a live media server setup, and then setting up the Script Server as both the scheduler for continuously deploying the content as well as the user interface for on-demand deployments.

### Downloading assets

Some assets require applying some ActionScript patches to work properly with AS2 emulators, so the first step here is to build a local Docker image for running FFDec:

```sh
docker build -t jpexs ./jpexs
```

The download script assumes that a local copy of AS2 media `media` directory is available at `./legacy-media/media_original`. It will use it as a source for hardlinks and other references the other seasonal content. For instance, in order to transfer these files from a remote server `remote_server` to the expected directory with a `user`, rsync can be employed:

```sh
mkdir -p legacy-media/media_original
rsync -avh -H user@remote_server:/path/to/legacy-media/media/ ./legacy-media/media_original
```

After that, the download can commence. I recommend first download one collection of each type (i.e., catalog, party, stage play, etc) before attempting to download all, if desired at all. All download sources are available at `assets` directory, which is what is needed to execute the Python script:

```sh
python3 download.py assets/handcrafted/base.json
python3 download.py <assets/path/some_file.json>
```

Make sure to download run the `base.json` file, as that is required for resetting the media server state.

### Media server setup

Once all the desired assets have been downloaded and patched, they need to be transferred to the live media server, if this was not run there already. Again, this can be accomplished by a few rsync commands:

```sh
rsync -avh -H legacy-media/base/ user@remote_server:/path/to/legacy-media/base
rsync -avh -H legacy-media/catalogs/ user@remote_server:/path/to/legacy-media/catalogs
rsync -avh -H legacy-media/rooms/ user@remote_server:/path/to/legacy-media/rooms
rsync -avh -H legacy-media/events/ user@remote_server:/path/to/legacy-media/events
rsync -avh -H legacy-media/parties/ user@remote_server:/path/to/legacy-media/parties
```

Then, make a hardlinked copy of media server's `legacy-media/media` to `legacy-media/media_original` to preserve the base content and setup the live directory for updates with rsync:

```sh
# On remote_server
cp -rl /path/to/legacy-media/media /path/to/legacy-media/media_original
```

### Running Script Server

Finally, all that's left is run the Script Server on the media server to enable scheduled and on-demand seasonal content updates.

This repository provides a working `docker-compose.yml` to deploy the Script Server all set. If that's a feasible approach for deployment to the media server, then simply cloning this repository on there, copying the sample files to the real destination with the following commands, then edited them as desired:

```sh
cp script_server/.htpasswd.sample script_server/.htpasswd
cp script_server/scripts/schedules.json.sample script_server/scripts/schedules.json
```

The default login is `admin` with password `admin`. To redefine its password, use `htpasswd .htpasswd admin`. Edit `schedules.json` following the example at the sample file to define the schedules for the seasonal content.
