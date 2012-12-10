import bpy,os,re
from xml.etree import ElementTree as ET

def typewriteit(scene):
  typewrite = bpy.data.objects['typewriter'].data.body
  #psani zacina v sekvenci na 151
  if bpy.context.scene.frame_current >= 915:
    i = int((bpy.context.scene.frame_current-915)/3)
  else:
    i = 0
  #print(typewrite, i, typewrite[:i])
  bpy.data.objects['search2'].data.body = typewrite[:i]

def render(lang):
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  if (not renderpath):
    os.mkdir(renderpath)
  bpy.context.scene.render.filepath = "//" + renderpath + '/task-switching-'
  if (not os.path.isfile(bpy.context.scene.render.frame_path())):
    bpy.ops.render.render(animation=True)
  else:
    print('already rendered')
  transcodepath = "../getting-started/" + lang + "/figures/"
  regexobj = re.search(r"^(.*\/)(.*)-(\d*)-(\d*)(\.avi)$", bpy.context.scene.render.frame_path())
  webmfile = regexobj.group(2) + ".webm"
  transcodecmd = "ffmpeg -y -i " + bpy.context.scene.render.frame_path() + " -b:v 8000k " + transcodepath + webmfile
  if (not os.path.isfile(transcodepath+webmfile)):
    os.system(transcodecmd)
  else:
    print('already transcoded',transcodepath + webmfile)

def brandificate():

  worldgnome = bpy.data.worlds['World GNOME'] 
  worldrhel = bpy.data.worlds['World RHEL']
  font = bpy.data.fonts['Overpass-Reg']

  for scene in bpy.data.scenes:
    if (scene.world == worldgnome):
      scene.world = worldrhel #replace background color
  for bobj in bpy.data.objects:
    #if (bobj.type == 'FONT' and bobj.get('branded')): #sadly doesn't work
    if (bobj.type == 'FONT' and (bobj.name[:5]=='title')): #replace title font with Overpass Bold
      bobj.data.font = font

#translates strings and calls render
def main():
  global typewrite
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../getting-started/' + lang + '/animation.xml')
    t[lang] = xmlfile.getroot()
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="search2"]').text
    brandificate()
    render(lang)
    
if __name__ == '__main__':
    bpy.app.handlers.frame_change_pre.append(typewriteit)
    main()
    bpy.app.handlers.frame_change_pre.pop(0)
