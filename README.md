# FORTIPROXY - Forticlient container with proxies

Project aims to be solid alternative to official FortiClient VPN on Linux (and probably MacOS) configured for authenticating through Azure AD.

As running is docker is work in progress, only way of using this repo right now is for local invocation.

## Prerequisites

There are few things needed to make this work:
* working Poetry installed (preferably) with [official installer](https://python-poetry.org/docs/)
* python 3.10 (should also work with older versions, but needs changing it in `pyproject.toml`)
* OpenConnect VPN client version 9+

## Dedicated virtual environment for installation

By default, Poetry will use whichever virtualenv is currently activated. However, if there's none, Poetry will create dedicated one that will be used whenever there's no active virtualenv.

## Configuration

All the configuration of `fortiproxy` python module is done through `.env` file. One needs to create it and fill with proper environment variables (`.env.example` can be used ...well, as an example ;)).

* `SAML_URL` - full URL to SAML start page as configured by VPN provider,
* `EMAIL` - Azure AD email used for sign-in,
* `PASSWORD` - Azure AD password,
* `SECRET` - 2FA TOTP secret used for token generation.
* `BROWSER_PATH` - path to chromium based browser

To check if everything works by running:

```bash
$ poetry run python -m fortiproxy
```
or
```bash
(virtualenv1) $ python -m fortiproxy
```

If everything worked correctly, script should print SAML cookie to std output.

### Running browser in xvfb

There's `xvfb-chromium` script prepared for docker environment to run a browser (used by fortiproxy script) inside virtual framebuffer X server (xvfb). One can also use it for local invocation, but browser invocation

```bash
chromium --no-sandbox $@ &
```
needs to be adjusted to reflect real name of the one that exists in a local system.


## Connecting to VPN

Only thing needed now to connect to VPN is invocation of OpenConnect.

```bash
(virtualenv1) $ sudo openconnect some-dummy-host.com:11111 --protocol=fortinet --cookie="SVPNCOOKIE=$(python -m fortiproxy)"
```

To have option of closing terminal window without disconnecting, one can run above command inside `tmux` session.
