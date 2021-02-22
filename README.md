# Welcome to ScanYourPDF!

This is my first open-source project so please, feel free to comment on anything that you think requires to be overwritten! The idea behind this software is to allow anyone to make their pdf look like it was scanned. Project is currently running version 1.0 on www.scanyourpdf.com

We were featured in HN for more than 12 hours on the front page! Thanks to everyone that commented and provided feedbck on the project. We are currently working in implementing all of them and feel free to drop of any comments!

[HN Post](https://news.ycombinator.com/item?id=23157408)




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

Then the usual virtualenv dance (this within your software directory):

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Ubuntu, PDF support in ImageMagick is disabled by default for security reasons. To "fix" this, change the line in `/etc/ImageMagick-6/policy.xml` from this:

```<policy domain="coder" rights="none" pattern="PDF" />```

To this:

```<policy domain="coder" rights="read|write" pattern="PDF" />```

Be warned that this may be insecure; use at your own risk.


# Gist
The document scanned_pdf.sh is a simple Gist with the two commands required to make the PDF look scanned in case you would like to run this program locally. To execute you need to make sure dependencies have been correctly installed and run
```
chmod +x ./scanned_pdf.sh
```
This makes the script executable

Usage:
```
./scanned_pdf.sh <filename_to_convert.pdf>
```
Example:
```
./scanned_pdf.sh scan.pdf
```

# Docker

Run the script from a Docker container

```
docker-compose build
docker-compose run --rm app ./scanned_pdf.sh -o output.pdf input.pdf
```

# Pending
- Contact form for people to send any PDF that may have failed the conversion process to check
- Make a Contributing.md file for people to help

# Pull request
- I think everything is working for people to start contributing. Any questions or comments please feel free to send me an email at hello@scanyourpdf.com
