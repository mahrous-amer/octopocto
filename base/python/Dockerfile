FROM python:latest

ARG base_dir
ARG service_dir
ARG arg

COPY $base_dir /opt/app
WORKDIR /opt/app

RUN echo "installing apt and pip deps" \
      && apt-get -y -q update \
      && DEBIAN_FRONTEND=noninteractive \
      && apt-get -y -q --no-install-recommends install $(cat aptfile) \
      && pip install --upgrade pip \
      && echo $(pwd && ls) && pip install -r /opt/app/requirments.txt

COPY $service_dir /app/
WORKDIR /app

RUN if [ -n "$service_dir" ] ; then \
      echo "installing apt and pip deps" \
      && apt-get -y -q update \
      && DEBIAN_FRONTEND=noninteractive \
      && apt-get -y -q --no-install-recommends install $(cat aptfile) \
      && pip install -r requirments.txt; \
    fi

RUN pip install git+https://github.com/redis/redis-py.git

ENV PYTHONPATH="/app/lib"

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["bin/main.py"]
