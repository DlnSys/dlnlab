FROM ubuntu:22.04
WORKDIR /app/
RUN apt-get update                              && \
    apt-get install -qy --no-install-recommends    \
        libc6=2.35-0ubuntu3.9                      \
        socat=1.7.*                             && \
    apt-get clean                               && \
    rm -rf /var/lib/apt/lists/                  && \
    useradd ctf
COPY --chown=ctf:ctf --chmod=500 ./public/editeur-de-configuration ./
COPY --chown=ctf:ctf --chmod=400 ./src/flag.txt ./
EXPOSE 4000
USER ctf
CMD ["socat", "tcp-listen:4000,reuseaddr,fork", "exec:'/app/editeur-de-configuration'"]
