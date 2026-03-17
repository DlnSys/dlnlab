In order to use the kraken Docker, you can first build it with `make build`
(which uses the `docker compose` plugin) and then execute `make exec` to get a shell inside
it.

The current host folder will be mounted in the container `/app` folder, so that you can add
your own files and interact with them.

