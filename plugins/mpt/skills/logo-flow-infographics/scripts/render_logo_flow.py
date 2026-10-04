#!/usr/bin/env python3
"""Render an approved local-asset, left-to-right logo flow. No network/install."""
import argparse
import base64
import hashlib
import html
import json
import math
import re
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ALLOWED = {"svg","g","path","defs","linearGradient","radialGradient","stop",
           "clipPath","mask","circle","ellipse","rect","polygon","polyline",
           "line","title","desc","use"}
def fail(message):
    raise ValueError(message)

def read_json(path):
    if path.stat().st_size > 262144:
        fail("JSON input too large")
    return json.loads(path.read_text(encoding="utf-8"))

def number(v, low, high, name):
    if isinstance(v, bool) or not isinstance(v, (int,float)) or not math.isfinite(v) or not low <= v <= high:
        fail("Invalid " + name)
    return v

def text(v, name, limit=500):
    if not isinstance(v,str) or not v.strip() or len(v)>limit:
        fail("Invalid " + name)
    return v

def local_svg(entry, directory):
    for key in ("name","path","sha256","source","license_note"):
        text(entry.get(key), key)
    text(entry["name"], "short asset name", 24)
    path = (directory / entry["path"]).resolve()
    if not path.is_relative_to(directory.resolve()):
        fail("Asset must stay within manifest directory")
    if path.stat().st_size > 262144:
        fail("Asset too large")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=entry["sha256"]:
        fail("Asset size or hash mismatch: " + entry["name"])
    if re.search(br"<!DOCTYPE|<!ENTITY",raw,re.I):
        fail("DTD/entities are unsupported")
    root = ET.fromstring(raw)
    if root.tag != "{"+NS+"}svg":
        fail("Asset must be a namespaced SVG")
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag not in ALLOWED:
            fail("Unsupported SVG element: " + tag)
        for key,value in element.attrib.items():
            key=key.split("}")[-1]
            if key.lower().startswith("on") or key == "base":
                fail("Event attributes and XML base overrides are forbidden")
            if "\\" in value:
                fail("Escaped attribute syntax is unsupported in this restricted SVG subset")
            if key in ("href","src") and not value.startswith("#"):
                fail("Only internal SVG references are supported")
            urls = re.findall(r"url\s*\(([^)]*)\)", value, re.I)
            if "@import" in value.lower() or any(not u.strip().strip("\"'").startswith("#") for u in urls):
                fail("External CSS resource or unsupported URL")
    view = [float(v) for v in re.split(r"[ ,]+",root.get("viewBox","").strip())]
    if len(view)!=4 or not all(math.isfinite(v) for v in view) or view[2]<=0 or view[3]<=0:
        fail("SVG needs a finite positive viewBox")
    # Explicit intrinsic pixels avoid 1em failure and low-resolution nested-image rasterization.
    scale=256/max(view[2:])
    root.set("width",format(view[2]*scale,".8g"))
    root.set("height",format(view[3]*scale,".8g"))
    normalized=ET.tostring(root,encoding="utf-8")
    return "data:image/svg+xml;base64,"+base64.b64encode(normalized).decode(), {
        "name":entry["name"],"source":entry["source"],"license_note":entry["license_note"],
        "original_sha256":entry["sha256"],"normalized_sha256":hashlib.sha256(normalized).hexdigest(),
        "viewbox_width":view[2],"viewbox_height":view[3],
        "normalization":"explicit intrinsic dimensions, maximum 256px; viewBox/geometry/colors retained"}

def build(graph_path):
    graph=read_json(graph_path)
    title=text(graph.get("title"),"title",160)
    text(graph.get("basis"),"source basis")
    description=text(graph.get("description"),"description",2000)
    if graph.get("status") not in ("synthetic","proposed","implemented"):
        fail("Declare synthetic, proposed, or implemented")
    width=number(graph.get("width",800),300,6000,"width")
    height=number(graph.get("height",510),250,6000,"height")
    disclaimer=graph.get("disclaimer","")
    if graph["status"]!="implemented" and not disclaimer:
        fail("Synthetic/proposed graph needs an explicit disclaimer")
    if disclaimer and (not isinstance(disclaimer,str) or len(disclaimer)>120):
        fail("Keep the external disclaimer short")
    manifest_path=(graph_path.parent/text(graph.get("asset_manifest"),"manifest")).resolve()
    manifest=read_json(manifest_path)
    nodes=graph.get("nodes",[]); edges=graph.get("edges",[])
    if not 1<=len(nodes)<=60 or len(edges)>120:
        fail("Unsupported graph size")
    ids={}; prepared=[]; provenance={}
    for node in nodes:
        ident=text(node.get("id"),"node id",64)
        if ident in ids:
            fail("Duplicate node id")
        entry=manifest[node["asset"]]
        if node.get("label",entry["name"])!=entry["name"]:
            fail("Node label must match the asset's accurate name")
        x=number(node.get("x"),0,width-100,"node x")
        y=number(node.get("y"),0,height-(160 if disclaimer else 130),"node y")
        uri,record=local_svg(entry,manifest_path.parent)
        ids[ident]=(x,y)
        fit=64/max(record["viewbox_width"],record["viewbox_height"])
        iw=record["viewbox_width"]*fit; ih=record["viewbox_height"]*fit
        prepared.append((ident,x,y,entry["name"],uri,iw,ih))
        provenance[node["asset"]]=record
    esc=lambda s:html.escape(str(s),quote=True)
    parts=[f'<svg xmlns="{NS}" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="flow-title flow-desc"><title id="flow-title">{esc(title)}</title><desc id="flow-desc">{esc(description)}</desc>',
        '<defs><pattern id="flow-dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#394255"/></pattern><marker id="flow-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#aeb8cb"/></marker></defs>',
        f'<rect width="{width}" height="{height}" fill="#171c28"/><rect width="{width}" height="{height}" fill="url(#flow-dots)"/>']
    for edge in edges:
        x,y=ids[edge["source"]];tx,ty=ids[edge["target"]]
        sx=x+100;sy=y+50;ey=ty+50
        if tx<=sx:
            fail("Helper requires forward left-to-right edges with space between cards")
        mid=(sx+tx)/2
        parts.append(f'<path d="M{sx} {sy}C{mid} {sy} {mid} {ey} {tx} {ey}" fill="none" stroke="#aeb8cb" stroke-width="2.5" marker-end="url(#flow-arrow)"/>')
    for ident,x,y,label,uri,iw,ih in prepared:
        parts.append(f'<g aria-label="{esc(label)}"><rect x="{x}" y="{y}" width="100" height="100" rx="18" fill="#fff" stroke="#8793a8" stroke-width="1.5"/><image x="{x+(100-iw)/2}" y="{y+(100-ih)/2}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/><text x="{x+50}" y="{y+124}" text-anchor="middle" font-family="Noto Sans CJK KR, sans-serif" font-size="16" font-weight="500" fill="#d2daea">{esc(label)}</text></g>')
    if disclaimer:
        parts.append(f'<text x="{width/2}" y="{height-45}" text-anchor="middle" font-family="Noto Sans CJK KR, sans-serif" font-size="16" fill="#d2daea">{esc(disclaimer)}</text>')
    parts.append("</svg>")
    return "".join(parts),{"status":graph["status"],"basis":graph["basis"],"assets":provenance,
                           "nodes":len(nodes),"edges":len(edges),"pixel_inspection":"required"}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph",type=Path)
    parser.add_argument("--svg",type=Path,required=True)
    parser.add_argument("--png",type=Path)
    args=parser.parse_args()
    svg,manifest=build(args.graph.resolve())
    output=args.svg.resolve();output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(svg,encoding="utf-8")
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    if args.png:
        renderer=shutil.which("inkscape")
        if not renderer:
            fail("SVG saved; PNG needs already installed Inkscape. No installation attempted.")
        png=args.png.resolve();png.parent.mkdir(parents=True,exist_ok=True)
        result=subprocess.run([renderer,str(output),"--export-type=png","--export-filename="+str(png)],capture_output=True,text=True,timeout=60)
        if result.returncode or not png.is_file() or png.read_bytes()[:8]!=b"\x89PNG\r\n\x1a\n":
            fail("PNG export failed; inspect renderer output: "+result.stderr[-1200:])
    print(json.dumps({"svg":str(output),"png":str(args.png.resolve()) if args.png else None,
                      "pixel_inspection":"required; renderer exit0 is not visual verification"}))
if __name__=="__main__":
    main()
