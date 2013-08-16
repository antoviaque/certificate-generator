#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Upstream University <contact@upstream-university.org>
#
# Authors:
#          Xavier Antoviaque <xavier@antoviaque.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#

# Imports #####################################################################

import codecs
import qrcode
import sh
import StringIO
import sys

from jinja2 import Template
from urlparse import urljoin


# Functions ###################################################################

def main():
    if len(sys.argv) != 4:
        print u'Usage: {file} <template.svg> <students_list.csv> <base_url>'.format(file=__file__)
        return 1
    
    template_file = sys.argv[1]
    students_list_file = sys.argv[2]
    base_url = sys.argv[3]
    
    for student in get_students_list(students_list_file, base_url):
        svg_file = u'{0}.svg'.format(student['short_name'])
        pdf_file = u'{0}.pdf'.format(student['short_name'])

        print u'* Generating {0}...'.format(student['url'])
        template2svg(student, template_file, svg_file)
        svg2pdf(svg_file, pdf_file)

def get_students_list(students_list_file, base_url):
    students = []
    with codecs.open(students_list_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            student_row = line.split(';')
            student_url = urljoin(base_url, '{0}.pdf'.format(student_row[0]))
            qrcode_img = get_qrcode(student_url)
            qrcode_dataurl = img2dataurl(qrcode_img)
            students.append({
                'short_name': student_row[0],
                'full_name': student_row[1],
                'graduation_date': student_row[2],
                'organization_complement': student_row[3],
                'url': student_url,
                'qrcode_url': qrcode_dataurl
            })
    return students

def get_qrcode(student_url):
    qrcode_img = qrcode.make(student_url, border=0)
    qrcode_img = img_white2transparent(qrcode_img)
    return qrcode_img

def img2dataurl(img):
    output = StringIO.StringIO()
    img.save(output, 'PNG')
    img_base64 = output.getvalue().encode('base64')
    img_dataurl = 'data:image/png;base64,{0}'.format(img_base64)
    return img_dataurl

def img_white2transparent(img):
    # http://stackoverflow.com/a/765774/1265417
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

def template2svg(student, template_file, svg_file):
    with codecs.open(template_file, encoding='utf-8') as f:
        template = Template(f.read())

    svg_raw = template.render(**student)

    with codecs.open(svg_file, 'w+', encoding='utf-8') as f:
        f.write(svg_raw)

def svg2pdf(svg_file, pdf_file):
    rsvg_convert = sh.Command('rsvg-convert')
    rsvg_convert('-f', 'pdf', '-o', pdf_file, svg_file)


# Main ########################################################################

if __name__ == '__main__':
    return_code = main()
    sys.exit(return_code)
