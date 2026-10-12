# WeatherNext Map Visual V14 - Real Himawari VIS/IR

**2026-10-12 | FRONTEND LAB ONLY | VISUAL REVIEW CANDIDATE | HOLD production**

This is an isolated, map-first Phú Quốc weather visualization with authentic geospatial data. **It is not live weather and not an approved release.** No API, forecast model, ingest, scheduler, database, authentication, CMS, Cloudflare route, Core V1.2, or production WeatherNext was changed.

## What changed since V13

- Real Himawari-9 imagery for six matching UTC observations on **11 October 2026**: 03:30, 05:30, 05:40, 06:00, 06:10 and 06:30 UTC (Vietnam +07:00). Frames are unevenly spaced.
- The **B02 visible 0.51 μm** radiance-to-reflectance field (nominal 1 km resolution at sub-satellite point) was combined with authentic **B13 infrared 10.4 μm brightness temperature** (nominal 2 km). The composite is a *visual enhancement of source observations*, not a natural-color RGB capture or a measured rain-radar product.
- Optical reflectance is emphasized as white/gray only where measured albedo is high; infrared background represents measured thermal brightness. **A bright visible pixel may be land, haze, or cloud; cloud membership is NOT independently classified.**
- 640×640 WGS84 PNG render grid over bounding box **W 103.55, S 9.76, E 104.45, N 10.66**. Resampling does **not** change the native sensor resolution or guarantee cloud parallax-free positioning.
- Real OSM/OpenFreeMap vector geography with coastline, road labels and islets. Historical **Sentinel-2 cloudless 2016/2017 by EOX IT Services GmbH** contributes the geographic photographic underlay. It is **not** the current sky and is labeled with Copernicus/EOX credit.

## Data contracts

- Source files for each observation: NOAA Open Data bucket `noaa-himawari9`, paths `AHI-L1b-FLDK/2026/10/11/<HHMM>/HS_H09_20261011_<HHMM>_B02_FLDK_R10_S0410.DAT.bz2`, `S0510`; and matching `B13_FLDK_R20_S0410`, `S0510`.
- Calibration uses each file's HSD header gain/offset, reflectance coefficient (B02), Planck/B13 infrared coefficients and geostationary projection parameters. No procedural noise, fake rain blobs, AI weather imagery, or invented coastlines.
- Rain color fields remain an **archived ECMWF model 0.5°** visualization. The accumulation interval of the old fixture is not verified, so units are intentionally **mm / kỳ mẫu**, *not mm/h, mm/3h or live radar*. Wind particles follow archived U/V model vectors and projected map coordinates; wave/temperature are *fixture-only* pending data-owner validation.
- VRain station examples are archival/stale and must not be advertised as current observations.
- In cloud mode, if a required satellite PNG is missing/undecodable, the app hides that unverified image and explicitly labels the **0.075° archived cloud-top grid fallback**. The fallback is **not** the real VIS/IR image.

## Tests

- On PHUQUOCLUX Windows isolated Chromium, verified MapLibre vector tiles, historical basemap, satellite composite, each of the five modes, six non-uniform timeline frames, zoom/pan, 390×844 mobile and 1440×900 desktop snapshots and 360×780 mobile variant.
- Browser JavaScript exceptions: **0** on the captured QA runs. Archived image-source failover: **PASS** in a separate test site intentionally missing the 06:30 UTC composite, while the vector map remained loaded.
- **NOT TESTED:** actual Safari on physical iPhone, full low-speed mobile network stress, long-running memory, or full production API parity. Those remain release blockers.
- This frontend is ready to present for visual review, **not approved** by the user and **not ready for Engine integration**.

## Preview

Use a web server (double-click `index.html` from a file:// URL may prevent dependent imagery loading):
```sh
python -m http.server 8766 --bind 127.0.0.1
```
Open `http://127.0.0.1:8766/` while connected to the Internet for OSM/OpenFreeMap/EOX map layers. The six Himawari derived PNG frames are bundled in `ahi/`. No production endpoints or secrets are required.

A GitHub raw-file URL is **not** an interactive preview. Hosted preview services may display an external-content warning before enabling the preview; no login or payment is requested.

## Attribution

Himawari-9 AHI data: Japan Meteorological Agency (JMA), redistributed via NOAA Open Data `noaa-himawari9`; these are independently modified/georeferenced visual composites, not official JMA/NOAA products. Map data © OpenStreetMap contributors, tiles © OpenFreeMap. Historic land imagery Sentinel-2 cloudless, © EOX IT Services GmbH, contains modified Copernicus Sentinel data 2016 & 2017, CC BY 4.0. Retain visible attribution in redistributed previews.

**Safety lock:** no merge, no production deployment, no Core/CMS/DB/auth/scheduler/ingest modification. Handoff to Engine requires explicit user visual approval and revalidation of data contracts.
