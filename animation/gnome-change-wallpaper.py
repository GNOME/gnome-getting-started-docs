import bpy,os,re,gnomerender
from xml.etree import ElementTree as ET

def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
    t[lang] = xmlfile.getroot()
  
  for lang in t:
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['usermenuuser'].data.body = bpy.data.objects['user'].data.body #due to different alignment
    gnomerender.render(lang)
    gnomerender.transcode(lang)
    
if __name__ == '__main__':
    main()
