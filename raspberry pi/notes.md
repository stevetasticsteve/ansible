
### Contract between
- index.html expects nginx.conf to redirect /clahub and /nextcloud
- Lexicon needs read access to spreadsheet managed by nextcloud. Achieving this by chmod'ing the docker volume and symlinking.
- Texts needs read access to nextcloud.

### Logs
- Lexicon_error log created upon error


Lexicon script (venv) needs access to /mnt/disk1/docker-data/volumes/nextcloud_data/_data/data/steve/files/'Team Share'/lexicon/Kovol_lexicon.ods
Texts script(venv) needs access to /mnt/disk1/docker-data/volumes/nextcloud_data/_data/data/steve/files/'Team Share'/lexicon/texts/
Nginx (container) needs access to /mnt/disk1/docker-data/volumes/nextcloud_data/_data/data/steve/files/'Team Share'/lexicon/texts/audio

/mnt/disk1/docker-data/volumes/nextcloud_data/_data/data keeps getting set to 750. Owner: www-data group: root
Needs to be 755

- sudo chmod command. Unreliable
- run scripts as root. texts and Lex already are
- run scripts as root group
- run scripts as www-data