# ByFly Wi-Fi

![screenshot]

## Installation

Change `conf.ini` file to your credentials.

**Note!** You need python and some packages. You can install packages with the following command:
```
$ pip install -r requirements.txt
```

## Help

You can bind alias to this script with the following commands:

### On Windows
```
> reg add "HKCU\Software\Microsoft\Command Processor" /v Autorun /d "doskey ciscowifi=python \"%cd%\ciscowifi.py\"" /f
```

### On Unix systems
```
$ echo "alias ciscowifi=\"$(pwd)/ciscowifi.py\"" >> ~/.bashrc
```

**Note!** You should be in the `ByFly-WiFi` directory.

You can now use `ciscowifi` command in you terminal for quick connection to wireless.

<!-- Attachments -->
[screenshot]: https://i.ibb.co/fHcHhF5/1.png
