# nmap2md

A little utility to convert nmap XML results to markdown tables.

## Usage

```
nmap -A -oX - 192.168.160.244 | nmap2md
```

Returns the below output:

#### 192.168.160.244

| Port | State | Service | Version |
|------|-------|---------|---------|
| 22/tcp | open | ssh | OpenSSH 8.9p1 Ubuntu 3 |
| 80/tcp | open | http | Apache httpd 2.4.52 |

## Additional Example

Use ProjectDiscovery.io tools to perform initial host + service discovery quickly and export the results to Markdown

```
mapcidr -cl 192.168.0.0/16 | naabu -sn | naabu -tp 100 -Pn -nmap-cli 'nmap -A -oX -' | nmap2md
```

Returns the below output:

#### 192.168.160.242

| Port | State | Service | Version |
|------|-------|---------|---------|
| 25/tcp | open | smtp | hMailServer smtpd  |
| 80/tcp | open | http | Microsoft IIS httpd 10.0 |
| 110/tcp | open | pop3 | hMailServer pop3d  |
| 135/tcp | open | msrpc | Microsoft Windows RPC  |
| 139/tcp | open | netbios-ssn | Microsoft Windows netbios-ssn  |
| 143/tcp | open | imap | hMailServer imapd  |
| 445/tcp | open | microsoft-ds |   |
| 587/tcp | open | smtp | hMailServer smtpd  |


#### 192.168.160.244

| Port | State | Service | Version |
|------|-------|---------|---------|
| 22/tcp | open | ssh | OpenSSH 8.9p1 Ubuntu 3 |
| 80/tcp | open | http | Apache httpd 2.4.52 |


#### 192.168.160.250

| Port | State | Service | Version |
|------|-------|---------|---------|
| 135/tcp | open | msrpc | Microsoft Windows RPC  |
| 139/tcp | open | netbios-ssn | Microsoft Windows netbios-ssn  |
| 445/tcp | open | microsoft-ds |   |
| 3389/tcp | open | ms-wbt-server |   |

## Install

Git clone and install to `/usr/local/bin/`

```
sudo git clone https://github.com/lawndoc/nmap2md /usr/local/src/nmap2md
sudo ln -s /usr/local/src/nmap2md/nmap2md.py /usr/local/bin/nmap2md
```

## Options

Columns and row cells definition should be divided by `,`.

* `-c` is used to define columns. It is possible to write there anything
    * Default: `Port,State,Service,Version`
* `--rc` is used to define **r**ow **c**ells
    * Default: `[port.number]/[port.protocol],[state],[service.name],[service.product] [service.version]`
    * Available options:
        * `[port.number]` Port number (80) 
        * `[port.protocol]` Port protocol (TCP)
        * `[state]` State (open)
        * `[service.name]` Name of the used service (http)
        * `[service.product]` Type of product used on that service (Apache httpd)
        * `[service.version]` Version of the product (2.2.14)
* `--hs` is **h**eader **s**ize. Size variations: from 1 to 6.
    * Default: 0 (disabled)
* `--print-empty` some port scanning results are empty and those are not displayed. However if there is a need to print empty sets, this option allows this.
    * Default: False

## Contributors

This project was originally created by [Vsevolod Djagilev](https://github.com/vdjagilev)

Thanks to the listed contributors for fixing bugs/testing & adding new features:

* [Brandon Hinkel](https://github.com/b4ndit)
* [initinfosec](https://github.com/initinfosec)
