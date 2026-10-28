# Scene figures

Draw the actual spatial relationship, start positions, relevant actors, movement and result.
Use a 560-960-wide SVG `viewBox`, text at least 14 SVG units, a transparent background and
sufficient contrast on both light and dark panels. Use outlines/halos where necessary;
color alone cannot distinguish actors. Keep comparable states at the same scale and frame.
For two to four states, label their order visibly and show changed positions, not just captions.
A schematic is not evidence of exact speed, distance or collision behavior.

Use static SVG with no scripts, event handlers, foreign objects, external resources or fonts.
Rasterize at 2x using `node <package>/scripts/svg_to_png.mjs input.svg output.png`.
The helper loads SVG as an image, with network blocked, so SVG scripts cannot execute.
It requires installed Chrome/Chromium and Node 18+; set `CHROME_PATH` to an existing executable
when discovery cannot find it. Missing Chrome is `Blocked`, not permission to install it.
Inspect the result; embed each PNG with meaningful `@image alt=... caption=...`. Keep searchable
explanation outside the raster image, and distinguish illustrative geometry from measured data.
