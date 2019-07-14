from PIL import Image
from pyglet.gl import *
import glob, os

###add more flexibility
coords_p = -100,-700

#size_m = 200, 200
#size_p = 400, 400
size_m = 80, 80
size_p = size_m[0]*2, size_m[1]*2
size_pullover = 1024, 768
pos = 383, 180

size_m = 165, 165
size_p = 330, 330
size_pullover = 1000, 1300
pos = 657, 225

#size_m = 1000, 1000
#size_p = 2000, 2000
#size_p = 1920, 1080

def full_black():
    for infile in glob.glob("fullblack/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      newData = []
      
      for item in datas:
        if item[0] >= 220 and item[1] >= 220 and item[2] >= 220:
          newData.append((255, 255, 255, 255))
        else:
          newData.append((0,0,0,255))
        
      img.putdata(newData)
      img.save("fullblack/"+infile[10:]+"done-tb.png", "PNG")
      print("tb-"+ file[10:])


def sample_resize():
    sample = Image.open("unwhite/sample.png")
    for infile in glob.glob("unwhite/*.png"):
        if infile != "unwhite/sample.png":
            img = Image.open(infile)
            s,ss = img.size
            sample = sample.resize((s,ss),Image.ANTIALIAS)
            sample.save("unwhite/sample.png", "PNG")
            break
    

def white_gone():
    #sample = Image.open("unwhite/sample.png")
    
    for infile in glob.glob("unwhite/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      #da = sample.getdata()
      newData = []
      count = 0
      
      for item in datas:
        if item[0] != 255 and item[1] != 255 and item[2] != 255:
          newData.append(datas[count])
        else:
          newData.append((0, 0, 0, 0))
        count += 1
      img.putdata(newData)
      """newData = []

      for item in datas:
        if item[0] >= 185 and item[1] >= 185 and item[2] >= 185:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(item)
        
      img.putdata(newData)
      """
      img.save("unwhite/done/" + file[8:] + ".png", "PNG")
      print("tw-"+ file[8:])

def whitey_gone():
    #sample = Image.open("unwhite/sample.png")
    
    for infile in glob.glob("unwhite/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      #da = sample.getdata()
      newData = []
      count = 0
      
      for item in datas:
        if item[0] <= 220 and item[1] <= 220 and item[2] <= 220:
          newData.append(datas[count])
        else:
          newData.append((0, 0, 0, 0))
        count += 1
      img.putdata(newData)
      
      img.save("unwhite/done/" + file[8:] + ".png", "PNG")
      print("tw-"+ file[8:])
      
def green_gone():
    #sample = Image.open("unwhite/sample.png")
    
    for infile in glob.glob("unwhite/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      #da = sample.getdata()
      newData = []
      count = 0
      
      for item in datas:
        if item[0] == 203 and item[1] == 210 and item[2] == 217:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(datas[count])
          
        count += 1
    
      """for item in datas:
        if item[0] >= 202 and item[0] <= 204 and item[1] >= 209 and item[1] <= 211 and item[2] >= 215 and item[2] <= 218:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(datas[count])
          
        count += 1
      img.putdata(newData)
      newData = []

      for item in datas:
        if item[0] >= 185 and item[1] >= 185 and item[2] >= 185:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(item)
        
      img.putdata(newData)
      """
      img.save("unwhite/done/" + file[8:] + "-done.png", "PNG")
      print("tw-"+ file[8:])

def resize_pullover():
  for infile in glob.glob("pullovers/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.resize(size_pullover,Image.ANTIALIAS)
      img.save("pullovers/resize/" + file[10:] + "-resize.png", "PNG")
      print("resize_pullover-"+ file[10:])

def merge():
  number = 0
  countt = 0
  maxx = 0
  
  for inf in glob.glob("pullovers/resize/*-resize.png"):
    countt = 0
    for infile in glob.glob("selection/M*.png"):
      img = Image.open(infile)
      file1, ext1 = os.path.splitext(infile)
      img2 = Image.open(inf)
      file2, ext2 = os.path.splitext(inf)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

      blank = Image.new('RGBA', img2.size)
      xyx,yxy = img.size
      number = yxy
      blank.paste(img,pos)
      #blank.save(file1[10:]+ "test.png", "PNG")
      #img = blank.convert("RGBA")
      datas = blank.getdata()
      dat = img2.getdata()
      newData = []
      count = 0
      for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
          newData.append(dat[count])
        else:
          newData.append(item)
        count += 1
        
      img2.putdata(newData)
      img2.save("step/M" + str(countt) + "00000"+ file1[11:] + "-" + file2[18:] + ".png", "PNG")
      countt += 1
      maxx = countt
      print("merge-" + file1[11:])
  countt = 0
  #ctt = 0
  for infile in glob.glob("selection/AK*.png"):
    for inf in glob.glob("step/M*.png"):
        sss = str(count)+"000"
        
        if str(inf[6:8]) == sss[0:2]:
          img = Image.open(infile)
          file1, ext1 = os.path.splitext(infile)
          img2 = Image.open(inf)
          file2, ext2 = os.path.splitext(inf)
          #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

          #blank = Image.new('RGBA', img2.size)
          xyx,yxy = pos
          img2.paste(img,(xyx, yxy+number-3))
          #blank.save(file1[10:]+ "test.png", "PNG")
          #img = blank.convert("RGBA")
          """datas = blank.getdata()
          dat = img2.getdata()
          newData = []
          count = 0
          for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
              newData.append(dat[count])
            else:
              newData.append(item)
            count += 1
            
          img2.putdata(newData)"""
          img2.save("merge_po/" + file1[10:] + "-" + file2[18:] + ".png", "PNG")
          print("merge-" + file1[10:])
          #ctt += 1
    countt += 1

def resize():
  for infile in glob.glob("Ms/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img.thumbnail(size_m)
      img.save("Ms/resize/" + file[3:] + "-resize.png", "PNG")
      print("resize-"+ file[3:])

def transparancy_black():
  for infile in glob.glob("Ms/resize/*-resize.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      newData = []
      
      for item in datas:
        if item[0] <= 155 and item[1] != 155 and item[2] != 155:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(item)
        
      img.putdata(newData)
      img.save("Ms/tb/" + file[10:] + "-tb.png", "PNG")
      print("tb-"+ file[10:])

def resize_pattern():
  for infile in glob.glob("patterns/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.resize(size_p, Image.ANTIALIAS)
      img.save("patterns/resize/" + file[9:] + "-resize.png", "PNG")
      print("resize_p-"+ file[9:])

def resize_pattern_new(infile,size1,size2):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      #img = img.resize((int(size1*1.4),size2), Image.ANTIALIAS)
      img = img.resize((size1,size2), Image.ANTIALIAS)
      img.save("patterns/resize/" + file[9:] + "-resize.png", "PNG")
      print("resize_p-"+ file[9:])
      inf = "patterns/resize/" + file[9:] + "-resize.png"
      return img, inf

def blit_pattern():
  
  for infile in glob.glob("Ms/tb/M*-tb.png"):
    for inf2 in glob.glob("patterns/*.png"):
      img = Image.open(infile)
      size1,size2 = img.size
      img2, inf = resize_pattern_new(inf2,size1,size2)
      #img11 = pyglet.image.load("Ms/tb/M-Bombardme+-resize-tb.png")
      file1, ext1 = os.path.splitext(infile)
      
      #img2 = Image.open(inf)
      #img22 = pyglet.image.load("patterns/resize/blue-resize.png")
      file2, ext2 = os.path.splitext(inf)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
      #blank = pyglet.image.Texture.create(200,200)
      blank = Image.new('RGBA', img.size)
      """w1, h1 = img.size
      w2, h2 = img2.size
      sssize = w1-w2
      #pos11 = 20-(w2-w1)
      #pos22 = 20-(h2-h1)"""
      blank.paste(img2,(0,0)) #sssize
      #print(str(img.size) + "" + str(img2.size))
      img = img.convert("RGBA")
      datas = img.getdata()
      dat = blank.getdata()
      newData = []
      count = 0
      for item in datas:
        if item[0] != 255 and item[1] != 255 and item[2] != 255:
          newData.append(dat[count])
        else:
          newData.append(item)
        count += 1
      blank.putdata(newData)
      blank.save("Ms/pattern_blit/" + file1[6:] + "-" + file2[17:] + ".png", "PNG")
      print("blit_p-" + file1[7:])
      
  for infile in glob.glob("Ms/tb/AK*-tb.png"):
    for inf2 in glob.glob("patterns/*.png"):
      img = Image.open(infile)
      size1,size2 = img.size
      size2 = int(size2*2.5)
      img2, inf = resize_pattern_new(inf2,size1,size2)
      #img11 = pyglet.image.load("Ms/tb/M-Bombardme+-resize-tb.png")
      file1, ext1 = os.path.splitext(infile)
      
      #img2 = Image.open(inf)
      #img22 = pyglet.image.load("patterns/resize/blue-resize.png")
      file2, ext2 = os.path.splitext(inf)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
      #blank = pyglet.image.Texture.create(200,200)
      blank = Image.new('RGBA', img.size)
      """w1, h1 = img.size
      w2, h2 = img2.size
      sssize = w1-w2
      #pos11 = 20-(w2-w1)
      #pos22 = 20-(h2-h1)"""
      blank.paste(img2,(0,int(size2/2.5*-1.5))) #sssize
      #print(str(img.size) + "" + str(img2.size))
      img = img.convert("RGBA")
      datas = img.getdata()
      dat = blank.getdata()
      newData = []
      count = 0
      for item in datas:
        if item[0] != 255 and item[1] != 255 and item[2] != 255:
          newData.append(dat[count])
        else:
          newData.append(item)
        count += 1
      blank.putdata(newData)
      blank.save("Ms/pattern_blit/" + file1[6:] + "-" + file2[17:] + ".png", "PNG")
      print("blit_p-" + file1[7:])
      #blank.blit_into(img22,0,0,0)

      #blank.blit_into(img11,10,10,0) 
      #blank.save("output/" + file1[7:] + "-" + file2[17:] + ".png")

def transparancy_white():
  for infile in glob.glob("Ms/pattern_blit/*.png"):
      file, ext = os.path.splitext(infile)
      img = Image.open(infile)
      img = img.convert("RGBA")
      datas = img.getdata()
      newData = []
      
      for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
          newData.append((0, 0, 0, 0))
        else:
          newData.append(item)
        
      img.putdata(newData)
      img.save("output/" + file[15:] + "-done.png", "PNG")
      print("tw-"+ file[15:])

def test():
  img = Image.open("Ms/tb/M-Bombardme+-resize-tb.png")
  file1, ext1 = os.path.splitext("Ms/tb/M-Bombardme+-resize-tb.png")
  
  img2 = Image.open("patterns/resize/blue-resize.png")
  file2, ext2 = os.path.splitext("patterns/resize/blue-resize.png")

  blank = Image.new('RGBA', (200,200))
  blank.paste(img2,(0,0))
  #blank.paste(img1,(0,0))
  #blank.save("output/" + file1[7:] + "-" + file2[17:] + ".png", "PNG")
  img = img.convert("RGBA")
  datas = img.getdata()
  dat = blank.getdata()
  newData = []
  count = 0
  for item in datas:
    if item[0] != 255 and item[1] != 255 and item[2] != 255:
      newData.append(dat[count])
    else:
      newData.append(item)
    count += 1
  blank.putdata(newData)
  blank.save("output/" + "test" + "-tb.png", "PNG")


"""
from PIL import Image

img = Image.open('1.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] != 255 and item[1] != 255 and item[2] != 255:
        newData.append((0, 0, 0, 0))
    else:
        newData.append(item)
        
img.putdata(newData)

img.save("img5.png", "PNG")"""

#test()
#resize_pullover()
