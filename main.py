import json,os,sys,http.client as H
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)
h=(H.HTTPSConnection if E.startswith("https:") else H.HTTPConnection)(E.split("://")[-1].rstrip("/"))
V={"p":1,"n":3,"b":3,"r":5,"q":9,"k":100}
B={
"semi-slav":("depth-2","white","c4c5 b8d7 g1f3 f6e4 c3e4 d5e4 f3d2 f7f5 f1c4 e6e5 d1b3 b7b5 c4f7 e8e7 b3e6"),
"sicilian-najdorf":("depth-3","black","f1b5 b8c6 d4c6 b7c6 b5c6 c8d7 c6a8 e7e6 a8b7 d8b6 e4e5 d6d5 b7a8 f8c5 e5f6 d7b5 f6g7 c5f2 e1d2 b6d4"),
"italian-game":("depth-4","white","f3h4 f6e4 h4f5 e4f2 d1f3 f2h1 f5g7 e8e7 f3f7 e7d6 g7f5"),
"ruy-lopez-berlin":("nodes-100k","black","f1e1 e4d6 f3e5 f8e7 e5c6 d7c6 b5e2 d6f5 c2c3 e7d6 g2g4 e8f8 g4f5 d8g5 g1f1 g5f5 d2d4 f5h3 f1g1 h3h2 g1f1 h2h1"),
"slav-defence":("nodes-250k","white","g2g3 b7b5 d1c2 c8e6 f3g5 d8d4 f1g2 f6d5 a2a4 b5a4 e1g1 e6g4 c3d5 c6d5 c1d2 g4e2 d2a5 e2f1 c2f5 d4g4 f5f7 e8d7 f7d5 d7c8 d5d8"),
"philidor-defence":("nodes-500k","black","c1e3 h7h5 f1c4 f8e7 e1g1 h5h4 g2g3 d7b6 c4d3 h4g3 h2g3 d8d7 d4e5 d7h3 f3h4 c8g4 d1e1 g4f3 d3b5 e8d8 h4f3 h3h1")}
def P(p,b):
 h.request("POST",p,json.dumps(b),{"content-type":"application/json"})
 r=h.getresponse();d=json.loads(r.read())
 if r.status!=200:raise RuntimeError(r.status,d)
 return d
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
  if not(dx or dy):continue
  if a=="p":
   if dy==(1 if w else -1) and abs(dx)==1:return 1
  elif a=="n":
   if abs(dx*dy)==2:return 1
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
 e[f]=(m[4].upper() if p.isupper() else m[4]) if len(m)>4 else p
 if p.lower()=="k" and abs(ord(m[0])-ord(m[2]))>1:
  r="h" if m[2]=="g" else "a";e[("f" if r=="h" else "d")+m[3]]=e.pop(r+m[1])
 return e
def C(f,L,w):
 d=W(f)
 lead=sum(V[p.lower()]*(1 if p.isupper()==w else -1) for p in d.values())
 def k(m):
  a=d[m[:2]].lower();v=d.get(m[2:4])
  if v is None and a=="p" and m[0]!=m[2]:v=d.get(m[2]+m[1])
  t=V[v.lower()] if v else 0;q=V[m[4]]-1 if len(m)>4 else 0;z=M(d,m)
  risk=V[z[m[2:4]].lower()]*A(z,m[2:4],not w)
  h=max([V[p.lower()] for s,p in z.items() if p.isupper()==w and p.lower()!="k" and A(z,s,not w) and not A(z,s,w)] or [0])
  enemy=next(s for s,p in z.items() if p.lower()=="k" and p.isupper()!=w)
  own=next(s for s,p in z.items() if p.lower()=="k" and p.isupper()==w)
  c=A(z,enemy,w);end=0
  if sum(p.isupper()!=w for p in z.values())==1 and not F(z,enemy,not w):return(-10000 if c else 10000,0,0,0,0,0,m)
  if lead>=5 and len(z)<12:
   x=ord(enemy[0])-97;y=int(enemy[1])-1
   edge=min(x,7-x)+min(y,7-y)
   dist=max(abs(ord(own[0])-ord(enemy[0])),abs(int(own[1])-int(enemy[1])))
   end=edge+dist/4
  y=3-abs(3.5-(ord(m[2])-97))-abs(3.5-int(m[3]))
  return(-t-q+risk,h,end,-c,-y,V[a],m)
 return min(L,key=k)
def F(d,s,w):
 for x in range(max(97,ord(s[0])-1),min(105,ord(s[0])+2)):
  for y in range(max(1,int(s[1])-1),min(9,int(s[1])+2)):
   t=chr(x)+str(y)
   if t!=s and (t not in d or d[t].isupper()!=w) and not A(M(d,s+t),t,not w):return 1
 return 0
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 b=B.get(g["opening"]["id"]);G=g["moves"][8:]
 q=b[2].split() if b and b[0]==g["opponent"] and b[1]==g["colour"] else []
 while g["status"]=="your_move":
  n=len(G)
  m=q[n] if n<len(q) and G==q[:n] and q[n] in g["legal_moves"] else C(g["fen"],g["legal_moves"],g["colour"]=="white")
  g=P("/move",{"game":g["game"],"move":m});G=g["moves"][8:]
