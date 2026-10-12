import os,bz2,struct,math,sys
TM=sys.argv[1] if len(sys.argv)>1 else '0600'
import numpy as np, cv2
ROOT=r'C:\Temp\openpq-himawari-v13'
BBOX=(103.55,9.76,104.45,10.66)
W,H=640,640
a=6378.137;b=6356.7523;dist=42164.
west,south,east,north=BBOX
lon,lat=np.meshgrid(np.linspace(west,east,W),np.linspace(north,south,H))
phi=np.deg2rad(lat);dl=np.deg2rad(lon-140.7)
phic=np.arctan((b*b)/(a*a)*np.tan(phi))
rc=b/np.sqrt(1-(a*a-b*b)/(a*a)*np.cos(phic)**2)
sx=dist-rc*np.cos(phic)*np.cos(dl);sy=-rc*np.cos(phic)*np.sin(dl);sz=rc*np.sin(phic)
xang=np.rad2deg(np.arctan(-sy/sx));yang=np.rad2deg(np.arctan(sz/np.sqrt(sx*sx+sy*sy)))
cols=5500.5+xang*40932549/65536-1
lines=5500.5-yang*40932549/65536
def read_segment(n):
 name=f'HS_H09_20261011_{TM}_B02_FLDK_R10_S{n:02}10.DAT.bz2'
 content=bz2.open(os.path.join(ROOT,name),'rb').read()
 pos=0;offsets={}
 for i in range(11):
  offsets[i+1]=pos;pos+=struct.unpack_from('<H',content,pos+1)[0]
 width,height=struct.unpack_from('<HH',content,offsets[2]+5)
 first=struct.unpack_from('<H',content,offsets[7]+5)[0]
 gain,offset=struct.unpack_from('<dd',content,offsets[5]+19)
 rad2refl=struct.unpack_from('<d',content,offsets[5]+35)[0]
 raw=np.frombuffer(content,dtype='<u2',count=width*height,offset=pos).reshape(height,width)
 return raw.copy(),first,(gain,offset,rad2refl)
s4,n4,cal=read_segment(4)
s5,n5,_=read_segment(5)
print('source rows',n4,n5, 'shape',s4.shape,s5.shape,'cal',cal)
allrows=np.vstack([s4,s5]);del s4,s5
img=cv2.remap(allrows.astype(np.float32),cols.astype(np.float32),(lines-n4).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=65535)
gain,offset,coef=cal
refl=np.clip((img*gain+offset)*coef,0,2)
bad=(img>64000)|(~np.isfinite(img))
refl[bad]=np.nan
print('reflectance p1,5,25,50,75,95,99',np.nanpercentile(refl,[1,5,25,50,75,95,99]))
# Bright albedo overlay: real VIS satellite reflectance B02; never claim it proves ground rain.
# White-gray 6500K-ish, no manufactured texture/noise; high reflectance corresponds to cloud OR bright land.
a=np.interp(np.nan_to_num(refl,nan=0),[0,.08,.14,.24,.40,.60,.90],[0,0,25,90,165,220,245])
brightness=np.interp(np.nan_to_num(refl,nan=0),[0,.05,.2,.6,1.],[180,192,219,246,255])
rgba=np.empty((H,W,4),dtype=np.uint8)
rgba[:,:,0]=brightness
rgba[:,:,1]=np.clip(brightness+2,0,255)
rgba[:,:,2]=np.clip(brightness+7,0,255)
rgba[:,:,3]=a.astype(np.uint8)
rgba[bad,3]=0
out=os.path.join(ROOT,f'AHI_B02_VIS_REFLECTANCE_20261011_{TM}.png')
cv2.imwrite(out,cv2.cvtColor(rgba,cv2.COLOR_RGBA2BGRA),[cv2.IMWRITE_PNG_COMPRESSION,7])
print('SAVED',out,os.path.getsize(out))
# composited with earlier B13 IR actual, subject to physical source data
ir=cv2.imread(os.path.join(ROOT,f'AHI_B13_BT_20261011_{TM}.png'),cv2.IMREAD_UNCHANGED)
assert ir is not None and ir.shape[2]==4
bas=ir.astype(np.float32);vis=cv2.cvtColor(rgba,cv2.COLOR_RGBA2BGRA).astype(np.float32)
al1=bas[:,:,3]/255; al2=vis[:,:,3]/255
aout=al2+al1*(1-al2)
outf=np.zeros_like(bas)
for channel in range(3):
 outf[:,:,channel]=np.where(aout>0,(vis[:,:,channel]*al2+bas[:,:,channel]*al1*(1-al2))/np.maximum(aout,1e-5),0)
outf[:,:,3]=aout*255
path=os.path.join(ROOT,f'AHI_COMPOSITE_VIS_IR_20261011_{TM}.png')
cv2.imwrite(path,outf.astype(np.uint8),[cv2.IMWRITE_PNG_COMPRESSION,8])
print('COMPOSITE',path,os.path.getsize(path))
