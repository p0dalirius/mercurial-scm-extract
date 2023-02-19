# mercurial-scm-extract

<p align="center">
    A tool to extract and dump files of mercurial SCM exposed on a web server.
    <br>
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/mercurial-scm-extract">
    <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
    <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
    <br>
</p>

## Features

 - [x] Extracts files of mercurial SCM exposed on a web server.
 - [x] Dump project files and .hg/ files locally.

## Usage

```
$ ./mercurial-scm-extract.py -h
mercurial-scm-extract.py v1.0 - by @podalirius_

usage: mercurial-scm-extract.py [-h] -u URL -d DIR [-v]

options:
  -h, --help         show this help message and exit
  -u URL, --url URL  Target URL.
  -d DIR, --dir DIR  Directory where to save dumped files.
  -v, --verbose      Verbose mode. (default: False)
```

## Example

![](./.github/example.png)

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.
