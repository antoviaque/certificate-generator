Certificate generator
=====================

Generate students certificate PDFs based on a SVG template, including a QR code to verify the certificate.

Requirements
------------

### Debian packages

```
$ sudo apt-get install librsvg2-bin
```

### Python packages

```
$ mkvirtualenv certificate-generator
$ pip install -r requirements.txt
```

Usage
-----

### Students data file

Create a text file, `students_list.csv`, with the students data to display in the certificates. One line per student, each line generates a different certificate:

```
gdufour;Georges Dufour;May 22nd, 2012;for Microsoft
jsmith;Julia Smith;May 22nd, 2012;for Google
...
```

### PDF generation

```
$ workon certificate-generator
$ python ./certificate-generator/generate-certificates.py <template.svg> <students_list.csv> <base_url>
```

With:

* `template.svg`: the SVG template, with the following tags positioned:
 * `short_name`: like `gdufour` for student Georges Dufour
 * `full_name`
 * `graduation_date`: with format `May 22nd, 2012`
 * `organization_complement`: like `for Microsoft`
 * `qrcode_url`: data url containing the QR code image as a base64-encoded PNG image, with a transparent background.
* `students_list.csv`: cf section above
* `base_url`: The generated QR code contains a URL, from which this is the base. The full URL will be `<base_url>/<short_name>.pdf`. This is where you will publish the PDF, to allow to verifiy the certificate.
