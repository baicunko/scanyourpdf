# Welcome to ScanYourPDF!

This is my first open-source project so please, feel free to comment on anything that you think requires to be overwritten! The idea behind this software is to allow anyone to make their pdf look like it was scanned. Project is currently running version 1.0 on www.scanyourpdf.com



# Dependencies

Project requires ImageMagick and GhostScript. This will do the trick on Ubuntu:

```
sudo apt-get install ghostscript
sudo apt-get install imagemagick
```

This should work on macOS with [Homebrew](https://brew.sh/):

```
brew install ghostscript
brew install imagemagick
```

Then the usual virtualenv dance:

```
python3 -m venv .venv
pip install -r requirements.txt
```

On Ubuntu, PDF support in ImageMagick is disabled by default for security reasons. To "fix" this, change the line in `/etc/ImageMagick-6/policy.xml` from this:

```<policy domain="coder" rights="none" pattern="PDF" />```

To this:

```<policy domain="coder" rights="read|write" pattern="PDF" />```

Be warned that this may be insecure; use at your own risk.

# Pending
- Contact form for people to send any PDF that may have failed the conversion process to check
- Make a Contributing.md file for people to help

# Pull request
- I think everything is working for people to start contributing. Any questions or comments please feel free to send me an email at hello@scanyourpdf.com
