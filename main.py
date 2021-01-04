import os
import base64
import lzma
import sys

import jinja2
import segno
import hashlib
import datetime

outputs = []
filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
sha384 = hashlib.sha384()
with open(filename,'rb') as f:
    if not os.path.exists('encoded'):
        os.mkdir('encoded')
    i = 0
    while True:
        block = f.read(256)
        if len(block) != 0:
            sha384.update(block)
            encoded = base64.b64encode(block)
            qr = segno.make_qr(encoded, error="H")
            #qr.save('encoded/qr_{}.png'.format(i), scale=3)
            outputs.append(['qr_{}.png'.format(i),filename,qr.svg_data_uri(scale=2.5),i])
            i += 1
            print(i*256)
        else:
            break

def gettime():
    return datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S fmt: MM/DD/YY, HH/MM/SS")

from jinja2 import Template
with open("templates/print.html") as f:
    template = Template(f.read())
    data = template.render(filename=filename,imgs=outputs,hash=segno.make_qr(sha384.hexdigest()).svg_data_uri(scale=2),len=len,time=gettime)
    mode = "w"
    if not os.path.exists('encoded'):
        mode = "x"
    with open('encoded/index.html',mode) as outfile:
        outfile.write(data)

