"""Optional libass cards/captions and fixed-canvas zooms; no capture or dependencies."""
from __future__ import annotations

import math
import subprocess


def finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("presentation coordinates, sizes and times must be finite numbers")
    return float(value)


def interval(row, end):
    start, stop = finite(row["start_ms"]), finite(row["end_ms"])
    if not 0 <= start < stop <= end:
        raise ValueError("presentation interval must be inside the movie")
    if round(start / 10) >= round(stop / 10):
        raise ValueError("presentation interval is shorter than ASS centisecond precision")
    return start, stop


def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def rendered_interval(row):
    """Use exactly the centisecond boundaries written to ASS, not pre-quantized times."""
    return round(row["start_ms"]/10)*10, round(row["end_ms"]/10)*10


def intersects(a, b):
    return a[0] < b[0]+b[2] and b[0] < a[0]+a[2] and a[1] < b[1]+b[3] and b[1] < a[1]+a[3]


def union(rects):
    x, y = min(r[0] for r in rects), min(r[1] for r in rects)
    return [x, y, max(r[0]+r[2] for r in rects)-x, max(r[1]+r[3] for r in rects)-y]


def validate(data, width, height, end):
    style = data.get("caption_style", "band")
    if style not in ("band", "overlay", "overlay-rounded"):
        raise ValueError("caption_style must be band, overlay or overlay-rounded")
    calls, highlights = data.get("callouts", []), data.get("highlights", [])
    if not isinstance(calls, list) or not isinstance(highlights, list):
        raise ValueError("callouts and highlights must be lists")
    for row in calls:
        interval(row, end)
        if not isinstance(row.get("text"), str) or not row["text"].strip() or len(row["text"]) > 2000:
            raise ValueError("callout text must contain 1-2000 characters")
        if not 0 <= finite(row["x"]) < width or not 0 <= finite(row["y"]) < height:
            raise ValueError("callout position must be inside the source frame")
        if not 0 < finite(row.get("size", max(12, height*.025))) <= height/2:
            raise ValueError("callout size must be positive and at most half the source height")
    previous_end = 0
    for row in highlights:
        start, stop = interval(row, end)
        if start < previous_end:
            raise ValueError("highlights must be ordered and nonoverlapping; combine simultaneous rects")
        previous_end = stop
        if not isinstance(row.get("zoom", True), bool):
            raise ValueError("highlight zoom must be boolean")
        if not 0 <= finite(row.get("margin", 32)) <= max(width, height):
            raise ValueError("highlight margin must be between zero and the source size")
        if not 1 <= finite(row.get("max_scale", 2)) <= 10:
            raise ValueError("highlight max_scale must be between 1 and 10")
        rects = row.get("rects")
        if not isinstance(rects, list) or not rects:
            raise ValueError("highlight rects must be a nonempty list")
        for rect in rects:
            x, y, w, h = (finite(rect[k]) for k in ("x", "y", "w", "h"))
            if not (0 <= x < x+w <= width and 0 <= y < y+h <= height):
                raise ValueError("highlight rectangle must fit inside the source frame")
    return style, calls, highlights


def ass_time(ms):
    n = round(ms/10)
    return f"{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}"


def literal(text):
    # Braces and backslashes are ASS control syntax, not trusted author markup.
    return text.replace("\\", "\\\ufeff").replace("{", "\\{").replace("}", "\\}").replace("\r", " ").replace("\n", "\\N")


def event(start, stop, layer, text, style="Default"):
    return f"Dialogue: {layer},{ass_time(start)},{ass_time(stop)},{style},,0,0,0,,{text}"


def document(width, height, events):
    return ("[Script Info]\nScriptType: v4.00+\n"
            f"PlayResX: {width}\nPlayResY: {height}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Default,Noto Sans CJK KR,24,&H00FFFFFF,&H00FFFFFF,&HFF000000,&H80000000,"
            "-1,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n"
            "Style: Square,Noto Sans CJK KR,24,&H00FFFFFF,&H00FFFFFF,&HFF000000,&H80000000,"
            "-1,0,0,0,100,100,0,0,4,8,0,7,0,0,0,1\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            + "\n".join(events) + "\n")


class TextMetrics:
    """Measure actual libass ink, using the same font/fallback and filter as final output."""
    def __init__(self, ffmpeg, stage, env):
        self.ffmpeg, self.stage, self.env = ffmpeg, stage, env
        self.cache = {}

    def line(self, text, size):
        key = (text, size)
        if key in self.cache:
            return self.cache[key]
        # Wide, bounded canvas; wrapping is explicit. Oversized candidates are split first.
        width = max(128, math.ceil(min(16384, (len(text)+2)*size*1.5)/2)*2)
        height = max(128, math.ceil(size*4/2)*2)
        tags = f"{{\\an7\\pos(16,16)\\q2\\fs{size:.4f}\\bord0\\shad0}}"
        (self.stage/"measure.ass").write_text(document(width, height, [event(0, 1000, 0, tags+literal(text))]), encoding="utf-8")
        process = subprocess.run([self.ffmpeg, "-v", "info", "-nostdin", "-f", "lavfi", "-i",
            f"color=c=black:s={width}x{height}:r=1:d=1", "-vf", "subtitles=filename=measure.ass",
            "-frames:v", "1", "-threads", "1", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
            cwd=self.stage, env=self.env, capture_output=True, check=True, timeout=60)
        if b"failed to find any fallback" in process.stderr:
            raise ValueError("presentation font lacks a glyph; select an installed font with coverage before assembly")
        raw = process.stdout
        if len(raw) != width*height:
            raise ValueError("unexpected text measurement frame size")
        # Threshold excludes faint antialias fringes, consistently for every line and card.
        rows = [y for y in range(height) if max(raw[y*width:(y+1)*width]) > 32]
        if not rows:
            raise ValueError("presentation text has no visible glyphs")
        left = width; right = 0
        for y in rows:
            row = raw[y*width:(y+1)*width]
            xs = [x for x, v in enumerate(row) if v > 32]
            left, right = min(left, xs[0]), max(right, xs[-1])
        if right >= width-2 or rows[-1] >= height-2:
            raise ValueError("presentation text exceeds the measurement canvas; split the caption")
        result = (right-left+1, rows[-1]-rows[0]+1, left-16, rows[0]-16)
        self.cache[key] = result
        return result

    def wrap(self, text, size, limit):
        if not isinstance(text, str) or not text.strip() or len(text) > 2000 or limit < size:
            raise ValueError("presentation text must fit its available width and contain 1-2000 characters")
        lines = []
        for paragraph in text.replace("\r", " ").splitlines():
            remaining = paragraph.strip()
            while remaining:
                # Bound candidates before measuring; every accepted line is then measured in libass.
                high = min(len(remaining), max(1, int(8000/size)))
                candidate = remaining[:high]
                if self.line(candidate, size)[0] > limit:
                    low = 0
                    while low+1 < high:
                        mid = (low+high)//2
                        if self.line(remaining[:mid].rstrip(), size)[0] <= limit: low = mid
                        else: high = mid
                    high = low
                    if high == 0: raise ValueError("presentation glyph exceeds the available width")
                if high < len(remaining):
                    boundary = remaining.rfind(" ", 0, high+1)
                    if boundary > high*.5: high = boundary
                line = remaining[:high].rstrip()
                lines.append({"text": line, "metrics": self.line(line, size)})
                remaining = remaining[high:].lstrip()
        gap = size*.25
        return {"lines": lines, "width": max(x["metrics"][0] for x in lines),
                "height": sum(x["metrics"][1] for x in lines)+gap*(len(lines)-1), "gap": gap, "size": size}


def rounded_path(w, h, r):
    r = min(r, w/2, h/2); k = r*.55228475
    return (f"m {r:.3f} 0 l {w-r:.3f} 0 b {w-r+k:.3f} 0 {w:.3f} {r-k:.3f} {w:.3f} {r:.3f} "
            f"l {w:.3f} {h-r:.3f} b {w:.3f} {h-r+k:.3f} {w-r+k:.3f} {h:.3f} {w-r:.3f} {h:.3f} "
            f"l {r:.3f} {h:.3f} b {r-k:.3f} {h:.3f} 0 {h-r+k:.3f} 0 {h-r:.3f} "
            f"l 0 {r:.3f} b 0 {r-k:.3f} {r-k:.3f} 0 {r:.3f} 0")


def shape(rect, radius, color, alpha="00", border=0, outline="CBD5E1"):
    x,y,w,h = rect
    return (f"{{\\an7\\pos({x:.4f},{y:.4f})\\p1\\bord{border}\\shad0\\1c&H{color}&"
            f"\\1a&H{alpha}&\\3c&H{outline}&\\3a&H{alpha}&}}"+rounded_path(w,h,radius))


def text_events(block, x, y, start, stop, color="FFFFFF", center=False, square=False):
    events = []
    for line in block["lines"]:
        w,h,dx,dy = line["metrics"]
        left = x+(block["width"]-w)/2 if center else x
        tags = (f"{{\\an7\\pos({left-dx:.4f},{y-dy:.4f})\\q2\\fs{block['size']:.4f}"
                f"\\1c&H{color}&" + (f"\\bord{block['size']*.35:.4f}" if square else "\\bord0") + "\\shad0}")
        events.append(event(start, stop, 2, tags+literal(line["text"]), "Square" if square else "Default"))
        y += h+block["gap"]
    return events


def callout_layout(rows, metrics, width, height):
    calls, events = [], []
    for row in rows:
        size = row.get("size", max(12, height*.025)); pad = size*.6
        x,y = row["x"], row["y"]
        block = metrics.wrap(row["text"], size, min(width*.55, width-x)-2*pad-4)
        w,h = block["width"]+2*pad, block["height"]+2*pad
        # Include the 2px shadow/border in the occupied geometry used by zoom/collisions.
        rect = [x, y, w+4, h+4]
        if x+rect[2] > width or y+rect[3] > height:
            raise ValueError("callout card exceeds the source frame; move or shorten it")
        render_start,render_stop = rendered_interval(row)
        item = {"start_ms": row["start_ms"], "end_ms": row["end_ms"], "rect": rect,
                "render_start_ms":render_start,"render_end_ms":render_stop}
        calls.append(item)
        start,stop = row["start_ms"],row["end_ms"]
        events += [event(start,stop,0,shape([x+2,y+2,w,h],size*.2,"000000","D8")),
                   event(start,stop,1,shape([x,y,w,h],size*.2,"FFFFFF",border=1,outline="E1D5CB")),
                   event(start,stop,1,shape([x,y, max(3,size*.14),h],0,"EB6325"))]
        events += text_events(block,x+pad,y+pad,start,stop,color="2A2117")
    return calls, events


def zoom_plan(rows, calls, width, height):
    plans = []
    for row in rows:
        bounds = [[r[k] for k in ("x","y","w","h")] for r in row["rects"]]
        active = [c["rect"] for c in calls if overlaps((row["start_ms"],row["end_ms"]),rendered_interval(c))]
        if any(intersects(c,r) for c in active for r in bounds):
            raise ValueError("callout overlaps a highlight; move the card before assembly")
        x,y,w,h = union(bounds+active)
        margin = max(2, row.get("margin",32)) # room for zoompan integer/chroma rounding
        left,top,right,bottom = max(0,x-margin),max(0,y-margin),min(width,x+w+margin),min(height,y+h+margin)
        scale = max(1, min(width/(right-left),height/(bottom-top),row.get("max_scale",2))) if row.get("zoom",True) else 1
        crop_w,crop_h = width/scale,height/scale
        cx = max(0,min(width-crop_w,(left+right-crop_w)/2))
        cy = max(0,min(height-crop_h,(top+bottom-crop_h)/2))
        plans.append({"start_ms":row["start_ms"],"end_ms":row["end_ms"],"scale":scale,"x":cx,"y":cy,
                      "rects":bounds,"transition_ms":min(500,(row["end_ms"]-row["start_ms"])/2)})
    for i,c in enumerate(calls):
        if any(overlaps(rendered_interval(c),rendered_interval(d)) and intersects(c["rect"],d["rect"]) for d in calls[:i]):
            raise ValueError("callout cards overlap; move or retime them")
    return plans


def view(plan, t, width, height):
    if plan is None or plan["scale"] <= 1: return 1,0,0
    u = max(0,min(1,(t-plan["start_ms"])/plan["transition_ms"],(plan["end_ms"]-t)/plan["transition_ms"]))
    z = 1+(plan["scale"]-1)*u*u*(3-2*u)
    ratio = (1-1/z)/(1-1/plan["scale"])
    return z, plan["x"]*ratio, plan["y"]*ratio


def zoom_filter(plans, width, height, fps):
    zooms, xs, ys = [], [], []
    for p in plans:
        if p["scale"] <= 1: continue
        t = f"in*1000/({fps})"
        u = f"max(0,min(1,min(({t}-{p['start_ms']})/{p['transition_ms']},({p['end_ms']}-{t})/{p['transition_ms']})))"
        zooms.append(f"({p['scale']-1})*({u})*({u})*(3-2*({u}))")
        active = f"between({t},{p['start_ms']},{p['end_ms']})"
        xs.append(f"if({active},{p['x']}*(1-1/zoom)/(1-1/{p['scale']}),0)")
        ys.append(f"if({active},{p['y']}*(1-1/zoom)/(1-1/{p['scale']}),0)")
    if not zooms: return None
    # Crop in full-resolution RGB: 4:2:0 snaps origins to even pixels and can erase
    # a border flush with the source edge. Ceil plus zoompan's clamp retains that edge.
    return (f"format=gbrp,zoompan=z='1+{'+'.join(zooms)}':x='ceil({'+'.join(xs)})':"
            f"y='ceil({'+'.join(ys)})':d=1:s={width}x{height}:fps={fps}")


def caption_events(captions, style, metrics, width, height, size, plans, calls, fps, warnings):
    events, boxes = [], []
    previous_end = 0
    for row in captions:
        interval(row, float("inf"))
        start,stop = rendered_interval(row)
        if start < previous_end: raise ValueError("overlay captions must be ordered and nonoverlapping")
        previous_end = stop
        if not row["text"].strip(): continue
        block = metrics.wrap(row["text"],size,width*.9-2*size*.5)
        pad = size*.5 if style == "overlay-rounded" else size*.35
        w,h = block["width"]+pad*2,block["height"]+pad*2
        if h > height*.4: raise ValueError("overlay caption is too tall; split its text or reduce caption size")
        bottom = [(width-w)/2,height*.94-h,w,h]
        top = [(width-w)/2,height*.06,w,h]
        # Check every encoded frame, including partial overlaps and transitions, not just midpoint.
        first,last = math.floor(start*fps/1000),math.ceil(stop*fps/1000)
        occupied = []
        for frame in range(first,last+1):
            t = min(stop-.001,max(start,frame*1000/fps))
            plan = next((p for p in plans if p["start_ms"] <= t < p["end_ms"]),None)
            z,x,y = view(plan,t,width,height)
            crop_w,crop_h = max(1,int(width*(1/z))),max(1,int(height*(1/z)))
            x,y = min(math.ceil(x),width-crop_w),min(math.ceil(y),height-crop_h)
            sx,sy = width/crop_w,height/crop_h
            # Protect edge antialiasing and a possible one-pixel floating-point crop
            # difference in FFmpeg; at high zoom that is more than one output pixel.
            guard = max(2,sx,sy)
            rects = list(plan["rects"]) if plan else []
            rects += [c["rect"] for c in calls if rendered_interval(c)[0] <= t < rendered_interval(c)[1]]
            occupied.extend([[(r[0]-x)*sx-guard,(r[1]-y)*sy-guard,r[2]*sx+2*guard,r[3]*sy+2*guard] for r in rects])
        moved = any(intersects(bottom,r) for r in occupied)
        box = top if moved else bottom
        if moved:
            if any(intersects(top,r) for r in occupied):
                raise ValueError("caption overlaps protected content at both top and bottom; use band or reframe the capture")
            warnings.append(f"caption moved to top to keep highlights visible: {row['start_ms']:g}ms")
        if style == "overlay-rounded": events.append(event(start,stop,0,shape(box,size*.22,"000000","80")))
        events += text_events(block,box[0]+pad,box[1]+pad,start,stop,center=True,square=style=="overlay")
        boxes.append({"start_ms":row["start_ms"],"end_ms":row["end_ms"],"render_start_ms":start,"render_end_ms":stop,
                      "rect":box,"position":"top" if moved else "bottom","lines":len(block["lines"])})
    return events,boxes


def prepare(data, captions, width, height, end, size, fps, ffmpeg, stage, env, warnings):
    style, rows, highlights = validate(data,width,height,end)
    metrics = TextMetrics(ffmpeg,stage,env)
    calls, call_events = callout_layout(rows,metrics,width,height)
    plans = zoom_plan(highlights,calls,width,height)
    filters = []
    if call_events:
        (stage/"callouts.ass").write_text(document(width,height,call_events),encoding="utf-8")
        filters.append("subtitles=filename=callouts.ass")
    zoom = zoom_filter(plans,width,height,fps)
    if zoom: filters.append(zoom)
    boxes = []
    if style != "band" and captions:
        events,boxes = caption_events(captions,style,metrics,width,height,size,plans,calls,float(fps),warnings)
        (stage/"overlay-captions.ass").write_text(document(width,height,events),encoding="utf-8")
    return filters,{"caption_style":style,"caption_boxes":boxes,"callout_boxes":calls,"zoom_plan":plans,
                    "text_metrics":"libass-rendered-ink" if calls or boxes else None}
