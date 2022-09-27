# Alpine version
ARG ALPINE_VERSION=edge
# 3proxy version
ARG THREE_PROXY_REPO=https://github.com/z3APA3A/3proxy
ARG THREE_PROXY_BRANCH=0.9.3
ARG THREE_PROXY_URL=${THREE_PROXY_REPO}/archive/${THREE_PROXY_BRANCH}.tar.gz


FROM python:3.10-alpine as build_stage
RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock README.md src ./
RUN python -m poetry build


# Build 3proxy
FROM alpine:${ALPINE_VERSION} as builder
ARG THREE_PROXY_REPO
ARG THREE_PROXY_BRANCH
ARG THREE_PROXY_URL
ADD ${THREE_PROXY_URL} /${THREE_PROXY_BRANCH}.tar.gz
RUN apk add --update alpine-sdk bash linux-headers && \
    cd / && \
    tar -xf ${THREE_PROXY_BRANCH}.tar.gz && \
    cd 3proxy-${THREE_PROXY_BRANCH} && \
    make -f Makefile.Linux



FROM alpine:${ALPINE_VERSION}
ARG THREE_PROXY_BRANCH

COPY --from=builder /3proxy-${THREE_PROXY_BRANCH}/bin /usr/local/bin

# Select S6 runtime architecture: aarch64|amd64 (more on https://github.com/just-containers/s6-overlay/releases/latest)
ARG s6_arch=amd64
ARG s6_version=2.2.0.3

ADD https://github.com/just-containers/s6-overlay/releases/download/v${s6_version}/s6-overlay-${s6_arch}.tar.gz /tmp/s6overlay.tar.gz

ADD rootfs /
RUN \
echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
apk upgrade --update --no-cache && \
apk --update --no-cache add \
  bash \
  tzdata \
  libcrypto3 \
  libssl3 \
  python3 \
  py3-pip \
  openconnect@community \
  dnsmasq \
  chromium \
  chromium-chromedriver && \
echo "Extracting s6 overlay..." && \
  tar xzf /tmp/s6overlay.tar.gz -C / && \
  chmod +x /opt/utils/healthcheck.sh && \
echo "Cleaning up temp directory..." && \
  rm -rf /tmp/s6overlay.tar.gz && \
rm -rf /var/cache/apk/*


COPY --from=build_stage /dist/*.whl .
RUN python -m pip install *.whl
ADD xvfb-chromium /usr/bin/xvfb-chromium

# Init
ENTRYPOINT [ "/init" ]
