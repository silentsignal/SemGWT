import os
import re
import sys
import ast

RE_ONSCRIPTDOWNLOADED=re.compile("^[^\\.]+\\.onScriptDownloaded\\(")
RE_BODYSCRIPT=re.compile("<body><script><!--")
cache=open(sys.argv[1],"r").read()
dirname=os.path.basename(sys.argv[1]).split('.')[0]

if "onScriptDownloaded" in cache: # version X
    os.mkdir(dirname)
    raw_arr=RE_ONSCRIPTDOWNLOADED.sub("",cache)[:-3]
    arr=ast.literal_eval(raw_arr) # this can result in code exec but json doesn't like single quites :P
    for n,v in enumerate(arr):
        with open(os.path.join(dirname,"%d.js" % (n)),"w") as out:
            out.write(v)
elif cache.startswith("<html>"): # version Y
    os.mkdir(dirname)
    parts=cache.split("<script><!--")
    for n,v in enumerate(parts):
        if n == 0:
            continue
        with open(os.path.join(dirname,"%d.js" % (n)),"w") as out:
            out.write(v.replace("--></script>","").replace("</body></html>",""))
    
