FROM python:3.11-slim

ARG UID="1000" \
    GID="1000" \
    WORKDIR="/app" \
    GROUP="app" \
    USER="app"

RUN apt-get update && \
    apt-get install -y && \
    apt install redis-tools curl -y && \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR ${WORKDIR}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH /root/.local/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=false

RUN groupadd -g ${GID} -r ${GROUP} && \
    useradd -d ${WORKDIR} -g ${GROUP} -l -r -u ${UID} ${USER} && \
    chown ${USER}:${GROUP} -R ${WORKDIR}

COPY --chown=${USER}:${GROUP} pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY --chown=${USER}:${GROUP} . .

RUN ls

RUN chmod +x 'infra/backend/wait-for-it.sh' && \
    chmod +x 'infra/backend/entrypoint.sh'

USER ${USER}

EXPOSE 8000

ENTRYPOINT ["infra/backend/entrypoint.sh"]
