# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Sets up Poetry environment variables and virtual environment
ENV POETRY_VERSION=1.8.3 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS builder
RUN --mount=type=cache,target=/root/.cache \
    pip install "poetry==$POETRY_VERSION"
WORKDIR /opt/pysetup
COPY ./poetry.lock ./pyproject.toml ./

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
    poetry install --no-dev
    
FROM base AS production
COPY --from=builder $VENV_PATH $VENV_PATH
# Switch to the non-privileged user to run the application.

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
    
RUN chown -R appuser:appuser $VENV_PATH
USER appuser

# Copy the source code into the container.
COPY ./t3 app/

WORKDIR /app

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
CMD ["/opt/pysetup/.venv/bin/streamlit", "run", "app.py"]

# so at it turns out the issue I was facing with the error "docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "streamlit": executable file not found in $PATH: unknown" is because docker couldn't find my streamlit executable which was installed in my virtual environment path which is 'opt/pysetup/.venv' which I actually set as my WORKDIR at first but then changed to '/app', also it needed to be absolute in the CMD in the last line. One thing I'm wondering is is it even worth it going through the hassle of creating a virtualenv if the container itself is isolated and atomic?