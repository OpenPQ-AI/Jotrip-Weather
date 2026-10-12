# WeatherNext Map Visual V15 - four forecast-layer visual reset

**2026-10-12 · isolated frontend visual lab · HOLD production · not approved for Engine.**

User assessment at V14: satellite **Clouds** look reasonably good, while **Rain, Wind, Waves, Temperature** are not visually adequate. V15 preserves the observed Himawari-9 VIS B02 + IR B13 six-frame cloud overlay and its map basemap, and changes the other four visualizations.

## What V15 renders

- **Rain (ECMWF archived 0.5° model):** stronger but semi-transparent rain accumulation gradient, *derived* isolines at 1/2/4/6 mm per archival sample, and three geo-anchored numeric values. The model accumulation **window is NOT verified**; display is **mm / kỳ mẫu***, not hourly intensity or radar. No invented rainfall hotspots, spot noise or cloud/radar conflation.
- **Wind (ECMWF archived 0.5°):** speed field (km/h), fixed vector arrows and animated particles using actual model **U/V** and map-projected coordinates. Fixed labels show numeric model speed. No random direction.
- **Waves (Copernicus Marine archival forecast, nominal 0.0833°):** **new, independently sourced** spatial snapshot extracted **read-only** from repo `data/weather-runtime/marine.json`, provenance `cmems_mod_glo_wav_anfc_0.083deg_PT3H-i`, `sampled_time=2026-10-11T06:00:00Z` (13:00 in Vietnam). A 154-cell regional subset is stored in `fixtures/marine_wave_20261011T0600Z.json`. Significant wave height Hs appears on real **OSM water polygons only**; OSM land pixels remain fully uncovered. Marine labels are sampled model heights, and map click includes archived mean wave period. **Only one actual snapshot is available**; the timeline is explicitly **1/1 and disabled for Waves**, not forged into the ECMWF seven-frame times. Direction convention has not been independently verified, so **wave propagation animation is not fabricated**.
- **Temperature (ECMWF archived 0.5°):** visual temperature gradient, contour lines (26/28/30/32°C) and georeferenced numeric temperature labels. Land imagery remains visible underneath.

## Ground truth and limits

- Mây: JMA/NOAA Himawari-9 AHI VIS B02 and IR B13 archival observations from 2026-10-11; those remain unchanged from V14. Reflectance whites may also indicate ground/haze; VIS/IR is not precipitation radar.
- Basemap: MapLibre GL + OpenFreeMap/OSM vector tiles and historical Sentinel-2 cloudless geographic underlay by EOX (Copernicus Sentinel 2016/17). Geo coordinates/shoreline come from OSM. Maps require network access; no guessed island silhouette is used as a trustworthy geography fallback.
- Rain/wind/temperature are independent forecast model surfaces in V8 archive, at 0.5° native grid. Interpolated presentation **does not create meteorological detail**. Model values, timestamps, uncertainty and labels must be validated by Engine before any live integration.
- Marine forecast rows are sample-source data (not live observations); no source code or runtime file was written back to Weather Runtime.
- VRain station values in the lab remain stale archival examples and are labeled as such.

## Captured QA

- Isolated Windows PHUQUOCLUX Chromium at **390×844** and **1440×900**. Tested five layers, zoom/pan, user-selected layer/timeline, numeric model sampling and vectors. No JS exceptions or captured network failures in the baseline online tests.
- OSM water masking: at a 390×844 sample test **land alpha=0**, sea alpha≈197 for Waves.
- No-Copernicus-filename failure test: browser stays loaded, `marineReady=false`, `value=null`, source explicitly reads "Chưa tải được snapshot Copernicus", wave timeline remains disabled, **no JS exception**.
- Known blockers: **physical iPhone Safari not tested**; no comprehensive low-bandwidth/device-FPS benchmark; Copernicus wave direction convention not verified; no merged data contracts; final aesthetic acceptance still pending.
- Visual evidence in `screenshots/`: four separate real Chrome mobile captures and a combined 4-up comparison. These are screenshots from running HTML, **not AI concept illustrations**.

## Run isolated

From the `visual-lab/weathernext-map-v15` folder:

```sh
python -m http.server 8795 --bind 127.0.0.1
```

Open `http://127.0.0.1:8795/` with Internet for vector map and historic geographic imagery. Both `ahi/` and `fixtures/` are mandatory. HTTPS rawgit.hack may require a click-through "Open the page", and is a third-party convenience preview, not a controlled production host.

**No Core V1.2, CMS, auth, DB, Cloudflare production, API, scheduler, ingest, Engine, main branch or WeatherNext production changes.** Explicit user visual approval and iPhone Safari QA are prerequisites to Engine handoff.

Attribution: Himawari-9 satellite imagery © JMA, NOAA Open Data redistribution (modified color/geoprojection). Wave data © Copernicus Marine Service, processed archived wave forecast. Map © OpenStreetMap contributors/OpenFreeMap; historical Sentinel-2 cloudless 2016/17 © EOX IT Services GmbH (modified Copernicus Sentinel data), CC BY 4.0.
