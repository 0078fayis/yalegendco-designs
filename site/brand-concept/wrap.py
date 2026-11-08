import sys
frag=open(sys.argv[1]).read()
html='<!doctype html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="color-scheme" content="light dark">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>\n'+frag.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
# move body content after head: everything from first non-head tag
i=html.index('<div class="note">')
head,body=html[:i],html[i:]
open(sys.argv[2],'w').write(head+'</head>\n<body>\n'+body+'\n</body>\n</html>\n')
