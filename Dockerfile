FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV VENV_PATH=/opt/venv
ENV BOT_TOKEN=$BOT_TOKEN
ENV POSTGRES_DSN=$POSTGRES_DSN
ENV MASTERS_URLS=$MASTERS_URLS


RUN groupadd --gid 2000 python
RUN useradd --uid 2000 --gid python --shell /usr/sbin/nologin --create-home python

RUN apt-get update
RUN pip install --no-cache-dir poetry

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --all-groups --no-install-project

RUN apt-get remove -y gcc cmake make libc-dev-bin libc6-dev \
    && rm -rf /var/lib/apt/lists/* ~/.cache \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /etc/apt/auth.conf

RUN ROOTDIRS=$(find / -maxdepth 1 -mindepth 1 \( -type d -o -type l \)  ! -name builds ! -name busybox ! -name dev ! -name etc ! -name kaniko ! -name proc ! -name sys ! -name tmp ! -name var ! -name workspace) \
    && mkdir -p /rootfs/dev /rootfs/proc /rootfs/run /rootfs/tmp \
    && cp -ax /etc/ /var /rootfs \
    && rm -rf /rootfs/var/run \
    && mv $ROOTDIRS /rootfs/


FROM scratch AS runtime-image

ENV LANG="C.UTF-8" \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/srv/www/
WORKDIR $WORKDIR

COPY --from=builder /rootfs/ /
COPY . .

RUN chown python:python /srv /tmp -R
USER python:python