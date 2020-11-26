# Systemd basic

## Intro

See https://en.wikipedia.org/wiki/Systemd

- You can list system units and timers

````shell script
systemctl list-units 
systemctl list-timers
````

- You can list user units and timers


````shell script
systemctl --user list-units 
systemctl --user list-timers
````

- You can filter on unit 

````shell script
systemctl list-units ‘*resolve*’
systemctl --user list-units '*bluetooth*'
````

output would be 

````shell script
sylvain@sylvain-hp:~$ systemctl list-units '*resolve*'
  UNIT                     LOAD   ACTIVE SUB     DESCRIPTION
  systemd-resolved.service loaded active running Network Name Resolution

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

1 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.

sylvain@sylvain-hp:~$ systemctl --user list-units '*bluetooth*'
  UNIT                                                                                        LOAD   ACTIVE SUB     DESCRIPTION                                                               >
  sys-devices-pci0000:00-0000:00:1a.0-usb1-1\x2d1-1\x2d1.3-1\x2d1.3:1.0-bluetooth-hci0.device loaded active plugged /sys/devices/pci0000:00/0000:00:1a.0/usb1/1-1/1-1.3/1-1.3:1.0/bluetooth/hc>
  sys-subsystem-bluetooth-devices-hci0.device                                                 loaded active plugged /sys/subsystem/bluetooth/devices/hci0                                     >
  bluetooth.target                                                                            loaded active active  Bluetooth                                                                 >

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

3 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
````


## Purpose

In this document we will show how to create our own `systemd service`.
Like `systemctl start named` used for the [DNS](https://github.com/scoulomb/myDNS/blob/master/2-advanced-bind/5-real-own-dns-application/6-docker-bind-dns-use-linux-nameserver-rather-route53/start.sh).
 
We will start using **user unit**.
Note we should not use root user when using user unit (as home folder `~` is different).

## Perform simple ping with systemd

```shell script
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=/usr/bin/ping attestationcovid.site

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service


systemctl status --user scoulomb.service
systemctl start --user scoulomb.service

systemctl --user stop scoulomb
```


## Run a simple docker image with systemd

We will now run a docker image with systemd

````
mkdir -p ~/.config/systemd/user
 
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run python:3.8

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service
````

To launch docker image, we need to be root (in our current setup).

As `systemd` will launch it, we do not want to require the password.
We will make our user, here `sylvain`, is sudoer for Docker

```shell script
sudo visudo
# https://linuxhandbook.com/sudo-without-password/
# Add this line
sylvain ALL=(ALL) NOPASSWD:/usr/bin/docker, /usr/bin/minikube
```

## To run a docker image doing a ping with user unit

We will now do a ping through a Docker image.
See docker commad here: https://github.com/scoulomb/docker-doctor#binsh-can-be-replaced-by-instruction (use second command)

### Run a docker image doing a ping with user unit and using `-it`

````shell script
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run -it --entrypoint="ping"  registry.hub.docker.com/scoulomb/docker-doctor:dev -c 4 attestationcovid.site; echo $?

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service
````

followed by

```shell script
systemctl --user daemon-reload
systemctl --user stop scoulomb

systemctl --user start scoulomb
systemctl --user status scoulomb
```

This did not work 

````shell script
sylvain@sylvain-hp:~$ systemctl --user status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/home/sylvain/.config/systemd/user/scoulomb.service; disabled; vendor preset: enabled)
     Active: failed (Result: exit-code) since Wed 2020-11-25 19:21:18 CET; 4min 38s ago
    Process: 154167 ExecStart=/usr/bin/sudo /usr/bin/docker run -it --entrypoint=ping registry.hub.docker.com/scoulomb/docker-doctor:dev -c 4 attestationcovid.site; echo $? (code=exited, status=1/FAILURE)
   Main PID: 154167 (code=exited, status=1/FAILURE)

nov. 25 19:21:18 sylvain-hp systemd[939]: Started Start a docker image.
nov. 25 19:21:18 sylvain-hp systemd[939]: scoulomb.service: Main process exited, code=exited, status=1/FAILURE
nov. 25 19:21:18 sylvain-hp systemd[939]: scoulomb.service: Failed with result 'exit-code'.
````

Message is not super-clear here, but error is due to the fact we use interactive mode.
We will see that message error is much more explicit with [system unit](#error-messages-are-more-explicit-with-system-unit) in the same situation.

### Run a docker image doing a ping with user unit and using non interactive mode

````shell script
sudo /usr/bin/docker run -d --rm --name=systemd-ping --entrypoint="ping"  registry.hub.docker.com/scoulomb/docker-doctor:dev -c 15 attestationcovid.site; echo $?
sudo docker logs systemd-ping --follow

# or without ping limit
sudo /usr/bin/docker run -d --name=systemd-ping --entrypoint="ping"  registry.hub.docker.com/scoulomb/docker-doctor:dev attestationcovid.site
sudo docker logs systemd-ping --follow
sudo docker rm systemd-ping --force
````


````shell script
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run -d --name=systemd-ping --entrypoint="ping"  registry.hub.docker.com/scoulomb/docker-doctor:dev attestationcovid.site

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service
````

followed by

```shell script
sudo docker rm systemd-ping --force
systemctl --user daemon-reload
systemctl --user stop scoulomb
systemctl --user start scoulomb
systemctl --user status scoulomb

sleep 3 
systemctl --user status scoulomb

sudo docker logs systemd-ping --follow
systemctl --user stop scoulomb
sudo docker logs systemd-ping --follow
```

Output is 

````shell script
sylvain@sylvain-hp:~$ systemctl --user status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/home/sylvain/.config/systemd/user/scoulomb.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-11-25 21:02:43 CET; 9ms ago
   Main PID: 189669 (sudo)
     CGroup: /user.slice/user-1000.slice/user@1000.service/scoulomb.service
             ├─189669 /usr/bin/sudo /usr/bin/docker run -d --name=systemd-ping --entrypoint=ping registry.hub.d>
             └─189672 /usr/bin/docker run -d --name=systemd-ping --entrypoint=ping registry.hub.docker.com/scou>


sylvain@sylvain-hp:~$ systemctl --user status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/home/sylvain/.config/systemd/user/scoulomb.service; disabled; vendor preset: enabled)
     Active: inactive (dead)

^C
sylvain@sylvain-hp:~$ sudo docker logs systemd-ping --follow
PING attestationcovid.site (216.239.38.21) 56(84) bytes of data.
64 bytes from any-in-2615.1e100.net (216.239.38.21): icmp_seq=1 ttl=114 time=36.9 ms
^C
sylvain@sylvain-hp:~$ systemctl --user stop scoulomb
sylvain@sylvain-hp:~$ sudo docker logs systemd-ping --follow
PING attestationcovid.site (216.239.38.21) 56(84) bytes of data.
64 bytes from any-in-2615.1e100.net (216.239.38.21): icmp_seq=1 ttl=114 time=36.9 ms
````
We have 2 issues we fix in next step:
1. Status is inactive whereas container is running.
2. Container is still running after a service stop. 

### Run a docker image doing a ping with user unit and improving the stop

From https://www.freedesktop.org/software/systemd/man/systemd.service.html

> ExecStop=
Commands to execute to stop the service started via ExecStart=. This argument takes multiple command lines, following the same scheme as described for ExecStart= above. Use of this setting is optional. After the commands configured in this option are run, it is implied that the service is stopped, and any processes remaining for it are terminated according to the KillMode=

Actually we just need to to run it in **NON** detached mode and an **ExecStop**  command

````shell script
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run --name=systemd-ping --entrypoint="ping" registry.hub.docker.com/scoulomb/docker-doctor:dev attestationcovid.site
ExecStop=sudo docker rm systemd-ping --force

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service
````

followed by

```shell script
sudo docker rm systemd-ping --force
systemctl --user daemon-reload
systemctl --user stop scoulomb
systemctl --user start scoulomb
systemctl --user status scoulomb

sleep 3 
systemctl --user status scoulomb

sudo docker logs systemd-ping --follow
systemctl --user stop scoulomb
sudo docker logs systemd-ping --follow
```

Output is 

````shell script
sylvain@sylvain-hp:~$ systemctl --user status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/home/sylvain/.config/systemd/user/scoulomb.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-11-25 21:16:57 CET; 4s ago
   Main PID: 194833 (sudo)
     CGroup: /user.slice/user-1000.slice/user@1000.service/scoulomb.service
             ├─194833 /usr/bin/sudo /usr/bin/docker run --name=systemd-ping --entrypoint=ping registry.hub.dock>
             └─194836 /usr/bin/docker run --name=systemd-ping --entrypoint=ping registry.hub.docker.com/scoulom>

nov. 25 21:16:57 sylvain-hp systemd[939]: Started Start a docker image.
sylvain@sylvain-hp:~$
sylvain@sylvain-hp:~$ sudo docker logs systemd-ping --follow
PING attestationcovid.site (216.239.32.21) 56(84) bytes of data.
64 bytes from any-in-2015.1e100.net (216.239.32.21): icmp_seq=1 ttl=114 time=37.3 ms
64 bytes from any-in-2015.1e100.net (216.239.32.21): icmp_seq=2 ttl=114 time=37.5 ms
^C
sylvain@sylvain-hp:~$ systemctl --user stop scoulomb
sylvain@sylvain-hp:~$ sudo docker logs systemd-ping --follow
Error: No such container: systemd-ping
````

## Add dependencies on other services using user unit is not working if dependencies are system unit

We will start from this example: ["To perform a simple ping with systemd"](#to-perform-a-simple-ping-with-systemd).

For example start a service only inf docker is started and if we are connected to Internet (`systemctl status network-online.target`).

See doc here: https://www.freedesktop.org/software/systemd/man/systemd.unit.html#Requisite=

````shell script
sudo systemctl stop docker.service

echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run --name=systemd-ping --entrypoint="ping" registry.hub.docker.com/scoulomb/docker-doctor:dev attestationcovid.site
ExecStop=sudo docker rm systemd-ping --force

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service
````

This will not work because 

https://wiki.archlinux.org/index.php/systemd/User
> systemd --user runs as a separate process from the systemd --system process. User units can not reference or depend on system units or units of other users.

=> we can not use `--user` if we have dependencies on system service or target.

So we remove the service and recreate it in system units instead of user units.
See here: for the directory https://doc.ubuntu-fr.org/creer_un_service_avec_systemd

So we remove our user unit and use system unit


```shell script
rm -f  ~/.config/systemd/user/scoulomb.service
```



## To add dependencies on other system unit using system units


```shell script
sudo -i # system unit so we can use root

echo '[Unit]
Description=Start a docker image
Requisite=network-online.target docker.service
After=docker.service

[Service]
ExecStart=sudo /usr/bin/docker run --name=systemd-ping --entrypoint="ping" registry.hub.docker.com/scoulomb/docker-doctor:dev attestationcovid.site
ExecStop=sudo docker rm systemd-ping --force

[Install]
WantedBy=default.target' >  ~/.config/systemd/user/scoulomb.service


systemctl daemon-reload
systemctl stop docker.service

```

We can do the ping only if docker is started and connected to Internet.


Observe following output 

````shell script
systemctl start scoulomb
journalctl --unit scoulomb.service | tail -n 4
systemctl list-dependencies scoulomb.service
````

````shell script
root@sylvain-hp:~# systemctl stop docker.service
root@sylvain-hp:~# systemctl start scoulomb
A dependency job for scoulomb.service failed. See 'journalctl -xe' for details.
root@sylvain-hp:~# journalctl --unit scoulomb.service | tail -n 4
nov. 25 21:46:15 sylvain-hp systemd[1]: Dependency failed for Start a docker image.
nov. 25 21:46:15 sylvain-hp systemd[1]: scoulomb.service: Job scoulomb.service/start failed with result 'dependency'.
nov. 25 21:46:19 sylvain-hp systemd[1]: Dependency failed for Start a docker image.
nov. 25 21:46:19 sylvain-hp systemd[1]: scoulomb.service: Job scoulomb.service/start failed with result 'dependency'.
root@sylvain-hp:~# systemctl list-dependencies scoulomb.service
scoulomb.service
● ├─docker.service
● ├─system.slice
● ├─network-online.target
● │ └─NetworkManager-wait-online.service
● └─sysinit.target
●   ├─apparmor.service
●   ├─dev-hugepages.mount
````

It is failing because docker Requisite  is not satisfied as we had done `sudo systemctl stop docker.service`.
If we start it it will work successfully.


````shell script
systemctl start docker.service
systemctl start scoulomb
systemctl status scoulomb
````
Here is the working output:

````shell script
root@sylvain-hp:~# systemctl start docker.service
root@sylvain-hp:~# ^C
root@sylvain-hp:~# systemctl start docker.service
root@sylvain-hp:~# systemctl status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/etc/systemd/system/scoulomb.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-11-25 21:48:15 CET; 2s ago
TriggeredBy: ● scoulomb.timer
   Main PID: 208902 (ping)
      Tasks: 1 (limit: 9357)
     Memory: 544.0K
     CGroup: /system.slice/scoulomb.service
             └─208902 /usr/bin/ping attestationcovid.site

nov. 25 21:48:15 sylvain-hp systemd[1]: Started Start a docker image.
nov. 25 21:48:15 sylvain-hp ping[208902]: PING attestationcovid.site(any-in-2001-4860-4802-34--15.1e100.net 
````

**Note on printing**


Here we lose the color :(. When doing copy paste of `systemctl list-dependencies scoulomb.service`
We can use as alternative.

````shell script
systemctl status scoulomb --output=json-pretty
systemctl list-dependencies --output=json
````

but it not working for `list-dependencies` unlike `status`.

See issues:
- https://github.com/systemd/systemd/issues/17726
- https://github.com/systemd/systemd/issues/17728

## Error messages are more explicit with system unit

Note that making mistakes of interactive mode as done [here](#run-a-docker-image-doing-a-ping-with-user-unit-and-using--it).
Lead to a clearer error message for system unit compared to user unit

````shell script
echo '[Unit]
Description=Start a docker image

[Service]
ExecStart=sudo /usr/bin/docker run -it --entrypoint="ping"  registry.hub.docker.com/scoulomb/docker-doctor:dev -c 4 attestationcovid.site; echo $?

[Install]
WantedBy=default.target' >  /etc/systemd/system/scoulomb.service
````

followed by

```shell script
systemctl daemon-reload
systemctl stop scoulomb

systemctl start scoulomb
systemctl status scoulomb
```

Here error is explicit

````shell script
root@sylvain-hp:~# systemctl status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/etc/systemd/system/scoulomb.service; disabled; vendor preset: enabled)
     Active: failed (Result: exit-code) since Wed 2020-11-25 21:51:47 CET; 4s ago
TriggeredBy: ● scoulomb.timer
    Process: 210132 ExecStart=/usr/bin/sudo /usr/bin/docker run -it --entrypoint=ping registry.hub.docker.com/s>
   Main PID: 210132 (code=exited, status=1/FAILURE)

nov. 25 21:51:46 sylvain-hp systemd[1]: Started Start a docker image.
nov. 25 21:51:46 sylvain-hp sudo[210132]:     root : TTY=unknown ; PWD=/ ; USER=root ; COMMAND=/usr/bin/docker >nov. 25 21:51:47 sylvain-hp sudo[210132]: pam_unix(sudo:session): session opened for user root by (uid=0)
nov. 25 21:51:47 sylvain-hp sudo[210133]: the input device is not a TTY
nov. 25 21:51:47 sylvain-hp sudo[210132]: pam_unix(sudo:session): session closed for user root
nov. 25 21:51:47 sylvain-hp systemd[1]: scoulomb.service: Main process exited, code=exited, status=1/FAILURE
nov. 25 21:51:47 sylvain-hp systemd[1]: scoulomb.service: Failed with result 'exit-code'.
````

## We can do it without Docker hopefully


As done [here](#perform-simple-ping-with-systemd).

````shell script
echo '[Unit]
Description=Start a docker image
Requisite=network-online.target docker.service
After=docker.service

[Service]
ExecStart=/usr/bin/ping attestationcovid.site

[Install]
WantedBy=default.target' > /etc/systemd/system/scoulomb.service
````

And

````shell script
systemctl daemon-reload
systemctl stop scoulomb

systemctl start scoulomb
systemctl status scoulomb
````

Output is 

````shell script
root@sylvain-hp:~# systemctl status scoulomb
● scoulomb.service - Start a docker image
     Loaded: loaded (/etc/systemd/system/scoulomb.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-11-25 21:55:29 CET; 1s ago
TriggeredBy: ● scoulomb.timer
   Main PID: 211280 (ping)
      Tasks: 1 (limit: 9357)
     Memory: 708.0K
     CGroup: /system.slice/scoulomb.service
             └─211280 /usr/bin/ping attestationcovid.site

nov. 25 21:55:29 sylvain-hp systemd[1]: Started Start a docker image.
nov. 25 21:55:29 sylvain-hp ping[211280]: PING attestationcovid.site(any-in-2001-4860-4802-34--15.1e100.net (20>
nov. 25 21:55:29 sylvain-hp ping[211280]: 64 bytes from any-in-2001-4860-4802-34--15.1e100.net (2001:4860:4802:>
nov. 25 21:55:30 sylvain-hp ping[211280]: 64 bytes from any-in-2001-4860-4802-34--15.1e100.net (2001:4860:4802:>
````

Here `systemctl stop scoulomb` or `systemctl stop scoulomb.timer` does not require to do a `ExecStop`.

<!-- We had to do it with Docker even if `ping` overrides uses exec from 
https://github.com/scoulomb/myDNS/blob/master/2-advanced-bind/5-real-own-dns-application/6-use-linux-nameserver-part-d.md#also-when-we-override-it-is-like-we-use-the-exec-form
and I would expect it to pass the signal but it seems kill mode used does not kill the docker OK CF--> 
 

## we could use timer

**Doc**
- https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd.timer.5
- https://jlk.fjfi.cvut.cz/arch/manpages/man/systemd.time.7.en
- https://wiki.archlinux.org/index.php/Systemd/Timers


````shell script
root@sylvain-hp:~# systemctl list-timers
NEXT                        LEFT         LAST                        PASSED       UNIT                         >
Wed 2020-11-25 22:30:05 CET 33min left   Wed 2020-11-25 21:30:21 CET 26min ago    anacron.timer                >
Thu 2020-11-26 00:00:00 CET 2h 3min left Wed 2020-11-25 00:00:02 CET 21h ago      logrotate.timer              >
[]
````

I will use [version without docker](#we-can-do-it-without-docker) and limit ping to 1 to have equivalent of a job.

````shell script
echo '[Unit]
Description=Start a ping

[Service]
ExecStart=/usr/bin/ping -c 1 attestationcovid.site

[Install]
WantedBy=default.target' > /etc/systemd/system/scoulomb.service


echo '[Unit]
Description=Start a docker image

[Timer]
OnCalendar=*-*-* *:*:15


[Install]
WantedBy=default.target' > /etc/systemd/system/scoulomb.timer
````

And the we start the service via the timer

````shell script
systemctl daemon-reload
systemctl stop scoulomb
systemctl stop scoulomb.timer

systemctl start scoulomb.timer
````

and we can check st 

````shell script
systemctl status scoulomb.timer
systemctl status scoulomb > tmp
cat tmp
journalctl --unit=scoulomb | tail -n 7
````

output is

````shell script
root@sylvain-hp:~# systemctl status scoulomb.timer
● scoulomb.timer - Start a docker image
     Loaded: loaded (/etc/systemd/system/scoulomb.timer; disabled; vendor preset: enabled)
     Active: active (waiting) since Wed 2020-11-25 22:00:11 CET; 2min 14s ago
    Trigger: Wed 2020-11-25 22:03:15 CET; 48s left
   Triggers: ● scoulomb.service

nov. 25 22:00:11 sylvain-hp systemd[1]: Started Start a docker image.
root@sylvain-hp:~# systemctl status scoulomb > tmp
root@sylvain-hp:~# cat tmp
● scoulomb.service - Start a ping
     Loaded: loaded (/etc/systemd/system/scoulomb.service; disabled; vendor preset: enabled)
     Active: inactive (dead) since Wed 2020-11-25 22:02:22 CET; 10s ago
TriggeredBy: ● scoulomb.timer
    Process: 213212 ExecStart=/usr/bin/ping -c 1 attestationcovid.site (code=exited, status=0/SUCCESS)
   Main PID: 213212 (code=exited, status=0/SUCCESS)

nov. 25 22:02:22 sylvain-hp systemd[1]: Started Start a ping.
nov. 25 22:02:22 sylvain-hp ping[213212]: PING attestationcovid.site(any-in-2001-4860-4802-32--15.1e100.net (2001:4860:4802:32::15)) 56 data bytes
nov. 25 22:02:22 sylvain-hp ping[213212]: 64 bytes from any-in-2001-4860-4802-32--15.1e100.net (2001:4860:4802:32::15): icmp_seq=1 ttl=114 time=51.5 ms
nov. 25 22:02:22 sylvain-hp ping[213212]: --- attestationcovid.site ping statistics ---
nov. 25 22:02:22 sylvain-hp ping[213212]: 1 packets transmitted, 1 received, 0% packet loss, time 0ms
nov. 25 22:02:22 sylvain-hp ping[213212]: rtt min/avg/max/mdev = 51.496/51.496/51.496/0.000 ms
nov. 25 22:02:22 sylvain-hp systemd[1]: scoulomb.service: Succeeded.
root@sylvain-hp:~# journalctl --unit=scoulomb | tail -n 7
nov. 25 22:02:22 sylvain-hp systemd[1]: Started Start a ping.
nov. 25 22:02:22 sylvain-hp ping[213212]: PING attestationcovid.site(any-in-2001-4860-4802-32--15.1e100.net (2001:4860:4802:32::15)) 56 data bytes
nov. 25 22:02:22 sylvain-hp ping[213212]: 64 bytes from any-in-2001-4860-4802-32--15.1e100.net (2001:4860:4802:32::15): icmp_seq=1 ttl=114 time=51.5 ms
nov. 25 22:02:22 sylvain-hp ping[213212]: --- attestationcovid.site ping statistics ---
nov. 25 22:02:22 sylvain-hp ping[213212]: 1 packets transmitted, 1 received, 0% packet loss, time 0ms
nov. 25 22:02:22 sylvain-hp ping[213212]: rtt min/avg/max/mdev = 51.496/51.496/51.496/0.000 ms
nov. 25 22:02:22 sylvain-hp systemd[1]: scoulomb.service: Succeeded.
````


We can use a better accuracy to ensure we trigger at correct second 

````shell script
echo '[Unit]
Description=Start a docker image

[Timer]
OnCalendar=*-*-* *:*:15
AccuracySec=0.5


[Install]
WantedBy=default.target' > /etc/systemd/system/scoulomb.timer

````


## Usage in real world

### program start up or cronjob

Note we can use system enable to launch a service or timer at system start
And disable (it will remove the symlink)

we use this for DEV vm with [Jupyter](https://github.com/scoulomb/myk8s/blob/master/Setup/ArchDevVM/archlinux-dev-vm-with-minikube.md#deploy-guest-archlinux-vm-with-vagrant).

````shell script
➤ systemctl list-units '*jupyter*'
  UNIT LOAD ACTIVE SUB DESCRIPTION
0 loaded units listed. Pass --all to see loaded but inactive units, too.
➤ systemctl list-units --user '*jupyter*'
  UNIT            LOAD   ACTIVE SUB     DESCRIPTION
  jupyter.service loaded active running Start Jupyter Notebook when loging in. Available at http://localhost:9999

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

1 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
````

we could start Minikube at machine start up with systemd.

### systemd-resolve


Also when we did `sudo systemd-resolve --flush-caches` here:
https://github.com/scoulomb/myk8s/blob/master/Setup/ArchDevVM/archlinux-dev-vm-with-minikube.md#dns-issue

Behind it is a `systemd` wrapper: https://wiki.archlinux.org/index.php/Systemd-resolved

Here is a proof

````shell script
[09:49] ~
➤ systemctl list-units '*resolve*'
  UNIT                     LOAD   ACTIVE SUB     DESCRIPTION
  systemd-resolved.service loaded active running Network Name Resolution

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

1 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.

➤ systemctl list-units | grep resolve
  systemd-resolved.service                                                                 loaded active running
   Network Name Resolution
[21:12] ~
➤ systemd-resolve --flush-caches
[21:12] ~
➤ systemctl status systemd-resolved.service
● systemd-resolved.service - Network Name Resolution
     Loaded: loaded (/usr/lib/systemd/system/systemd-resolved.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-11-25 08:45:27 UTC; 12h ago
       Docs: man:systemd-resolved.service(8)
             https://www.freedesktop.org/wiki/Software/systemd/resolved
             https://www.freedesktop.org/wiki/Software/systemd/writing-network-configuration-managers
             https://www.freedesktop.org/wiki/Software/systemd/writing-resolver-clients
   Main PID: 280 (systemd-resolve)
     Status: "Processing requests..."
      Tasks: 1 (limit: 17556)
     Memory: 4.3M
     CGroup: /system.slice/systemd-resolved.service
             └─280 /usr/lib/systemd/systemd-resolved

Nov 25 08:45:27 archlinux systemd-resolved[280]: Negative trust anchors: 10.in-addr.arpa 16.172.in-addr.arpa 17>Nov 25 08:45:27 archlinux systemd-resolved[280]: Using system hostname 'archlinux'.
Nov 25 08:45:27 archlinux systemd[1]: Started Network Name Resolution.
Nov 25 08:45:40 archlinux systemd-resolved[280]: Using degraded feature set UDP instead of UDP+EDNS0 for DNS se>Nov 25 08:45:51 archlinux systemd-resolved[280]: Using degraded feature set TCP instead of UDP for DNS server 1>
Nov 25 11:28:13 archlinux systemd-resolved[280]: Grace period over, resuming full feature set (UDP+EDNS0) for D>Nov 25 14:53:51 archlinux systemd-resolved[280]: Using degraded feature set UDP instead of UDP+EDNS0 for DNS se>
Nov 25 18:35:55 archlinux systemd-resolved[280]: Grace period over, resuming full feature set (UDP+EDNS0) for D>Nov 25 18:36:06 archlinux systemd-resolved[280]: Using degraded feature set UDP instead of UDP+EDNS0 for DNS se>
Nov 25 21:12:12 archlinux systemd-resolved[280]: Flushed all caches.
````


<!-- flush cache when change nw -->
<!-- OK CONCLUDED AND LINK DONE HERE-->


