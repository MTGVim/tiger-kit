from __future__ import annotations

import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib
from unittest.mock import patch

from test_optional_media import movie, png


def rectangles(path, width, height, boxes):
    data = bytearray(bytes((48, 90, 130))*width*height)
    for (x,y,w,h), color in boxes:
        for row in range(y,y+h):
            start = (row*width+x)*3
            data[start:start+w*3] = bytes(color)*w
    def chunk(kind, payload):
        return struct.pack(">I",len(payload))+kind+payload+struct.pack(">I",zlib.crc32(kind+payload))
    pixels = b"".join(b"\0"+data[y*width*3:(y+1)*width*3] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,2,0,0,0))+
                     chunk(b"IDAT",zlib.compress(pixels))+chunk(b"IEND",b""))


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "media tools unavailable")
class VideoPresentationTests(unittest.TestCase):
    def setUp(self):
        if not movie.subtitle_filter(): self.skipTest("subtitles filter unavailable")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        png(self.root/"frame.png",(48,90,130),640,360)
        self.data = {"mode":"evidence","source_fps":20,"end_ms":3000,
            "frames":[{"path":str(self.root/"frame.png"),"timestamp_ms":0}],
            "captions":[{"start_ms":0,"end_ms":3000,"text":"Wide WWW and narrow iii"}]}

    def build(self, name):
        manifest = self.root/"manifest.json";manifest.write_text(json.dumps(self.data))
        return movie.build(manifest,self.root/name)

    def pixels(self, result, seconds=1.5):
        return subprocess.run([result["ffmpeg_path"],"-v","error","-ss",str(seconds),"-i",result["path"],
            "-frames:v","1","-threads","1","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True,check=True).stdout

    def bounds(self, raw, predicate):
        hits = [i//3 for i in range(0,len(raw),3) if predicate(*raw[i:i+3])]
        self.assertTrue(hits)
        return (min(n%640 for n in hits),min(n//640 for n in hits),max(n%640 for n in hits),max(n//640 for n in hits))

    def test_overlay_variants_keep_height_srt_and_symmetric_ink_padding(self):
        source = (self.root/"frame.png").read_bytes()
        for style in ("overlay","overlay-rounded"):
            self.data["caption_style"] = style
            result = self.build(style+".mp4")
            self.assertEqual((result["width"],result["height"],result["caption_band_px"]),(640,360,0))
            self.assertIn(self.data["captions"][0]["text"],Path(result["captions_path"]).read_text())
            raw = self.pixels(result)
            ink = self.bounds(raw, lambda r,g,b: min(r,g,b)>200)
            box = self.bounds(raw, lambda r,g,b: r<35 and g<65 and b<95)
            self.assertLessEqual(abs((ink[0]-box[0])-(box[2]-ink[2])),result["caption_size_px"]*.3)
            self.assertGreater(ink[1],300)
            self.assertEqual(result["media_status"],"ready")
        self.assertEqual(source,(self.root/"frame.png").read_bytes())

    def test_caption_moves_for_any_overlapping_time_and_clear_caption_stays_bottom(self):
        self.data["caption_style"]="overlay-rounded"
        self.data["captions"]=[{"start_ms":0,"end_ms":1500,"text":"Keep the target visible"},
                               {"start_ms":1500,"end_ms":3000,"text":"Return to the lower position"}]
        self.data["highlights"]=[{"start_ms":1000,"end_ms":1500,"zoom":False,
            "rects":[{"x":200,"y":285,"w":240,"h":65}]}]
        result=self.build("collision.mp4")
        self.assertEqual([r["position"] for r in result["presentation"]["caption_boxes"]],["top","bottom"])
        self.assertTrue(any("caption moved to top to keep highlights visible: 0ms" in w for w in result["warnings"]))
        first=self.bounds(self.pixels(result,.2),lambda r,g,b:min(r,g,b)>200)
        last=self.bounds(self.pixels(result,2),lambda r,g,b:min(r,g,b)>200)
        self.assertLess(first[3],80);self.assertGreater(last[1],300)

    def test_zoom_preserves_all_targets_and_card_with_continuous_motion(self):
        targets=[({"x":260,"y":240,"w":80,"h":55},(20,240,20)),
                 ({"x":400,"y":250,"w":70,"h":45},(240,20,20))]
        rectangles(self.root/"frame.png",640,360,[([r[k] for k in ("x","y","w","h")],c) for r,c in targets])
        self.data["captions"]=[]
        self.data["highlights"]=[{"start_ms":500,"end_ms":2500,"rects":[r for r,c in targets]}]
        self.data["callouts"]=[{"start_ms":500,"end_ms":2500,"x":260,"y":150,"text":"Two distinct groups","size":18}]
        result=self.build("zoom.mp4")
        mid=self.pixels(result,1.5)
        for predicate in (lambda r,g,b:g>190 and r<60 and b<60,lambda r,g,b:r>190 and g<60 and b<60):
            box=self.bounds(mid,predicate)
            self.assertTrue(0<box[0]<box[2]<639 and 0<box[1]<box[3]<359)
        # The white card and all colored targets are visibly within the actual decoded frame.
        card=self.bounds(mid,lambda r,g,b:min(r,g,b)>225)
        self.assertTrue(0<card[0]<card[2]<639 and 0<card[1]<card[3]<359)
        green=lambda r,g,b:g>190 and r<60 and b<60
        widths=[]
        for t in (.5,.6,.7,.8,.9,1.,2.,2.1,2.2,2.3,2.4,2.5):
            b=self.bounds(self.pixels(result,t),green);widths.append(b[2]-b[0])
        self.assertEqual(widths[:6],sorted(widths[:6]))
        self.assertEqual(widths[6:],sorted(widths[6:],reverse=True))
        self.assertGreater(widths[5],widths[0]+15)
        self.assertLess(max(abs(a-b) for a,b in zip(widths,widths[1:])),20)

    def test_literal_ass_text_cannot_inject_position_or_drawing(self):
        self.data["caption_style"]="overlay-rounded"
        self.data["captions"][0]["text"]=r"Literal {\pos(0,0)\p1} text"
        result=self.build("literal.mp4")
        box=self.bounds(self.pixels(result),lambda r,g,b:min(r,g,b)>200)
        self.assertGreater(box[1],300)
        self.assertIn(self.data["captions"][0]["text"],Path(result["captions_path"]).read_text())

    def test_multiline_card_has_balanced_actual_vertical_padding(self):
        self.data["captions"]=[]
        self.data["callouts"]=[{"start_ms":0,"end_ms":3000,"x":100,"y":110,"size":24,
            "text":"Revenue and margin\nCompare the group totals"}]
        result=self.build("card.mp4");raw=self.pixels(result)
        card=self.bounds(raw,lambda r,g,b:min(r,g,b)>225)
        ink=self.bounds(raw,lambda r,g,b:max(r,g,b)<75)
        self.assertLessEqual(abs((ink[1]-card[1])-(card[3]-ink[3])),24*.2)

    def test_ass_rounded_interval_protects_card_on_fractional_output_frame(self):
        self.data.update(source_fps=30,caption_style="overlay-rounded")
        self.data["callouts"]=[{"start_ms":34,"end_ms":65,"x":260,"y":310,"size":12,"text":"CARD"}]
        result=self.build("quantized.mp4")
        self.assertEqual(result["presentation"]["caption_boxes"][0]["position"],"top")
        self.assertEqual(result["presentation"]["callout_boxes"][0]["render_start_ms"],30)
        raw=self.pixels(result,1/30)
        # Card and caption are both rendered, in separate vertical regions.
        white=self.bounds(raw,lambda r,g,b:min(r,g,b)>225)
        self.assertLess(white[1],80);self.assertGreater(white[3],310)

    def test_gif_keeps_selected_rounded_captions_and_sidecar(self):
        self.data["caption_style"]="overlay-rounded"
        result=self.build("overlay.gif")
        self.assertEqual((result["height"],result["subtitles"]),(360,"hard"))
        self.assertTrue(Path(result["captions_path"]).is_file())

    def test_noninteger_zoom_preserves_right_and_bottom_border_at_source_edge(self):
        rectangles(self.root/"frame.png",640,360,[([600,320,40,40],(255,255,255)),([602,322,36,36],(20,240,20))])
        self.data["captions"]=[]
        self.data["highlights"]=[{"start_ms":500,"end_ms":2500,"margin":0,"max_scale":1.7,
            "rects":[{"x":600,"y":320,"w":40,"h":40}]}]
        result=self.build("edge.mp4");raw=self.pixels(result)
        right=(325*640+639)*3;bottom=(359*640+605)*3
        self.assertGreater(min(raw[right:right+3]),190)
        self.assertGreater(min(raw[bottom:bottom+3]),190)

    def test_high_zoom_uses_integer_crop_geometry_for_caption_collision(self):
        rectangles(self.root/"frame.png",640,360,[([300,176,20,4],(240,20,20)),([300,197,20,4],(20,240,20))])
        self.data["caption_style"]="overlay-rounded"
        self.data["captions"]=[{"start_ms":1000,"end_ms":2000,"text":"Caption should avoid the target"}]
        self.data["highlights"]=[{"start_ms":500,"end_ms":2500,"margin":0,"max_scale":9.7,
            "rects":[{"x":300,"y":176,"w":20,"h":4},{"x":300,"y":197,"w":20,"h":4}]}]
        # The original float-only check returned a covered lower caption. If the
        # integer crop plus resampling guard leaves neither position clear, reject it.
        with self.assertRaisesRegex(ValueError,"both top and bottom"):
            self.build("high-zoom.mp4")
        self.assertFalse((self.root/"high-zoom.mp4").exists())
        self.data["captions"]=[];clear=self.build("high-zoom-clear.mp4")
        target=self.bounds(self.pixels(clear),lambda r,g,b:g>190 and r<60 and b<60)
        self.assertTrue(0<target[0]<target[2]<639 and 0<target[1]<target[3]<359)

    def test_bad_geometry_overlap_and_both_caption_positions_fail_without_output(self):
        self.data["caption_style"]="overlay-rounded"
        cases=[{"callouts":[{"start_ms":0,"end_ms":3000,"x":630,"y":300,"text":"No room"}]},
               {"highlights":[{"start_ms":0,"end_ms":3000,"rects":[{"x":-1,"y":10,"w":20,"h":20}]}]},
               {"highlights":[{"start_ms":0,"end_ms":3000,"zoom":False,"rects":[{"x":0,"y":0,"w":640,"h":360}]}]},
               {"callouts":[{"start_ms":0,"end_ms":3000,"x":200,"y":100,"text":"Covers target"}],
                "highlights":[{"start_ms":0,"end_ms":3000,"rects":[{"x":180,"y":80,"w":300,"h":100}]}]}]
        for case in cases:
            self.data.pop("callouts",None);self.data.pop("highlights",None);self.data.update(case)
            with self.assertRaises(ValueError): self.build("bad.mp4")
            self.assertFalse((self.root/"bad.mp4").exists())

    def test_captions_off_preserves_selected_callouts_and_capture_zoom(self):
        self.data["caption_style"] = "none"
        self.data["callouts"] = [{"start_ms":0,"end_ms":3000,"x":100,"y":100,"text":"A fact"}]
        self.data["highlights"] = [{"start_ms":500,"end_ms":2500,"zoom":True,
            "rects":[{"x":100,"y":220,"w":160,"h":60}]}]
        result = self.build("callout-without-captions.mp4")
        self.assertEqual(result["media_status"], "ready")
        self.assertEqual(result["subtitles"], "none")
        self.assertEqual(result["height"], 360)
        self.assertEqual(result["presentation"]["caption_boxes"], [])
        self.assertTrue(result["presentation"]["callout_boxes"])
        self.assertTrue(result["presentation"]["zoom_plan"])
        self.assertFalse(Path(result["path"]).with_suffix(".srt").exists())
        self.bounds(self.pixels(result), lambda r,g,b:min(r,g,b)>225)

    def test_missing_libass_blocks_callouts_even_without_captions(self):
        self.data["captions"]=[]
        self.data["callouts"]=[{"start_ms":0,"end_ms":3000,"x":100,"y":100,"text":"A fact"}]
        with patch.object(movie,"media_tools",return_value=(shutil.which("ffmpeg"),shutil.which("ffprobe"),False)):
            result=self.build("blocked.mp4")
        self.assertEqual(result["media_status"],"blocked")
        self.assertEqual(result["prerequisite"],"ffmpeg-subtitles-filter")
        self.assertTrue(Path(result["path"]).is_file())


if __name__=="__main__":unittest.main()
