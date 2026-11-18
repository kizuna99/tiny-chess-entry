import json,os,sys,urllib.request as U
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)
V={"p":1,"n":3,"b":3,"r":5,"q":9,"k":100}
B={"semi-slav":("depth-2","white","d2d4 d7d5 c2c4 c7c6 b1c3 g8f6 e2e3 e7e6 d1c2 b8d7 c1d2 e6e5 c4d5 c6d5 c3b5 e8e7 b5c7 d7b6 d4e5 f6e4 g1f3 e4d2 c2c5 e7d7 f1b5"),"sicilian-najdorf":("depth-3","black","e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 f1b5 f6d7 c1g5 h7h6 d1h5 d8b6 c2c3 b8c6 b5c6 b7c6 b2b4 c6c5 b4c5 b6c5 f2f4 a8b8 e1f1 b8b2 g2g4 c5c4 f1g1 c4d3 b1a3 d3e3 g1f1 e3f2"),"italian-game":("depth-4","white","e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 e1g1 f6e4 c4d5 f7f5 f3e5 c5f2 f1f2 e4f2 d1h5 e8e7 h5f5 f2d1 d2d4 h8f8 e5c6 d7c6 f5e5 e7d7 e5e6"),"ruy-lopez-berlin":("nodes-100k","black","e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1 f6e4 f1e1 e4g5 f3e5 g5e6 b1c3 c6e5 e1e5 c7c6 b5d3 d7d5 a2a4 c8d7 g2g4 g7g6 e5e1 h7h5 g4h5 d8h4 h5g6 h4h2 g1f1 h2h3 f1g1 h3h1"),"slav-defence":("nodes-250k","white","d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 a2a4 d8a5 c1d2 c8e6 e2e4 b8d7 f1e2 a5b6 e1g1 e8c8 a4a5 b6b2 f3g5 c6c5 a5a6 b7a6 d1a4 b2d2 e2c4 d2g5 a4a6 c8c7 a6a7 c7d6 a1a6 d7b6 a6b6"),"philidor-defence":("nodes-500k","black","e2e4 e7e5 g1f3 d7d6 d2d4 g8f6 b1c3 b8d7 c1e3 e5d4 f3d4 d6d5 e4d5 f8b4 e3g5 e8g8 a2a3 b4c3 b2c3 d7e5 f2f4 c8g4 d1b1 f8e8 g5f6 d8f6 f4e5 e8e5 e1d2 c7c5 d5c6 b7c6 b1b4 f6f4 d2d3 f4e4 d3d2 e4e3")}
def P(p,b):
 r=U.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with U.urlopen(r) as x:return json.load(x)
def W(f):
 d={}
 for i,r in enumerate(f.split()[0].split("/")):
  n=0
  for c in r:
   if c.isdigit():n+=int(c)
   else:d["abcdefgh"[n]+str(8-i)]=c;n+=1
 return d
def A(d,s,w):
 x=ord(s[0])-97;y=int(s[1])-1
 for q,p in d.items():
  if p.isupper()!=w:continue
  a=p.lower();u=ord(q[0])-97;v=int(q[1])-1;dx=x-u;dy=y-v
  if a=="p":
   if dy==(1 if w else -1) and abs(dx)==1:return 1
  elif a=="n":
   if sorted((abs(dx),abs(dy)))==[1,2]:return 1
  elif a=="k":
   if max(abs(dx),abs(dy))==1:return 1
  elif a in"brq" and (dx==0 or dy==0 or abs(dx)==abs(dy)):
   if a=="b" and abs(dx)!=abs(dy):continue
   if a=="r" and dx and dy:continue
   sx=(dx>0)-(dx<0);sy=(dy>0)-(dy<0);i=u+sx;j=v+sy
   while (i,j)!=(x,y):
    if chr(97+i)+str(j+1) in d:break
    i+=sx;j+=sy
   else:return 1
 return 0
def M(d,m):
 e=dict(d);p=e.pop(m[:2]);f=m[2:4];g=e.get(f)
 if p.lower()=="p" and m[0]!=m[2] and g is None:e.pop(m[2]+m[1],0)
 e[f]=p.lower() if len(m)>4 else p
 if p.lower()=="k" and abs(ord(m[0])-ord(m[2]))>1:
  r="h" if m[2]=="g" else "a";e[("f" if r=="h" else "d")+m[3]]=e.pop(r+m[1])
 return e
def C(f,L,w):
 d=W(f)
 def k(m):
  a=d[m[:2]].lower();v=d.get(m[2:4])
  if v is None and a=="p" and m[0]!=m[2]:v=d.get(m[2]+m[1])
  t=V[v.lower()] if v else 0;q=V[m[4]] if len(m)>4 else 0;z=M(d,m)
  h=V[a] if a!="k" and A(z,m[2:4],not w) and not A(z,m[2:4],w) else 0
  c=[s for s,p in z.items() if p.lower()=="k" and p.isupper()!=w]
  c=30*A(z,c[0],w) if c else 0
  y=3-abs(3.5-(ord(m[2])-97))-abs(3.5-int(m[3]))
  return(-t,-q,-c,h,-y,V[a],m)
 return min(L,key=k)
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 b=B.get(g["opening"]["id"]);G=g["moves"]
 while g["status"]=="your_move":
  m=None
  if b and b[0]==g["opponent"] and b[1]==g["colour"]:
   q=b[2].split()
   if G==q[:len(G)] and len(G)<len(q):m=q[len(G)]
  if m is None:m=C(g["fen"],g["legal_moves"],g["colour"]=="white")
  g=P("/move",{"game":g["game"],"move":m});G=g["moves"]
