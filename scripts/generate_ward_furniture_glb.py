
"""Generate lightweight GLB furniture models for the Streamlit ward viewer.
No external geometry packages are required; the script writes valid binary glTF 2.0.
"""
from __future__ import annotations

import json, math, struct
from pathlib import Path
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "models" / "ward_furniture"
OUT.mkdir(parents=True, exist_ok=True)

@dataclass
class Prim:
    name: str
    positions: list[tuple[float,float,float]]
    normals: list[tuple[float,float,float]]
    indices: list[int]
    material: int

MATS = [
    ("bed blue", (0.50,0.72,1.00,1)), ("white ceramic", (0.98,0.99,1.0,1)),
    # Keep equipment outlines visible without turning small details into black blobs in the WebGL viewer.
    ("light satin metal", (0.58,0.66,0.76,1)), ("soft grey", (0.76,0.82,0.90,1)),
    ("glass blue", (0.62,0.82,1.0,0.42)), ("warm wood", (0.82,0.62,0.38,1)),
    ("green clinical", (0.60,0.90,0.76,1)), ("red clinical", (0.95,0.42,0.40,1)),
    ("yellow ppe", (1.00,0.84,0.32,1)), ("teal screen", (0.42,0.86,0.92,1)),
]
MAT = {name:i for i,(name,_) in enumerate(MATS)}
MAT['dark metal'] = MAT['light satin metal']  # Backward-compatible alias for model definitions.

def transform(v, loc=(0,0,0), scale=(1,1,1)):
    return (v[0]*scale[0]+loc[0], v[1]*scale[1]+loc[1], v[2]*scale[2]+loc[2])

def box(name, sx, sy, sz, loc=(0,0,0), mat=0):
    x=sx/2; y=sy/2; z=sz/2
    faces=[
        ([(x,-y,-z),(x,-y,z),(x,y,z),(x,y,-z)],(1,0,0)),
        ([(-x,-y,z),(-x,-y,-z),(-x,y,-z),(-x,y,z)],(-1,0,0)),
        ([(-x,y,-z),(x,y,-z),(x,y,z),(-x,y,z)],(0,1,0)),
        ([(-x,-y,z),(x,-y,z),(x,-y,-z),(-x,-y,-z)],(0,-1,0)),
        ([(-x,-y,z),(-x,y,z),(x,y,z),(x,-y,z)],(0,0,1)),
        ([(-x,y,-z),(-x,-y,-z),(x,-y,-z),(x,y,-z)],(0,0,-1)),
    ]
    pos=[]; nor=[]; idx=[]
    for verts,n in faces:
        base=len(pos); pos += [transform(v,loc) for v in verts]; nor += [n]*4; idx += [base,base+1,base+2, base,base+2,base+3]
    return Prim(name,pos,nor,idx,mat)

def cyl(name, rx, rz, h, loc=(0,0,0), mat=0, seg=32):
    pos=[]; nor=[]; idx=[]
    # side verts bottom/top pairs, y up
    for i in range(seg):
        a=2*math.pi*i/seg; ca=math.cos(a); sa=math.sin(a)
        n=(ca,0,sa); pos.append((loc[0]+rx*ca,loc[1],loc[2]+rz*sa)); pos.append((loc[0]+rx*ca,loc[1]+h,loc[2]+rz*sa)); nor += [n,n]
    for i in range(seg):
        j=(i+1)%seg; idx += [2*i,2*j,2*j+1, 2*i,2*j+1,2*i+1]
    cb=len(pos); pos.append(loc); nor.append((0,-1,0))
    ct=len(pos); pos.append((loc[0],loc[1]+h,loc[2])); nor.append((0,1,0))
    for i in range(seg):
        j=(i+1)%seg; idx += [cb,2*j,2*i, ct,2*i+1,2*j+1]
    return Prim(name,pos,nor,idx,mat)

def ellipsoid(name, rx, ry, rz, loc=(0,0,0), mat=0, rings=8, seg=24, upper_only=False):
    pos=[]; nor=[]; idx=[]
    theta0 = 0 if upper_only else -math.pi/2
    theta1 = math.pi/2
    for r in range(rings+1):
        t=theta0+(theta1-theta0)*r/rings
        ct=math.cos(t); st=math.sin(t)
        for s in range(seg):
            a=2*math.pi*s/seg; ca=math.cos(a); sa=math.sin(a)
            x=rx*ct*ca; y=ry*st; z=rz*ct*sa
            pos.append((loc[0]+x,loc[1]+y+ry*(1 if upper_only else 0),loc[2]+z))
            ln=math.sqrt((ct*ca)**2+st**2+(ct*sa)**2) or 1
            nor.append((ct*ca/ln, st/ln, ct*sa/ln))
    for r in range(rings):
        for s in range(seg):
            a=r*seg+s; b=r*seg+(s+1)%seg; c=(r+1)*seg+(s+1)%seg; d=(r+1)*seg+s
            idx += [a,b,c, a,c,d]
    return Prim(name,pos,nor,idx,mat)

def torus(name, major, minor, loc=(0,0,0), mat=0, seg=32, tube=10):
    pos=[]; nor=[]; idx=[]
    for i in range(seg):
        a=2*math.pi*i/seg; ca=math.cos(a); sa=math.sin(a)
        for j in range(tube):
            b=2*math.pi*j/tube; cb=math.cos(b); sb=math.sin(b)
            x=(major+minor*cb)*ca; y=minor*sb; z=(major+minor*cb)*sa
            pos.append((loc[0]+x,loc[1]+y,loc[2]+z)); nor.append((cb*ca,sb,cb*sa))
    for i in range(seg):
        for j in range(tube):
            a=i*tube+j; b=i*tube+(j+1)%tube; c=((i+1)%seg)*tube+(j+1)%tube; d=((i+1)%seg)*tube+j
            idx += [a,b,c, a,c,d]
    return Prim(name,pos,nor,idx,mat)

def write_glb(path: Path, prims: list[Prim]):
    bin_blob=bytearray(); buffer_views=[]; accessors=[]; meshes=[]; nodes=[]
    def pad4(b):
        while len(b)%4: b.append(0)
    for p in prims:
        node_index=len(nodes)
        prim_json={"attributes":{},"indices":None,"material":p.material}
        for key,data,ctype,typ in [("POSITION",p.positions,5126,"VEC3"),("NORMAL",p.normals,5126,"VEC3")]:
            pad4(bin_blob); off=len(bin_blob)
            for v in data: bin_blob.extend(struct.pack('<3f',*v))
            buffer_views.append({"buffer":0,"byteOffset":off,"byteLength":len(bin_blob)-off,"target":34962})
            vals=[c for v in data for c in v]
            acc={"bufferView":len(buffer_views)-1,"componentType":ctype,"count":len(data),"type":typ}
            if key=="POSITION":
                acc["min"]=[min(v[i] for v in data) for i in range(3)]; acc["max"]=[max(v[i] for v in data) for i in range(3)]
            accessors.append(acc); prim_json["attributes"][key]=len(accessors)-1
        pad4(bin_blob); off=len(bin_blob)
        use_u32=max(p.indices)>65535
        fmt='<I' if use_u32 else '<H'; comp=5125 if use_u32 else 5123
        for ix in p.indices: bin_blob.extend(struct.pack(fmt,ix))
        buffer_views.append({"buffer":0,"byteOffset":off,"byteLength":len(bin_blob)-off,"target":34963})
        accessors.append({"bufferView":len(buffer_views)-1,"componentType":comp,"count":len(p.indices),"type":"SCALAR"})
        prim_json["indices"]=len(accessors)-1
        meshes.append({"name":p.name,"primitives":[prim_json]})
        nodes.append({"name":p.name,"mesh":len(meshes)-1})
    materials=[]
    for name,rgba in MATS:
        materials.append({"name":name,"pbrMetallicRoughness":{"baseColorFactor":rgba,"roughnessFactor":0.82,"metallicFactor":0.0},"alphaMode":"BLEND" if rgba[3]<1 else "OPAQUE"})
    gltf={"asset":{"version":"2.0","generator":"ward-furniture-generator"},"scene":0,"scenes":[{"nodes":list(range(len(nodes)))}],"nodes":nodes,"meshes":meshes,"materials":materials,"buffers":[{"byteLength":len(bin_blob)}],"bufferViews":buffer_views,"accessors":accessors}
    j=json.dumps(gltf,separators=(',',':')).encode(); j += b' ' * ((4-len(j)%4)%4)
    pad4(bin_blob)
    total=12+8+len(j)+8+len(bin_blob)
    with path.open('wb') as f:
        f.write(struct.pack('<4sII',b'glTF',2,total)); f.write(struct.pack('<I4s',len(j),b'JSON')); f.write(j); f.write(struct.pack('<I4s',len(bin_blob),b'BIN\0')); f.write(bin_blob)

def model_patient_bed():
    return [box('hospital bed wheeled steel frame',1.0,.10,.55,(0,.10,0),MAT['dark metal']), ellipsoid('single curved blue hospital mattress',.44,.10,.24,(0,.21,0),MAT['bed blue'], upper_only=True), ellipsoid('raised pillow cushion',.28,.06,.11,(-.23,.37,-.12),MAT['white ceramic'], upper_only=True), box('tall bed headboard',.08,.42,.60,(-.54,.24,0),MAT['dark metal']), cyl('left tubular side rail',.018,.018,.48,(0,.30,-.31),MAT['dark metal'],16), cyl('right tubular side rail',.018,.018,.48,(0,.30,.31),MAT['dark metal'],16), cyl('iv pole',.014,.014,.72,(.48,.10,-.28),MAT['dark metal'],12), ellipsoid('hanging iv bag',.055,.075,.025,(.48,.82,-.28),MAT['yellow ppe'])]
def model_toilet():
    return [box('toilet base plinth',.42,.08,.48,(0,.04,0),MAT['soft grey']), ellipsoid('rounded ceramic toilet bowl',.23,.14,.19,(0,.10,.04),MAT['white ceramic'],upper_only=True), torus('open toilet seat ring',.17,.025,(0,.28,.04),MAT['dark metal']), box('rectangular flush tank',.44,.25,.12,(-.02,.20,-.25),MAT['white ceramic'])]
def model_basin():
    return [box('wall bracket panel',.55,.25,.08,(0,.13,-.18),MAT['soft grey']), ellipsoid('deep wall hung basin bowl',.34,.12,.22,(0,.18,.02),MAT['white ceramic'],upper_only=True), torus('thin blue basin rim',.24,.018,(0,.36,.02),MAT['teal screen']), cyl('short faucet stem',.018,.018,.18,(0,.34,-.11),MAT['dark metal'],12), ellipsoid('dark drain',.035,.012,.035,(0,.38,.03),MAT['dark metal'])]
def model_shower():
    return [box('low shower tray',.72,.05,.72,(0,.025,0),MAT['bed blue']), box('transparent shower glass screen',.72,.45,.035,(0,.25,-.34),MAT['glass blue']), cyl('shower riser pipe',.014,.014,.62,(.26,.05,-.25),MAT['dark metal'],12), ellipsoid('round shower head',.07,.035,.07,(.26,.70,-.25),MAT['teal screen'])]
def model_counter():
    return [box('long curved nurse counter front',1.05,.22,.24,(0,.11,0),MAT['green clinical']), box('perpendicular return counter wing',.25,.22,.62,(.40,.11,.20),MAT['green clinical']), box('monitor one',.16,.12,.025,(-.20,.34,-.02),MAT['dark metal']), box('monitor two',.16,.12,.025,(.06,.34,-.02),MAT['dark metal'])]
def model_cart():
    return [box('medical cart body with drawer stack',.38,.42,.32,(0,.26,0),MAT['teal screen']), box('top tray lip',.44,.045,.38,(0,.50,0),MAT['dark metal']), cyl('left cart handle post',.015,.015,.42,(-.24,.24,-.17),MAT['dark metal'],12), cyl('right cart handle post',.015,.015,.42,(-.24,.24,.17),MAT['dark metal'],12), *[cyl('small caster wheel',.045,.045,.035,(x,.02,z),MAT['dark metal'],12) for x in (-.17,.17) for z in (-.14,.14)]]
def model_shelf():
    return [box('open supply shelving tall frame',.38,.72,.18,(0,.36,0),MAT['green clinical']), box('shelf level 1',.42,.035,.22,(0,.18,0),MAT['white ceramic']), box('shelf level 2',.42,.035,.22,(0,.38,0),MAT['white ceramic']), box('shelf level 3',.42,.035,.22,(0,.58,0),MAT['white ceramic'])]
def model_bench(): return [box('ppe bench wooden seat',.72,.12,.22,(0,.28,0),MAT['warm wood']), *[cyl('bench round leg',.025,.025,.26,(x,0,z),MAT['dark metal'],10) for x in (-.28,.28) for z in (-.08,.08)]]
def model_cabinet(): return [box('tall ppe cabinet body',.38,.82,.28,(0,.41,0),MAT['yellow ppe']), box('cabinet door seam',.015,.76,.30,(0,.43,0),MAT['dark metal'])]
def model_waste_bin(): return [cyl('round clinical waste bin tapered body',.17,.17,.34,(0,.02,0),MAT['red clinical'],28), torus('dark waste bin rim',.17,.018,(0,.38,0),MAT['dark metal'])]
def model_worktop(): return [box('dirty utility worktop with sink',.78,.18,.28,(0,.24,0),MAT['red clinical']), ellipsoid('small inset utility sink',.16,.035,.10,(.20,.36,0),MAT['white ceramic'],upper_only=True)]
def model_headwall(): return [box('medical gas headwall rail panel',.78,.42,.08,(0,.28,0),MAT['dark metal']), box('oxygen outlet green block',.12,.08,.04,(-.22,.44,.05),MAT['green clinical']), box('suction outlet red block',.12,.08,.04,(0,.44,.05),MAT['red clinical']), box('call outlet yellow block',.12,.08,.04,(.22,.44,.05),MAT['yellow ppe'])]
def model_bedside_table(): return [box('compact bedside cabinet body',.28,.34,.24,(0,.20,0),MAT['soft grey']), box('drawer dark reveal line',.30,.025,.25,(0,.31,0),MAT['dark metal']), box('small overbed tray top',.34,.035,.28,(0,.39,0),MAT['white ceramic'])]

models={
 'hospital_bed.glb':model_patient_bed(), 'headwall.glb':model_headwall(), 'bedside_table.glb':model_bedside_table(), 'toilet.glb':model_toilet(), 'washbasin.glb':model_basin(), 'shower.glb':model_shower(), 'nurse_counter.glb':model_counter(), 'medical_cart.glb':model_cart(), 'supply_shelf.glb':model_shelf(), 'ppe_bench.glb':model_bench(), 'ppe_cabinet.glb':model_cabinet(), 'waste_bin.glb':model_waste_bin(), 'dirty_worktop.glb':model_worktop()
}
for name,prims in models.items(): write_glb(OUT/name, prims)
print(f'wrote {len(models)} GLB furniture models to {OUT}')
