import colorsys
import os
from PIL import Image

THEME_SPECS = {
    "green": {
        "name": "Dark Forest Green",
        "hex": "#127b37",
        "target_h": 141 / 360,
        "s_scale": 1.3,
        "s_min": 0.85,
        "v_mult": 0.50,
        "v_cap": 0.50,
    },
    "red": {
        "name": "Discord Red",
        "hex": "#f64d4d",
        "target_h": 0.0,
        "s_scale": 1.05,
        "s_min": 0.65,
        "v_mult": 1.0,
        "v_cap": 1.0,
    },
    "default": {
        "name": "Original Discord Blue",
        "hex": "#5662f6",
        "target_h": 235.5 / 360,
        "s_scale": 1.0,
        "s_min": 0.65,
        "v_mult": 1.0,
        "v_cap": 1.0,
    }
}

def shift_pixel(r, g, b, theme="green"):
    if theme == "default":
        # For default restore, we shift any previously recolored pixels back to Discord blue #5662f6
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        deg = h * 360
        if (deg <= 25 or deg >= 335 or 70 <= deg <= 175) and s > 0.15:
            nr, ng, nb = colorsys.hsv_to_rgb(235.5 / 360, 0.65, 0.965)
            return int(nr * 255), int(ng * 255), int(nb * 255)
        return r, g, b

    spec = THEME_SPECS.get(theme, THEME_SPECS["green"])
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    deg = h * 360

    # Match blurple (185-305), green (75-175), or red (<=25 or >=335) with saturation
    if (185 <= deg <= 305 or 75 <= deg <= 175 or deg <= 25 or deg >= 335) and s > 0.15:
        target_s = min(max(s * spec["s_scale"], spec["s_min"]), 1.0)
        target_v = min(v, 1.0) * spec["v_mult"] if v > 0.65 else min(v, spec["v_cap"])
        nr, ng, nb = colorsys.hsv_to_rgb(spec["target_h"], target_s, target_v)
        return int(nr * 255), int(ng * 255), int(nb * 255)

    return r, g, b

def recolor_image(img, theme="green"):
    img = img.convert("RGBA")
    px = img.load()
    changed = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a > 10:
                nr, ng, nb = shift_pixel(r, g, b, theme)
                if (nr, ng, nb) != (r, g, b):
                    changed += 1
                px[x, y] = (nr, ng, nb, a)
    return img, changed

def build_multiscale_ico(src_ico_path, output_ico_path, theme="green"):
    ico = Image.open(src_ico_path)
    if hasattr(ico, "ico") and (256, 256) in getattr(ico, "info", {}).get("sizes", set()):
        base_img = ico.ico.getimage((256, 256))
    else:
        base_img = ico.convert("RGBA")

    if theme == "default":
        # Keep pristine original
        recolored = base_img.copy()
    else:
        recolored, _ = recolor_image(base_img, theme)

    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)]
    frames = [recolored.resize(s, Image.Resampling.LANCZOS) for s in sizes]
    os.makedirs(os.path.dirname(output_ico_path), exist_ok=True)
    frames[0].save(output_ico_path, format="ICO", sizes=sizes, append_images=frames[1:])
    return output_ico_path

def recolor_tray_pngs(tray_files, theme="green"):
    ok = 0
    fail = 0
    for p in tray_files:
        try:
            img = Image.open(p)
            img, n = recolor_image(img, theme)
            if n > 0:
                img.save(p, format="PNG")
            ok += 1
        except Exception as e:
            fail += 1
    return ok, fail
