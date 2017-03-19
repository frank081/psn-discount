# psn-discount
Psn Game Crawler

## Run

### Daemon

```
docker run --name psn-discount -d -v $HOME/.ssh:/home/runtime/.ssh --restart=always lidejia/psn-discount:latest
```

### Onetime

```
docker run -it --rm -v $HOME/.ssh:/home/runtime/.ssh --user runtime --entrypoint=./Crontab/psn.sh lidejia/psn-discount:latest
```
