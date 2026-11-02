"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""
import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,          # sampling: lebar citra kerja (piksel)
    "gamma": 1.0,          # < 1 mencerahkan, > 1 menggelapkan
    "clahe_clip": 2.0,     # 0 berarti CLAHE tidak dipakai
    "clahe_tile": 8,
    "penapis": "median",   # "none", "rerata", "gaussian", "median"
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,        # 0 berarti tanpa penajaman
}

def praproses(img_bgr, p=None):
    """Urutan: ubah ukuran -> gamma -> CLAHE kanal V -> redam derau -> tajamkan."""
    p = {**PARAM_BAWAAN, **(p or {})}
    img = img_bgr.copy()
    
    # TODO 1: ubah ukuran agar lebar = p["lebar"], rasio aspek tetap,
    # gunakan interpolation=cv2.INTER_AREA, simpan ke variabel img
    h, w = img.shape[:2]
    if p["lebar"] is not None and w != p["lebar"]:
        target_w = int(p["lebar"])
        target_h = int(round(h * (target_w / float(w))))
        img = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # TODO 2: bila p["gamma"] != 1, terapkan koreksi gamma dengan cv2.LUT
    if p.get("gamma", 1.0) != 1.0:
        g = float(p["gamma"])
        lut = np.array([255.0 * ((i / 255.0) ** g) for i in range(256)]).clip(0, 255).astype(np.uint8)
        img = cv2.LUT(img, lut)
        
    # TODO 3: bila p["clahe_clip"] > 0, ubah ke HSV, terapkan CLAHE pada
    # kanal V saja, lalu kembalikan ke BGR
    if p.get("clahe_clip", 0) > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        tile = int(p.get("clahe_tile", 8))
        clahe = cv2.createCLAHE(clipLimit=float(p["clahe_clip"]), tileGridSize=(tile, tile))
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    # TODO 4: redam derau sesuai p["penapis"], p["kernel"], p["sigma"]
    penapis = p.get("penapis", "none")
    k = int(p.get("kernel", 3))
    if penapis == "median":
        img = cv2.medianBlur(img, k)
    elif penapis == "gaussian":
        sig = float(p.get("sigma", 1.0))
        img = cv2.GaussianBlur(img, (k, k), sig)
    elif penapis == "rerata":
        img = cv2.blur(img, (k, k))
        
    # TODO 5: bila p["tajam_k"] > 0, lakukan unsharp masking
    if p.get("tajam_k", 0) > 0:
        tk = float(p["tajam_k"])
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1.0 + tk, blur, -tk, 0)
        
    return img

def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
