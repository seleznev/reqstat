# reqstat

## Components

* reqstatd

  Daemon that receive log messages (in syslog format) from webserver (fox ex. nginx), collect statistics and expose in Prometheus format.

* reqstat

  CLI utility to show metrics in console.

## How to send nginx logs to reqstatd

By default reqstatd waiting nginx log in combined (default) format on 2671/tcp port.

To send logs to reqstat add line like this to nginx configuration (for ex. `/etc/nginx/conf.d/reqstat.conf`):

```
access_log syslog:server=localhost:2671;
```

And then reload nginx:

```
service nginx reload
```

## How to build deb package

On Debian Stretch:

1. Install build dependencies:
   ```
   apt install -y dpkg-dev debhelper dh-systemd python3-setuptools
   ```

2. Build package:
   ```
   dpkg-buildpackage -uc -us
   ```
