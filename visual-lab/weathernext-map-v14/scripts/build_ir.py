import os, bz2,struct,json,math
import numpy as np,cv2
ROOT=r'C:\Temp\openpq-himawari-v13'
BBOX=(103.55,9.76,104.45,10.66)
W,H=640,640
a0=6378.137;b0=6356.7523;earth_to_satellite=42164.0
lo,latlo,hi,lathi=BBOX
lon,lat=np.meshgrid(np.linspace(lo,hi,W),np.linspace(lathi,latlo,H))
phi=np.deg2rad(lat);dl=np.deg2rad(lon-140.7)
phic=np.arctan((b0*b0)/(a0*a0)*np.tan(phi))
rc=b0/np.sqrt(1-(a0*a0-b0*b0)/(a0*a0)*np.cos(phic)**2)
sx=earth_to_satellite-rc*np.cos(phic)*np.cos(dl)
sy=-rc*np.cos(phic)*np.sin(dl)
sz=rc*np.sin(phic)
xang=np.rad2deg(np.arctan(-sy/sx));yang=np.rad2deg(np.arctan(sz/np.sqrt(sx*sx+sy*sy)))
col=2750.5+xang*20466275/65536-1;line=2750.5-yang*20466275/65536
def get_file(tm,seg):
 f=f'HS_H09_20261011_{tm}_B13_FLDK_R20_S{seg:02}10.DAT.bz2'
 path=os.path.join(ROOT,f)
 if not os.path.isfile(path):
  import urllib.request
  url='https://noaa-himawari9.s3.amazonaws.com/AHI-L1b-FLDK/2026/10/11/'+tm+'/'+f
  urllib.request.urlretrieve(url,path)
 data=bz2.open(path,'rb').read()
 pos=0;blocks={}
 for i in range(11):
  blocks[i+1]=pos;pos+=struct.unpack_from('<H',data,pos+1)[0]
 d2,d5,d7=blocks[2],blocks[5],blocks[7]
 width,height=struct.unpack_from('<HH',data,d2+5)
 first=struct.unpack_from('<H',data,d7+5)[0]
 gain,offset=struct.unpack_from('<dd',data,d5+19)
 c0,c1,c2=struct.unpack_from('<ddd',data,d5+35)
 wave=struct.unpack_from('<d',data,d5+5)[0]*1e-6
 phys=struct.unpack_from('<ddd',data,d5+35+6*8)
 raw=np.frombuffer(data,dtype='<u2',count=width*height,offset=pos).reshape((height,width))
 return raw,first,(gain,offset,c0,c1,c2,wave,*phys)
def build(tm='0600'):
 arrays=[];params=None
 for seg in (4,5):
  raw,first,params=get_file(tm,seg);arrays.append(raw)
 counts=np.vstack(arrays)
 firstline=1651
 indices=(line-firstline).astype(np.float32)
 counts_r=cv2.remap(counts.astype(np.float32),col.astype(np.float32),indices,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=65535)
 gain,offset,c0,c1,c2,wave,c_light,h_p,k_b=params
 rad=counts_r*gain+offset
 with np.errstate(divide='ignore',invalid='ignore',over='ignore'):
  temp=(h_p*c_light/(k_b*wave))/np.log((2*h_p*c_light*c_light)/(np.maximum(rad,1e-6)*1e6*wave**5)+1)
  temp=c0+c1*temp+c2*temp*temp
 temp[(counts_r>65000)|(rad<=0)|(~np.isfinite(temp))]=np.nan
 print(tm,'sample brightness',np.nanpercentile(temp,[1,5,25,50,75,95,99]),'center',temp[H//2,W//2])
 # IR brightness-temperature representation with transparency based only on physical BT.
 # alpha and color derived from source B13; not radar or synthetic texture.
 stops=np.array([185,210,230,245,260,273,284,292,320],dtype=np.float32)
 rgb=np.array([[245,120,104],[250,187,114],[255,238,209],[229,242,252],[188,216,236],[131,168,191],[82,132,166],[53,92,126],[53,92,126]],dtype=np.float32)
 t=np.nan_to_num(temp,nan=320.0)
 rgba=np.empty((H,W,4),np.uint8)
 for ch in range(3):rgba[:,:,ch]=np.interp(t,stops,rgb[:,ch]).clip(0,255).astype('uint8')
 alpha=np.interp(t,[185,220,240,255,270,280,287,295],[255,252,242,212,145,85,27,0])
 alpha[(temp<180)|(~np.isfinite(temp))]=0
 rgba[:,:,3]=alpha.clip(0,255).astype('uint8')
 fn=os.path.join(ROOT,'AHI_B13_BT_20261011_'+tm+'.png')
 cv2.imwrite(fn,cv2.cvtColor(rgba,cv2.COLOR_RGBA2BGRA),[cv2.IMWRITE_PNG_COMPRESSION,9])
 print('EXPORTED',fn,os.path.getsize(fn))
 return fn
if __name__=='__main__':
 import sys
 for tm in sys.argv[1:] or ['0600']:build(tm)
