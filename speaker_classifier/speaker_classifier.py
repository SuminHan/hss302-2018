import codecs
import os
import shutil
import string
import time

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
valid_content_chars = "-_.() %s%s%s" % (string.ascii_letters, string.digits, string.printable)
alphabets = "abcdefghijklmnopqrstuvwxyz"

rdir = 'result'
sdir = 'samples'
if not os.path.exists(rdir):
    os.makedirs(rdir)
else:
    for the_file in os.listdir(rdir):
        file_path = os.path.join(rdir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

f = []
for (dirpath, dirnames, filenames) in os.walk(sdir):
    f.extend(filenames)

ofiles = {}
for fn in f:
    print(fn)
    prev_speaker = None
    with codecs.open(os.path.join(sdir, fn), 'r', 'utf-8') as page:
        for line in page:
            cidx = 0
            not_name = False
            while cidx < len(line) and line[cidx] != ':':
                if line[cidx] not in " %s%s"%(alphabets.lower(), alphabets.upper()):
                    not_name = True
                cidx = cidx + 1

            if not cidx < len(line) or not_name:
                if not prev_speaker: continue
                else: speaker = prev_speaker
            else:
                speaker = line[:cidx].strip()
            content = line[cidx+1:].strip()

            valid_content = "".join(e for e in content if e in valid_content_chars)
            if len(valid_content) == 0: continue

            valid_name = "".join(e for e in speaker if e in valid_chars)
            if valid_name not in ofiles:
                ofiles[valid_name] = codecs.open(os.path.join(rdir,valid_name + '.txt'),'w+',encoding='utf8')

            ofiles[valid_name].write(valid_content + '\n')
            prev_speaker = valid_name

for of in ofiles:
    ofiles[of].close()