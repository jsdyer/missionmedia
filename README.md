# Mission Media

Search NASA photographs, video and audio, inspect original assets and keep private research boards with source credits.

**Use it:** https://coolcode.ca/missionmedia/

<!-- coolcode:guide -->
Search any subject in NASA’s media library, filter by type and year, then inspect original assets and captions. Save records into private local boards with notes; export a backup or credits for the selected board. Dates reflect source records, and credits do not grant reuse rights. No API key is needed.
<!-- /coolcode:guide -->

## Use the research desk

1. Enter any mission, person, place or subject. The buttons are starting points, not a fixed collection. Filter images, video or audio and optionally enter a four-digit source-year range.
2. Select **Inspect & collect**. The inspector displays NASA's description, creator or center, record ID, source date and metadata check time. Asset files open directly on NASA's servers. Files marked `~orig` by NASA are labelled original; displayed pixel dimensions and sizes are included only when NASA provides them in search metadata. Other assets may still have unknown dimensions. No binary files are downloaded in the background.
3. For video/audio, choose **Load preview** to request a playable file. Captions and the complete source metadata JSON are linked when NASA supplies them. A 404 caption response means no caption file is listed; other caption failures are shown separately.
4. Type a board name and optional notes and explicitly choose **Save to board**. You can move a saved record by changing its board name. The same NASA ID appears once in the library; saving it again updates its board and notes.
5. In **My boards**, filter the board and search saved text. Export the visible credits as text or CSV, or back up the entire library as JSON. Imports add unknown IDs and retain existing notes and placements. The limit is 300 saved media records. Imported records can be unrelated to every default query.

Search metadata dates can describe NASA's cataloguing choices and are not a guarantee of the moment depicted. The separate metadata-check timestamp is when this browser received a search response. Saved records preserve their original check time; reopening their assets does not pretend that their description was freshly fetched. Search again and save the result to refresh its summary.

## Sources and reuse

- [NASA Image and Video Library](https://images.nasa.gov/)
- [Official API documentation](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf): search, asset manifest, metadata and caption endpoints at `https://images-api.nasa.gov`.
- [NASA images and media usage guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/)

This is an on-demand reference and media-research application. It is distinct from sky observation/astronomy data tools and Internet Archive media browsing. It does not aggregate copyrighted third-party streaming catalogues or imply that every item is unrestricted. NASA records can include third-party content, identifiable people and insignia; review the original record and NASA's guidelines before reuse. Missing creator fields are explicitly retained as blank in CSV; human-readable credits fall back to NASA and its recorded center rather than inventing a photographer.

The public NASA API supports browser requests and requires **no API key**. No secret, backend or paid service is needed. NASA can return rate limits, maintenance failures or withdrawn assets; the application reports request errors and retains saved local boards. Search exposes at most 100 API pages; use more specific terms and filters when there are more results. Files are opened as source links, not promised to remain available forever.

## Privacy and storage

Search phrases, media type, year filters and selected NASA IDs are sent directly to NASA. Preview images and explicitly loaded audio/video contact NASA's asset host. Queries are placed in the page URL for bookmarking and can appear in browser history. Board names, research notes and imported backup contents stay in this browser under `coolcode:missionmedia:boards`. Nothing is saved until you choose Save or Import. Clear browser data to erase saved boards, or remove individual records in the application. NASA images are not copied into local storage. Backups contain record summaries and notes, not media binaries.

No accounts, cloud sync, external font service or API credentials are used. The standard CoolCode aggregate visitor counter receives the tool ID, not searches, board names, notes or imports. External strings are rendered as text, asset links are restricted to NASA media hosts, imports are validated and bounded, and CSV cells with formula prefixes are escaped.

## Expand or customize

Edit `web/config.json`: add `{ "label": "Your starting point", "query": "your subject" }` entries to `presets`, change `defaultBoard`, or set `pageSize` from 1 to 100. Arbitrary valid queries work without edits. Board names are visitor input and derive from saved data, not this configuration. Change `web/` for the interface and keep NASA response normalization and export logic in `web/model.mjs`.

```sh
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

Then commit the source to `main`. The Pages workflow tests, builds and runs Playwright against the actual built application at a project subpath before deploying. Browser tests use controlled NASA responses for repeatable interactions; these fixtures are never published. Tests cover arbitrary searches, file selection, captions, local board persistence, import/export, source errors and mobile layout. CI uses installed Google Chrome on `ubuntu-24.04`; for local browser checks install the packages from `tests/browser-requirements.txt` and provide `CHROMIUM_PATH` if needed.

## Operations and integration

There is **no scheduled collector** and no data freshness download. NASA requests happen when visitors search or inspect results. The Pages workflow retains `workflow_dispatch`, but no cron guard or independent watchdog refresh target is needed. Record this explicit absence of schedules in the hub's operations inventory.

After CI and Pages verification, integrate `tool.json` and the guide excerpt into the CoolCode catalogue, repository audit, sitemap and existing Worker registry using the hub's [tool lifecycle](https://github.com/jsdyer/jsdyer.github.io/blob/main/docs/tool-lifecycle.md). No change to watchdog server code is needed for this on-demand app. Do not publish credentials in `web/`, repository variables or source files; this app does not require any.
