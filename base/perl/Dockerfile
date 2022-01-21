FROM perl:5.26

ARG base_dir
ARG service_dir

COPY $base_dir /opt/app
WORKDIR /opt/app

RUN echo "installing apt and cpan deps" \
      && apt-get -y -q update \
      && DEBIAN_FRONTEND=noninteractive \
      && apt-get -y -q --no-install-recommends install $(cat aptfile) \
      && cpanm -n --installdeps . \
      && rm -rf ~/.cpanm

COPY $service_dir /app/
WORKDIR /app

RUN if [ -n "$service_dir" ] ; then \
      echo "installing apt and cpan deps" \
      && apt-get -y -q update \
      && DEBIAN_FRONTEND=noninteractive \
      && apt-get -y -q --no-install-recommends install $(cat aptfile) \
      && cpanm -n --installdeps . \
      && rm -rf ~/.cpanm;\
    fi

ENTRYPOINT ["/opt/app/bin/start.pl"]
