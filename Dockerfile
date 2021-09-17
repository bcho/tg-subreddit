FROM python:3.9-slim-buster as base

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
# disable pip cache
ENV PIP_NO_CACHE_DIR=1

COPY . .
RUN pip install --prefer-binary -r requirements.txt

FROM python:3.9-slim-buster

# prepare non-root user
RUN groupadd -g 999 app && \
	useradd -r -u 999 -g app app && \
	mkdir -p /home/app && chown -R app:app /home/app

# venv
COPY --from=base /opt/venv /opt/venv

# source code
WORKDIR /app
COPY . /app

USER app
CMD ["/opt/venv/bin/python", "app.py"]