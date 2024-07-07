# nmap2md

A little utility to convert nmap XML results to markdown tables.

## Install

Git clone and install to `/usr/local/bin/`

```
sudo git clone https://github.com/lawndoc/nmap2md /usr/local/src/nmap2md
sudo ln -s /usr/local/src/nmap2md/nmap2md.py /usr/local/bin/nmap2md
```

## Usage

```
nmap -A -oX - | nmap2md
```

Returns the below output:

#### 192.168.160.244

| Port | State | Service | Version |
|------|-------|---------|---------|
| 22/tcp | open | ssh | OpenSSH 8.9p1 Ubuntu 3 |
| 80/tcp | open | http | Apache httpd 2.4.52 |

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
* `--sort` is for sorting.
    * Default: `Port;asc`
    * Can use any column that is defined in `-c`
    * `asc` & `desc` options, if none is provided: `asc` by default
* `--print-empty` some port scanning results are empty and those are not displayed. However if there is a need to print empty sets, this option allows this.
    * Default: False

## Additional Example

Use ProjectDiscovery.io tools to perform initial host + service discovery quickly and export the results to Markdown

```
mapcidr -cl 192.168.0.0/16 | naabu -sn | naabu -tp 100 -Pn -nmap-cli 'nmap -A -oX -' | nmap2md
```

## Contributors

This project was originally created by [Vsevolod Djagilev](https://github.com/vdjagilev)

Thanks to the listed contributors for fixing bugs/testing & adding new features:

* [Brandon Hinkel](https://github.com/b4ndit)
* [initinfosec](https://github.com/initinfosec)
