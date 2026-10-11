# WeatherNext Map Visual V13 - AHI B13 actual IR imagery

Date: 2026-10-12 (Asia/Ho_Chi_Minh). Status: FRONTEND LAB, HOLD PRODUCTION, NOT USER-APPROVED.

## Important distinction

- MapLibre GL + OpenFreeMap vector basemap: actual geographic coordinates; no invented coastline.
- EOX Sentinel-2 cloudless 2016 underlying land imagery: HISTORICAL BASMAP ONLY, not current weather. Attribution: EOxCloudless https://cloudless.eox.at by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016 & 2017), CC BY 4.0.
- Himawari-9 AHI original Band B13, nominal ~10.4 micrometer infrared window, authentic 2026-10-11 observations from NOAA public S3 bucket `noaa-himawari9`: brightness temperature (not cloud top median, not radar, not rain measurement). JMA manages Himawari; NOAA freely redistributes. Processed data are MODIFIED / reprojection and palette, no NOAA/JMA endorsement.
- Source: `AHI-L1b-FLDK/2026/10/11/{HHMM}/HS_H09_20261011_{HHMM}_B13_FLDK_R20_S0410.DAT.bz2` and `S0510`.
- 6 observations: 03:30, 05:30, 05:40, 06:00, 06:10, 06:30 UTC on 2026-10-11. Irregular gaps faithfully shown; video repeats discrete observed frames, no invented motion between frames.
- Each image PNG is a fixed WGS84 rectangle W 103.55 E 104.45 S 9.76 N 10.66, 640x640 samples; original AHI infrared native nadir pixel ~2km, *not* true 640-pixel physical resolution, interpolation doesn't create details.
- Legacy archived Himawari cloud-top 0.075 degree grid is only fallback when raw B13 imagery fails.
- Rain: archived ECMWF forecast ~0.5 degree; coarse fields, no inferred local radar echoes; accumulation window in fixture is NOT verified so labeled "mm / kỳ mẫu".
- Wind: archived model U/V, vector-particle simulation in geographic coords, not live observed wind.
- VRain stations: archived sample only, stale labels.
- This is a visual experiment; no API, Core, CMS, scheduler, production, Cloudflare, and no active weather changes.

## Testing evidence

- Windows PHUQUOCLUX isolated headless Chromium connected to local HTTP server and CDN: full vector, EOX basemap and AHI source images rendered; layer switching and six discrete frames were exercised; no JS exceptions in captured test.
- Real browser screenshots mobile 390 x 844 and desktop 1440 x 900 in screenshots/.
- Safari on an actual iPhone: **NOT YET TESTED**. No guarantee of final user acceptance.
- Vercel preview was blocked by 403 credentials in prior V11 attempts. GitHub **source browsing isn't an interactive preview**.
- Environment and sample archive remain strictly separate from core and weather production.

## Run locally

Serve this directory with `python -m http.server 8765 --bind 127.0.0.1`; open `http://127.0.0.1:8765/` in browser with Internet for vector and Sentinel-2 tiles. Downloaded AHI six PNGs are local under ahi/. Browser double-click may restrict image source fetch. No real-time update.
