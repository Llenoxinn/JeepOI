# JeepOI — "Jeep, oy!"

> The Cebu jeepney map you can trust: every route verified and dated, the fastest way to get there first, every tourist spot tied to the jeep that reaches it, and the full story of which jeeps are gone and what modernization will change.

**Team:** 2 people (CS sophomores)
**Type:** side project / passion project. Not a thesis, not a startup.
**Timeline:** 14 weeks, part-time (about 8–10 hrs/week each, plus weekend route rides)
**Scope for v1:** Cebu City core plus the main tourist lines into Mandaue and Mactan
**Status of this plan:** v3, 26 Oct 2026. v2 added the competitor teardown and three research passes (full findings in `reports/Cebu jeepney apps and tourism.md`); v3 adds a review of Commute Bacolod as a design reference (Section 3a), honest answers to outside criticism (Section 3b), a Google Maps baseline test, and a performance budget.

**What success means for us:**
1. We learn a lot: graphs and shortest paths, GIS data, map rendering, motion design, field research, shipping as a team.
2. We ship something we're proud to show: polished, fast, and honest about what it knows.
3. Some Cebuanos and visitors actually find it useful, even if most people keep using Google Maps.

JeepOI does not need to beat Google Maps to be worth building. It needs to be good, honest, and ours.

---

## 1. One-line pitch and positioning

**Other Cebu jeep apps tell you where a jeep goes. JeepOI tells you where it goes *today*, how we know, how fast it gets you there, what you can see along the way, and what is about to change.**

Positioning in one sentence: **JeepOI sells trust and time, wrapped in the best-looking map in Cebu.**

---

## 2. The landscape (what already exists)

Cebu already has several route finders. JeepOI should not pretend otherwise.

| Product | What it does well | Where it falls short |
|---|---|---|
| **Route7 / Sugbu Buddy** (route7.vercel.app) | 94 routes incl. Mandaue and Mactan; A-to-B planner with up to 2 transfers; fares with student discount; 55 "Spots"; "Ask Nana" chat helper; Bisaya phrases; hotlines; dark mode | Its own About page says routes, stops and fares may be outdated; access distances are straight-line; spot pins are approximate; geometry is derived from cebujeepneys.weebly with republishing rights unverified; no history, LPTRP or BRT content; standard Leaflet look. See the team teardown in Section 3. |
| **JTransit** (jtransit.app) | Door-to-door trips with walk/wait/ride times and fare; 60+ routes; crowdsourced route proposals with voting | No tourism layer, no history, no modernization context, no visible data dates |
| **Cebu Jeepney Finder** (cebujeepney.vercel.app) | 55 routes, 1,156 stops, transfers | Anonymous, no sources, no dates, Cebu City only |
| **JeepMe**, **RUTA**, others | Open-source / "AI" planners | JeepMe calls its own data approximate; RUTA was waitlist-only with a planned ₱99–169/month paywall |
| **cebujeepneys.weebly.com** | Broad code coverage, one Google My Map per code, MyBus/V-hire/ferry pages | No dates, fares or search; appears unmaintained |
| **suroy.ph 2026 guide** | The only source with the Sept 2026 fares; honest about unconfirmed codes | Text only, about 17 codes, no map |
| **Google Maps** | Code-level jeep directions since about 2017 | Opaque source and freshness |
| **Sakay.ph** | Mature planner | Built for Metro Manila; Cebu coverage unclear |
| **OpenStreetMap** | Open data: about 66 Metro Cebu jeep routes plus MyBus and CBRT | "In progress", old tagging, stops missing |
| **Government** | — | LTFRB told an FOI requester it has no Cebu route map; the Cebu BRT has no official app or map |

**The shared blind spot:** every tool treats the network as frozen. None shows when a route was last verified, who verified it, which routes used to run, or what the LPTRP and BRT will change. That is the gap JeepOI owns.

---

## 3. Competitor teardown: Route7 (team observation, 26 Oct 2026)

Our own hands-on notes, and what JeepOI does about each one:

| # | What we observed on Route7 | JeepOI's answer |
|---|---|---|
| 1 | The default map view is a whole-region overview with a very general zoom, even though coverage is only Cebu and nearby cities. It should start at a location marker, like a terminal. | **Smart default view:** start at the user's location if they allow it; otherwise zoom to the downtown/Colon cluster with terminals visible. Never open on the whole province. |
| 2 | No location markers for landmarks. | **Named markers** for landmarks, terminals and stops, with zoom-based decluttering so the map stays clean. |
| 3 | Routes are accurate, but there are no jeep suggestions tied to landmarks on the map. | **Tap any landmark or stop:** see every jeep that passes it, plus "ride from here" shortcuts. |
| 4 | The route/jeep suggestion panel is tiny (about an inch tall) and you have to swipe; it can't be expanded. | **Bottom sheet with three snap points** (peek, half, full) that drags and expands, like Google Maps. |
| 5 | Some listed routes we have never seen on the road: 04B, 03Q, 04M, 04A. | **"Last seen" sightings:** every route shows when someone last saw it running, and anyone can tap "I saw this jeep today." Routes with no recent sighting are flagged. (Note: 03Q and 04B do appear in the Oct 2026 suroy.ph guide, so they may exist but run rarely. This is exactly what field checks and sightings will settle.) |
| 6 | Missing routes. | Grow coverage steadily, but every route we add is ridden or marked "unverified." Quality over count. |
| 7 | Coverage is localized to Cebu City; only some routes in other cities. | v1 covers Cebu City plus the key Mandaue/Mactan tourist lines (23, MI-01A, MI-02B); expand city by city after launch. |
| 8 | Suggestion: add bus routes. | **Bus layer:** Cebu BRT and MyBus in v1, Ceres/Beep and V-hire later. |
| 9 | Should include terminals and stops. | **Terminals and named stops are first-class map objects** (SM, Ayala, Colon, Carbon, IT Park, JY Square, Parkmall, North/South Bus Terminals, Marina Mall). |
| 10 | The Spots feature is fine as an extra, but there are too few spots. | **Code-first tourism** (Section 5.3): fewer but verified spots, each tied to exact jeep codes, alighting points and honest last-mile costs. |
| 11 | Cancelling a pinned location is hard. Pinning and erasing a pin should be easy. | **One-tap pin, one-tap clear:** long-press or tap "Pin" to drop; every pin shows as a chip with an "x"; dragging the pin moves it. |
| 12 | The AI helper is not accurate: it suggested a Balamban–Ayala V-hire that doesn't pass the area, when 04L exists. | **Jepoy only answers from JeepOI's own route data and planner,** never from general AI knowledge (Section 5.6). |
| 13 | Overall it's confusing because there are no location markers or stop names at landmarks. | Named stops at landmarks, and every trip result says exactly where to board and where to get off ("Para sa Fuente"). |

**What we should *not* copy:** Route7's data or geometry. Its own About page says the rights are unverified. JeepOI builds its own verified data (Section 7).

---

## 3a. Reference product: Commute Bacolod (team review, 26 Oct 2026)

Not a competitor (it's Bacolod), but the most polished Philippine jeepney app we've seen, and a good model for how JeepOI should feel. Reviewed at commutebacolod.com and app.commutebacolod.com (v1.3.0).

**What it does well, and what JeepOI borrows:**

| Commute Bacolod | Borrow for JeepOI |
|---|---|
| Separate marketing site (www) and app (app subdomain) | Same idea, simpler: landing page at `/`, the map app at `/app`, one codebase |
| Hero has "Where from? / Where to?" fields right on the landing page that jump into the app | Put the from/to fields in our hero too, so the landing page is also the fastest way to start a trip |
| Editorial design: huge clean type, monochrome, lots of white space, an illustrated road graphic | Confirms our direction (big type, restraint); our twist is the signboard identity and the night map |
| "How it works": a phone mockup stays pinned while four steps scroll past and light up | Use this pattern for our "How JeepOI works" section, pinned with GSAP |
| Branded loading screen ("Preparing your map") | Jepoy loading screen with a short Bisaya line |
| Results: a **Fastest / Recommended** card first, then **"Try another: different jeepney"** alternatives | Matches our Fastest-first tabs; add a "Try another jeep" option inside each tab |
| Summary chips on each result: fare, km, number of rides | Same chips, plus time and the trust badge |
| Step-by-step directions; **tap a step to focus it on the map** | Add to our result cards: every step (walk, board, ride, get off) is tappable and flies the map there |
| **"Ride a modern jeep: same route, higher fare (+₱5)"** toggle inside the ride step | Add a traditional/modern toggle per ride leg that updates the fare live |
| Walk legs labeled **"Walk or take a tricycle"** | Label short legs "Walk or tricycle," and long uphill legs "Habal-habal or Grab" with a price range |
| "Avoid jeepney routes" filter | Add "Avoid" options: avoid a specific code, avoid transfers, avoid long walks |
| Route directory with a color legend | Our Route Explorer already covers this; add a simple legend panel |
| Community updates feed: road closures for the MassKara festival, new features | **Route notices:** dated alerts for Sinulog closures, roadworks and BRT diversions, attached to the routes they affect, so they also feed the trust ledger |
| Real Reddit testimonials on the landing page | After launch, a testimonials section with real quotes (with permission) |
| Watch-demo video, FAQ, help center, privacy/terms/cookie pages, contact email, Buy Me a Coffee, visible version number | Ship a 30-second demo video at launch, an FAQ, privacy and terms pages, a contact email, an optional tip link to cover hosting, and a version number with a short changelog |

**What to avoid:**
- **Vanity stats.** Its stats band counts up to "50K+ users, 15+ routes, 100% local data, 5/5 rating," and before the animation runs (or for screen readers) the raw text reads "4K+ users, 5+ routes, 1% local data, 1/5 rating." Claims like "5/5" and "100%" also can't be checked. JeepOI shows only numbers we can prove (routes verified, km ridden, last update date), and animated counters must render the real final value in the HTML.
- **Overpromising "live updates."** Its landing page says "Get live updates," but there's no live vehicle data behind it. We only claim what we actually do.
- **Repeated content for screen readers.** The testimonial marquee repeats items in the page text; decorative duplicates should be hidden from assistive tech.

---

## 3b. Hard questions, honest answers

A public comment on Route7 raised questions that apply to any Cebu jeep app, including ours. Better to answer them now than after launch.

**"The solution already exists and it's free on Google Maps. Why build another one?"**
- Partly fair. Google Maps does give Cebu jeep directions by code.
- But "it's up to date" is an assumption. Nobody has published where Google's Cebu jeep data comes from or how fresh it is. So we **measure instead of claim**: the same 20 test trips go through Google Maps, Route7 and JeepOI (Section 14, H5), and we publish the results either way.
- If Google wins on trip planning, that's fine. The planner is a doorway, not our headline. What Google doesn't do: show how fresh each route is, show routes that disappeared, explain what the LPTRP changes, or plan a day around one jeep code.
- And this is a passion project. We're building it to learn and to make something good for Cebu, not to replace Google.

**"Why would a user chat with an AI just to get an answer?"**
- Agreed. Typing a start and an end is faster than a conversation.
- That's why the core of JeepOI has **no AI at all**. Jepoy is an optional v2 extra for vague Bisaya questions ("asa ko musakay padulong Carbon?").
- If hallway tests don't show people want it, we cut Jepoy and lose nothing (Section 5.6).

**"How will you keep fares up to date? Do you need an LTFRB partnership?"**
- No partnership needed. Jeep fares are a public formula (base fare for the first 4 km plus a rate per km), changed by LTFRB a few times a year and announced publicly.
- We store the formula as one dated rule in one file (Section 7.5), so an update is a few numbers.
- The real cost is attention, so there's a named owner: a monthly "fare watch" (Section 7.5). The app always shows which fare rule it used and its date.

**"What search algorithm? Storing everything as files is inefficient. Compute on search and cache."**
- We do compute on every search: Dijkstra/A* runs per query (Section 8).
- The file is only the **graph** (stops and connections), precomputed once. That's how routing engines work: build the network ahead of time, search it per request.
- The search runs **in the browser** because Cebu's network is small (around 10,000 stops). Dijkstra with a priority queue is O((V + E) log V), which on this graph takes milliseconds on a phone. Running it in the browser means no server bills, it works on weak signal, and the browser and CDN already cache the graph file.
- Server-side routing with caching makes sense for country-sized networks or live data. If JeepOI ever outgrows the browser, Section 8.7 says when and how we move.
- We back this with a measured benchmark, not just an argument (Section 8.7).

**"What makes you different from competitors using AI LLMs for routes? LLMs are expensive."**
- JeepOI's routing uses no LLM, so it costs nothing per search.
- If Jepoy ships, it uses one small model call to understand the question, then calls our own planner for the actual route. It has a monthly spending cap and is the first thing we cut if costs grow.

**"This is not innovative."**
- For trip planning in Cebu, that's fair. Several tools already do it.
- What's new in JeepOI isn't the planner. It's a field-verified, dated, open route dataset (the way Digital Matatus mapped Nairobi), a published accuracy comparison of existing tools, and the history and modernization layer nobody else has.
- And for a passion project, "innovative" isn't the bar. "Good, honest, and useful to someone" is.

---

## 4. Goals

1. **Trustworthy.** Every route and spot shows its status, last-verified date, method and sources.
2. **Fastest first.** The planner ranks by real door-to-door travel time, using speeds measured on our own rides.
3. **Visual and interactive.** The best-looking, most explorable transit map in Cebu.
4. **Useful to tourists.** Start from a jeep code and see everything it can take you to, including where the jeep can't go and what the last mile costs.
5. **Tells the story of change.** Ghost routes, the LPTRP and the BRT, explained for normal commuters.
6. **Teaches us something real.** Each feature is picked partly for what we'll learn building it:

| Feature | What we learn |
|---|---|
| Fastest-first planner | Graph modeling, Dijkstra/A*, k-shortest paths, benchmarking |
| Data pipeline | GPS cleaning, map matching, GeoJSON, OpenStreetMap |
| Map and motion | WebGL maps, data-driven styling, GSAP, animation performance |
| Field rides | Real-world data collection, research methods |
| Jepoy (if built) | LLM function calling, prompt testing, cost control |

**Not goals:** live vehicle tracking, booking, being an official LTFRB source, beating Route7 on raw route count, or replacing Google Maps.

---

## 5. Features

Features are tiered so a two-person team ships something great even if time runs short.

- **Tier 1 — Core (must ship):** 5.1, 5.2, 5.3, 5.4
- **Tier 2 — Signature (should ship):** 5.5, 5.7 (bus layer), 5.7b (route notices)
- **Tier 3 — Later (v2, after launch):** 5.6 Jepoy, plus the stretch list in Section 13

### 5.1 Fastest-first trip planner — "Asa ka padulong?"
- **Start and end:** tap the map, long-press to pin, search a place, choose from a landmark list, or "Use my location." Every pin is a chip with an "x" to clear it. A swap button flips start and end.
- **Results in three tabs:**
  - **Fastest** (default, first)
  - **Cheapest**
  - **Fewest transfers**
- **Each result card shows:**
  - Summary chips: total time, fare, distance, number of rides
  - Time broken into walk, wait, ride and transfer ("32 min: walk 6, wait 4, ride 20, transfer 2")
  - Jeep codes rendered as signboard placards
  - Where to board and where to get off, by stop name ("Board at Gaisano Fuente, para sa Colon")
  - Fare, regular and discounted (student/senior/PWD 20%)
  - Trust badge for each route used
  - "Try another jeep" for alternatives with a different code
- **Step-by-step directions:** every step (walk, board, ride, get off) is tappable and flies the map to it. Ride steps have a **traditional/modern toggle** that updates the fare live. Short walking legs say "Walk or tricycle"; long uphill legs say "Habal-habal or Grab" with a price range.
- **Avoid options:** avoid a specific code, avoid transfers, avoid long walks.
- **On the map:** walking legs dotted, jeep legs in route color, transfer and alighting markers with names. Tapping "Ride along" animates the camera along the trip.
- **Bottom sheet:** peek, half and full snap points, so results are never stuck in a tiny strip.
- How "fastest" works is in Section 8.

### 5.2 Route Explorer with a trust ledger — "Unsa'y mga jeep?"
- All active routes, color-coded by code family, with parallel offset lines on shared corridors (Colon, Osmeña Blvd) so overlapping routes stay readable.
- **Tap a route:** highlight it, dim the others, and open a panel with:
  - Code, endpoints, both directions, stops and landmarks passed
  - Fare range (traditional/modern, regular/discounted)
  - **Trust ledger:** status (verified, reported, disputed, unconfirmed, discontinued, planned), last verified date, method (ridden with GPS, OSM cross-check, dated guide), source links
  - **Last seen:** most recent sighting, plus an "I saw this jeep today" button
  - "This changed" report button
- **Tap a stop, terminal or landmark:** see every jeep that passes there.
- **Tap any street:** "Jeeps that pass here."
- Search by code ("13C"), stop or landmark. Filters: code family, area, traditional/modern, verified only.
- **Line styles carry meaning:** verified = solid, unconfirmed = thin, disputed = hatched, planned = outlined, ghost = faded dashed.

### 5.3 Code-first tourism — "Laag gamit jeep"
Route7 starts from a spot. **JeepOI starts from the jeep.**

- **Tour Lines:** curated route-as-tour itineraries, each a single jeep ride:
  - **17B Heritage Line:** IT Park → Lahug → Capitol → Fuente → Colon → Basilica / Magellan's Cross district → Carbon
  - **01K Museum Line:** Urgello → Colon → Parian (Heritage Monument, Casa Gorordo, Yap-San Diego) → Museo Sugbo → SM
  - **04L Gateway Line:** JY Square → Ayala → SM, plus the honest last-mile guide to the uphill spots
  - **Mactan Line (23 / MI-01A):** Parkmall/Marina Mall → Mactan Shrine and the Sutukil seafood row → Punta Engaño resort strip
- **Ride-along view:** the camera follows the jeep while spots slide in, each with three facts: exactly where to get off, the walk, and what to know (dress code, hours, entrance fee).
- **"Where can this jeep take me?":** pick any code and see every spot within a short walk of its route.
- **Honest last-mile connectors:** spots no jeep reaches are drawn as dashed connectors with prices, never as fake jeep stops. Example: "JY Square → Temple of Leah: habal-habal ₱100–150 or Grab ₱200–400; arrange your ride back."
- **"No jeep goes here" is a feature:** Temple of Leah, Sirao Flower Garden, Tops Lookout and the Taoist Temple are clearly marked as last-mile-only.
- **Downtown heritage is one walkable cluster,** since no current source gives codes for individual monuments.
- Spot categories: heritage, church, museum, food, market, mall, nature/viewpoint, beach, nightlife.

### 5.4 Smart map basics (from the teardown)
- Smart default view (user location, or downtown with terminals visible).
- Named markers for terminals, stops and landmarks, decluttered by zoom level.
- One-tap pin and clear.
- Works great on phones first: big tap targets, bottom sheet, thumb-reachable controls.
- Bisaya/English toggle for all UI labels.

### 5.5 Ghost Routes and the modernization story — "Asa na sila?"
- **Era slider:** drag through 2011 → 2020 (pandemic) → 2026 → 2028 (LPTRP plan) and watch routes appear, vanish and merge. Ghost routes are faded dashed lines, each with a story card: last seen, why it changed if known, what replaced it, sources.
- **Before/after swipe:** today's network vs the LPTRP's 40 routes.
- **"Is my jeep affected?":** type a code and see its planned fate, tagged "planned / unconfirmed" until LTFRB publishes official mappings. Never imply official mappings that don't exist.
- **Scrollytelling page (5 chapters), pinned map with scroll-driven changes:**
  1. **The code system:** how Cebu codes work, with an interactive signboard decoder.
  2. **The spaghetti:** all routes at once, overlap hotspots as a heatmap.
  3. **The vanishing:** ghost routes over time.
  4. **What's changing:** LPTRP 2024–2028 (40 routes, 1,013 units: 663 on rationalized routes, 350 on new ones), new loops and radials like Sirao–IT Park, the BRT corridor and shared BRT lanes, a live counter that ticks as you scroll, and the human side (drivers expected to be displaced, operators who never received the plan).
  5. **What this means for you:** jump into the planner or "Is my jeep affected?"

### 5.6 Jepoy — the JeepOI mascot and chat helper (v2, optional)
- **Status:** optional. Jepoy is the mascot everywhere (empty states, loading, tips) from v1, but the **chat** only gets built if hallway tests show people want to ask questions instead of tapping a map. If not, we cut the chat and keep the mascot.
- **Why it's not core:** typing a start and an end is faster than chatting. Jepoy only earns its place for vague or Bisaya questions the search box can't parse.
- **Who:** Jepoy is a friendly little jeep character who speaks Bisaya-English and helps you get around ("Asa ka padulong, bai?").
- **What it does:** turns questions like "Unsaon pag-adto sa Museo Sugbo gikan sa IT Park?" into a planner query and answers with the result, plus a "Show on map" button.
- **The rule that matters:** Jepoy never invents routes. It calls JeepOI's own trip planner and route data as tools and only repeats what they return. This is the fix for the Route7 mistake we caught (suggesting a Balamban–Ayala V-hire when 04L exists).
- **Answer contract** (every route answer has these parts, in this order):
  1. The jeep code(s), from the planner
  2. Where to board and where to get off, by stop name
  3. Time estimate and fare
  4. Trust badge for each route used
  5. "Show on map" action
- **When the planner finds nothing:** Jepoy says so plainly and offers the nearest jeep option or a last-mile alternative. It never guesses.
- **Testing before launch** (borrowed from how prompt and skill writers test instructions):
  - Build a test set of 20 questions, including traps: the Balamban V-hire case, "How do I get to Tops by jeep?" (correct answer: no jeep goes there), a code that doesn't exist, and a misspelled landmark.
  - Run each question 5 times with the plain model (control) and 5 times with Jepoy's tool setup.
  - Read every answer by hand. Ship only when Jepoy passes every trap in every run.
- **Tech:** any LLM API with function calling, called from a serverless function so the API key never reaches the browser. No chat history stored by default.
- **Cost control:**
  - Use a small, cheap model; it only has to understand the question, because the route comes from our planner.
  - Cache answers to common questions ("IT Park to Colon") so repeats cost nothing.
  - Rate-limit per user and set a hard monthly spending cap. When the cap is hit, Jepoy politely hands over to the normal planner.

### 5.7 Bus layer
- Cebu BRT corridor and stations, and MyBus routes, as a toggleable layer in v1.
- Combined jeep + BRT trips in the planner once the bus data is verified.
- Ceres, Beep and V-hire in v2.

### 5.7b Route notices
- Dated alerts for Sinulog closures, roadworks, BRT diversions and fare changes, attached to the routes and stops they affect.
- Affected routes show a notice badge until the notice expires, and the planner warns when a trip uses an affected route.
- Each notice has a source (city announcement, news, our own sighting) and an end date, so the trust ledger stays honest.
- The same notices appear in a "Route news" section on the landing page and get cross-posted to our Facebook page.

### 5.8 Report, sighting and correction loop
- On every route and spot: "This changed," "I saw this jeep today," and optional photo upload.
- v1: Google Form. v2: Supabase table, with reports showing on the route as "reported" until checked.

---

## 6. Design direction

The goal is the best-looking transit map in Cebu, with an identity that feels Cebuano rather than generic.

### 6.1 Visual identity
- **Signboard aesthetic:** route codes render as windshield placards everywhere (map labels, result cards, the marquee). This is the brand.
- **Palette:** deep night base for the map UI, signboard yellow as the accent, chrome silver for secondary UI, and a color-blind-safe set of route-family colors (start from the Okabe-Ito palette). Because there are more code families than safe colors, line patterns and placard labels also carry meaning, so color is never the only signal.
- **Typography:** Cabinet Grotesk for headlines, Geist for UI text, Geist Mono for route codes and fares. Not Inter.
- **Light and dark themes,** both designed, not one inverted from the other.

### 6.2 Landing page structure
1. **Navigation:** floating glass pill nav (Plan, Explore, Tour Lines, Story).
2. **Attention (hero):** cinematic, centered. Behind it, the live network map with animated jeeps, under a dark radial wash. The headline stays on 2 lines max in a wide container (for example, "Every jeep in Cebu. Where it really goes, today."). Below it, **"Asa ka gikan? / Asa ka padulong?" (from/to) fields** that jump straight into the planner, then exactly two buttons: "Plan a trip" and "Ride a Tour Line." No stats or badges in the hero.
3. **How it works:** a phone mockup pinned on one side while four steps scroll past and light up (search, see the fastest jeep, follow the steps, get off at the right stop).
4. **Interest:** a gapless bento grid of 4 cards: Trust ledger, Time machine, Tour Lines, Fastest first. Use `grid-auto-flow: dense` and check that spans interlock with no empty cells.
5. **Desire:** the pinned scroll story. The map stays fixed on one side while chapters scroll past.
6. **Route news:** the latest route notices (Section 5.7b).
7. **Proof, honestly:** only numbers we can back up, like "18 routes verified," "212 km ridden," "last updated 3 days ago." No vanity counts, no made-up ratings. After launch, real testimonials (with permission).
8. **Action:** a big "Plan your first trip" call to action and a footer with sources, methodology, OSM attribution, FAQ, privacy, terms, contact, an optional tip link for hosting costs, and the version number.

**App shell:** the map app lives at `/app`, with a Jepoy loading screen and a visible version number linked to a short changelog.

### 6.3 Motion
- **GSAP ScrollTrigger** for the story: pinned map, scrubbed text reveals, and Tour Line cards that stack as you scroll.
- **An infinite marquee of route-code placards** across the landing page.
- **Map motion:** ride-along camera, animated jeeps with fading trails (deck.gl TripsLayer), smooth fly-to between chapters.
- **Reduced motion is mandatory:** when the user's device asks for reduced motion, every animation collapses to its static end state. No pinning, scrubbing or auto-scrolling marquee.
- Hover and press feedback on every tappable card.

### 6.4 Accessibility
- Color-blind-safe routes, keyboard navigation, focus states, text alternatives for map content (every route and trip is also readable as a list), and contrast checked on both themes.

---

## 7. Data plan

### 7.1 Sources, in order of trust

| Source | What it gives | Trust | Use for |
|---|---|---|---|
| **Our GPS rides** | Fresh route lines both directions, real speeds by time of day, stop names | Highest | Ground truth for core and tour routes; travel-time model |
| **LPTRP documents** (Cebu City, LTFRB-7) | Official new routes, lengths, units | High for "planned" | Modernization layer |
| **OpenStreetMap** (`network=PH:PUJ:Metro Cebu`, plus MyBus and CBRT) | Draft geometry, about 66 routes | Medium | Starting skeleton, bus layer |
| **OSM edit history** | Past versions of route relations | Medium | Ghost routes |
| **Dated guides and news** (CDN 2020 and 2023, Sugbo.ph 2024, r/Cebu wiki 2025, suroy.ph Oct 2026) | Code lists by date, fares, policy events | Medium | Ghost-route diffing, timeline, cross-checks |
| **2013 DOTC GTFS** (if a copy can be found) | Historical routes, rough shapes | Low | "Then" layer |
| **cebujeepneys.weebly.com** | One map per code | Low–Medium | Cross-checking only. The research suggests a CC BY-NC 3.0 license; confirm on the site before using any geometry, and attribute it per route if used. |
| **Community sightings and reports** | "I saw this jeep" and "this changed" | Signal, not truth | Flags for re-verification |

**Do not use:** Route7's data (rights unverified) or 3D Universal's code tables (they contradict every other source).

### 7.2 Getting official data
- File an FOI request at foi.gov.ph for the Cebu City LPTRP 2024–2028 (route list, maps, units) and the adopting ordinance with annexes.
- Email or visit the Cebu City Transportation Office and LTFRB-7. Introduce JeepOI as a free student project and offer the cleaned data back.
- Ask the department or an adviser for an endorsement letter.

### 7.3 Pulling OSM data
On overpass-turbo.eu:

```
[out:json][timeout:180];
relation["type"="route"]["network"="PH:PUJ:Metro Cebu"];
out body;
>;
out skel qt;
```

Convert with `osmtogeojson` and save to `data/raw/osm/` with the download date in the filename. Repeat with the bus networks for the BRT/MyBus layer.

### 7.4 Field protocol
- **Ride both directions.** GPS logger (GPSLogger for Android, OsmAnd or Strava) at 1–5 second intervals.
- **Log time too:** note departure time and time of day (AM peak, midday, PM peak, night). Ride timestamps feed the travel-time model in Section 8.
- **Name the stops:** at landmarks, terminals and turns, voice-note the stop name people actually use ("Gaisano Fuente," "atbang sa Capitol"). These become named stops on the map.
- **Count headways when you can:** at a busy stop, time how many minutes between jeeps of the same code. This feeds wait-time estimates.
- **Photos:** the signboard at start and end.
- **Fare paid** and whether the jeep is traditional or modern.
- **File naming:** `17B_outbound_2026-11-08_AM_A.gpx` (code, direction, date, time band, initials).
- **Safety:** daytime rides, phones secure, pairs in unfamiliar areas.
- **Cleaning:** map-match traces to roads (OSRM `match` or Valhalla `trace_route`), then hand-check in QGIS or geojson.io.

**Priority rides (they cover most of the tourist map):** 17B, 04L, 01K, 14D, 12G, 04B, 13C, 06H, then 23 and MI-01A on Mactan. Also field-check the routes the team has never seen running (04B, 03Q, 04M, 04A).

### 7.5 Fares as dated data
Fares changed on **28 September 2026** (per suroy.ph, Oct 2026; confirm with LTFRB-7):
- Traditional: ₱14 for the first 4 km, plus ₱2 per km after
- Modern: ₱17 for the first 4 km, plus ₱2.40 per km after
- 20% discount for students, seniors and PWD
- This is a temporary guide until 31 Dec 2026; the official matrix is expected January 2027

So fares live in `data/fares.json` as **dated rules**, never hard-coded:

```json
[
  {
    "effective_from": "2026-09-28",
    "effective_to": "2026-12-31",
    "label": "Temporary LTFRB guide",
    "traditional": { "base": 14, "base_km": 4, "per_km": 2.0 },
    "modern":      { "base": 17, "base_km": 4, "per_km": 2.4 },
    "discount": 0.20,
    "source": "https://suroy.ph/cebu-city-jeepney-guide-2026/",
    "verified": false
  }
]
```

The UI shows which fare rule applied and its date.

**Fare watch (Person A owns this):**
- Once a month, check LTFRB-7 announcements and local news (SunStar, CDN) for fare changes.
- When a change is announced, add a new dated rule to `fares.json`; old rules stay for history.
- Put a reminder in the calendar for early January 2027, when the official matrix is expected.
- If a fare rule is more than 6 months unchecked, the UI shows "fare may be outdated."

### 7.6 Data model

**`data/processed/routes.geojson`** — one Feature per route per direction:

```jsonc
{
  "type": "Feature",
  "geometry": { "type": "LineString", "coordinates": [[123.89, 10.33], "..."] },
  "properties": {
    "id": "17B-out",
    "code": "17B",
    "direction": "outbound",
    "name": "Apas (IT Park) – Carbon",
    "mode": "jeep",                       // jeep | modern_jeep | brt | bus
    "family": "17",
    "stops": ["IT Park", "JY Square", "Capitol", "Fuente", "Colon", "Carbon"],
    "status": "verified",                 // verified | reported | disputed | unconfirmed | discontinued | planned
    "years_active": [2011, null],         // null = still running
    "verification": {
      "last_verified": "2026-11-08",
      "method": "ridden_gps",             // ridden_gps | osm_crosscheck | dated_guide | document
      "by": "A"
    },
    "last_seen": "2026-11-20",
    "headway_min": 6,                     // measured or estimated
    "lptrp": { "in_plan": "unconfirmed", "plan_route": null },
    "sources": ["ride:17B_outbound_2026-11-08_AM_A.gpx", "osm:relation/123456", "https://suroy.ph/cebu-city-jeepney-guide-2026/"]
  }
}
```

**`data/processed/stops.geojson`** — named stops, terminals and transfer hubs (Points): name, aliases ("Gaisano Fuente", "Fuente rotunda"), type (stop, terminal, hub), routes served.

**`data/processed/speeds.json`** — measured speed per route segment per time band (from GPS rides).

**`data/processed/spots.json`** — tourism layer:

```jsonc
{
  "id": "museo-sugbo",
  "name": "Museo Sugbo",
  "category": "museum",
  "area": "M.J. Cuenco Ave",
  "location": [123.905, 10.302],
  "codes": ["01K"],
  "alight_at": "Front of the museum on M.J. Cuenco Ave",
  "walk_min": 1,
  "last_mile": null,                      // or { "from": "JY Square", "mode": "habal-habal", "price": "₱100–150", "note": "Arrange your ride back" }
  "tips": ["Check opening hours", "Small entrance fee"],
  "confidence": "medium-high",
  "last_verified": null,
  "sources": ["https://suroy.ph/cebu-city-jeepney-guide-2026/"]
}
```

**`data/processed/route_history.json`** — dated events for ghost routes and the timeline:

```jsonc
{ "code": "06H", "event": "reported_missing", "date": "2024", "source": "sugbo.ph comment" }
{ "code": "06H", "event": "confirmed_running", "date": "2026-10", "source": "suroy.ph" }
{ "code": "XXy", "event": "discontinued", "date": "2020-03", "evidence": "missing from all 2023+ lists; driver confirmed", "source": "..." }
```

### 7.7 Building ghost routes
1. List every code from each dated source (2011–13 blogs, CDN 2020 and 2023, Sugbo.ph 2024, r/Cebu 2025, suroy.ph and OSM 2026, OSM history).
2. A code found in older lists but missing from every 2026 source becomes a **ghost candidate**.
3. Confirm with a field check or by asking drivers at terminals before marking it discontinued. (06H is the cautionary example: feared gone in 2024, listed again in 2026.)
4. Time-box this: aim for 15–25 well-documented ghosts, not every rumor.

### 7.8 Accuracy rules
- Nothing goes on the map without at least one source.
- Every route and spot shows its status and last-verified date.
- Unverified data is labeled, never hidden and never dressed up as verified.
- Routes with no sighting in 60 days get flagged for re-checking.
- Re-ride core routes every 6 months, or after a report.

---

## 8. Fastest route first: the algorithm

### 8.1 The idea
Treat Cebu's jeep network as a **graph** and find the path with the **lowest total travel time**, not the shortest distance. A 2 km ride on a jammed street can take longer than 4 km on a clear one, and a route that needs a 15-minute wait can lose to a longer ride on a frequent jeep.

**Total trip time = walking time + waiting time + riding time + transfer penalty**

### 8.2 Building the graph
- **Stops:** jeeps stop almost anywhere, so place a stop every 150–200 m along each route, plus the named stops at landmarks and terminals.
- **Two kinds of nodes**, so the algorithm knows whether you're on the street or on a jeep:
  - **Street node** at each stop: you're standing there.
  - **On-board node** for each (stop, route) pair: you're riding that route at that stop.
- **Edges and their weights (all in seconds):**
  - **Ride:** on-board stop → next on-board stop on the same route. Weight = segment length ÷ measured speed for that segment and time of day.
  - **Board:** street → on-board. Weight = expected wait (half the headway, e.g. a jeep every 8 minutes means about 4 minutes of waiting) + a small boarding penalty.
  - **Get off:** on-board → street. Small weight.
  - **Walk:** start → nearby stops, stops → destination, and between stops of different routes within about 300 m (transfers). Weight = walking distance ÷ 1.2 m/s.
  - **Transfer penalty:** extra weight (around 3 minutes) every time you board a second jeep, because transfers are annoying even when quick.

### 8.3 The search
- Run **Dijkstra's algorithm** from the start to the destination on this graph. It's the classic shortest-path algorithm from data structures, and with only thousands of nodes it runs in milliseconds in the browser.
- **A\* upgrade:** add a heuristic (straight-line distance ÷ the fastest plausible jeep speed) to speed it up. It finds the same answer with fewer steps.
- **Three answers for three tabs:**
  - **Fastest:** the normal run.
  - **Fewest transfers:** rerun with a very large transfer penalty.
  - **Cheapest:** gather a pool of good candidates (the runs above plus Yen's k-shortest paths, k = 5), compute each one's exact fare from the dated fare rules, and sort.
- **v2 upgrade:** a frequency-based version of **RAPTOR**, the algorithm real transit apps use. It works in rounds (best time with 0 transfers, then 1, then 2) and naturally gives the time-vs-transfers trade-off.

### 8.4 Where the speeds come from
- **v1:** our GPS rides give the median speed per road segment per time band (AM peak, midday, PM peak, night).
- **Before enough rides exist:** fall back to default speeds (for example 12 km/h downtown, 18 km/h elsewhere), clearly marked as estimates.
- **Walking:** v1 uses straight-line distance × 1.3 to approximate street detours, labeled as an estimate. v2 uses real walking paths from OSM footways, which also beats Route7's straight-line estimates.

### 8.5 Keeping it honest
- Each result shows the time breakdown, and uses "about" until a route has measured speeds.
- **Test set:** 20 real trips the team knows well. Target: the planner's top answer is a route a local would actually take in at least 18 of 20.
- **Calibration:** ride 10 of those trips and compare predicted vs actual time. Target: within ±25% for at least 8 of 10.

### 8.6 Precomputed extras
The same graph powers a stretch feature: **"How far can I get in 30 minutes?"** maps, precomputed offline for key landmarks.

### 8.7 Performance budget and where the search runs

**What's precomputed vs what runs per search:**

| Step | When | Where |
|---|---|---|
| Clean GPS, build routes, stops, speeds | When data changes | Python pipeline |
| Build the graph (nodes, edges, weights) | When data changes | `pipeline/build_graph.py` → `graph.json` |
| Find nearest stops to start and end | Every search | Browser (spatial index, e.g. `kdbush`) |
| Dijkstra/A* for Fastest, Fewest transfers | Every search | Browser |
| k-shortest candidates + exact fares for Cheapest | Every search | Browser |

**Size estimate:** about 100 route directions × about 80 stops each ≈ 8,000–10,000 on-board nodes, a few thousand street nodes, and roughly 30,000–50,000 edges. Complexity is O((V + E) log V) with a binary-heap priority queue.

**Targets (measured, not assumed):**
- Graph file: under 1 MB gzipped
- One search (all three tabs): under 100 ms on a mid-range Android phone
- First load of the planner: under 3 seconds on 4G

**How we measure:** a benchmark script runs the 20-trip test set 100 times and reports the median and 95th-percentile search time, on a laptop and on a real mid-range phone. Results go in `docs/benchmarks.md` and get re-run whenever the graph grows.

**Caching:**
- `graph.json` gets a content hash in its filename, so browsers and the CDN cache it until the data actually changes.
- The routing code runs in a Web Worker, so searches never freeze the map.
- Recent searches are memoized in memory, so switching between result tabs is instant.

**When we'd move routing to a server:** if the graph passes about 100,000 nodes (all of Metro Cebu plus buses and V-hire), if search time on a phone goes over 300 ms, or if we ever add live data. Then the same algorithm moves into a serverless function with cached results for popular trips. The algorithm doesn't change, only where it runs.

**Keeping the graph fresh:** a GitHub Action rebuilds `graph.json` whenever files in `data/` change, runs the 20-trip test set, and blocks the deploy if trips that used to pass start failing.

---

## 9. Tourism starter dataset

From the research report (full table with sources in `reports/Cebu jeepney apps and tourism.md`). Every row gets field-verified and dated before launch.

| Spot | Category | Codes (current sources) | Get off at | Last mile / note | Confidence |
|---|---|---|---|---|---|
| Basilica del Santo Niño, Magellan's Cross | Heritage, church | 17B; any Colon jeep (01K, 13C, 14D) | Colon | Under 10 min walk; Basilica dress code | Medium–High |
| Fort San Pedro, Plaza Independencia, National Museum | Heritage, museum | No current code; "Plaza"/"Pier" jeeps | Plaza Independencia | Or 15–20 min walk from Magellan's Cross | Low |
| Parian cluster (Heritage Monument, Casa Gorordo, Yap-San Diego) | Heritage | 01K | Parian | One walkable cluster | Medium |
| Museo Sugbo | Museum | 01K | M.J. Cuenco Ave | Right on the route | Medium–High |
| Carbon Market | Market, food | 04B, 13B, 17B, 62B | Carbon | Redevelopment ongoing; recheck access | High (17B/04B) |
| Taboan Market | Market (dried fish) | 12G | Taboan | Pasalubong stop | Medium–High |
| Fuente Osmeña, Larsian BBQ | Landmark, food | 04B, 17B | Fuente | Larsian best at night | High / Medium |
| IT Park, Sugbo Mercado | Food, nightlife | 17B, 17C, 17D | IT Park | Check market days | High |
| SM City Cebu | Mall, hub | 01K, 03Q, 04L, 06H, 10H, 10M, 12G, 12I | SM terminal | Major transfer hub | High |
| Ayala Center Cebu | Mall, hub | 03Q, 04L, 06H, 12L, 14D | Ayala terminal | 14D links to Colon heritage | High |
| JY Square | Uphill gateway hub | 04L; 17B/C/D via Lahug | JY Square | Start of every uphill trip | High |
| Temple of Leah | Viewpoint | **No jeep** | JY Square | Habal-habal ₱100–150 or Grab ₱200–400; arrange return | No jeep |
| Sirao Flower Garden | Nature | **No jeep** (LPTRP plans a Sirao–IT Park route) | JY Square | Habal-habal; ₱100 entry | No jeep |
| Tops Lookout | Viewpoint | **No jeep** (04L does not go there) | JY Square | Shuttle, taxi or agreed motorcycle | No jeep |
| Taoist Temple | Temple | **No jeep** | Lahug / JY | Taxi or Grab; book a round trip | No jeep |
| Mactan Shrine, Sutukil row | Heritage, seafood | 23, MI-01A | Shrine | Pick your seafood to be cooked | Medium |
| Maribago / Punta Engaño resorts | Beach | 23, MI-02B, MI-01A | Resort gates | Most beaches need a day pass | Medium |
| SM Seaside | Mall | **No traditional jeep;** MyBus, modern jeep via CCLEX | Terminal | Mark as bus / modern jeep only | High |

---

## 10. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + TypeScript + Vite | Common, fast, good for portfolios |
| Map | MapLibre GL JS | Free, vector tiles, smooth camera, `line-offset` and `line-dasharray` for meaningful styles |
| Basemap | OpenFreeMap or Protomaps (PMTiles), with a custom night style | Free, no billing surprises, fully restylable |
| Animation layers | deck.gl via `MapLibreOverlay` (TripsLayer for animated jeeps) | Fading-trail jeeps, heatmaps |
| Geo utilities | Turf.js | Distances, nearest point, `along` for ride-along |
| Routing | Custom Dijkstra/A* in TypeScript (or `ngraph.path`) on a precomputed graph | Runs in the browser, no server needed |
| Motion and story | GSAP + ScrollTrigger (GSAP is now fully free), or Scrollama | Pinned map story, scrubbing, stacking |
| UI | Tailwind CSS, Vaul-style bottom sheet | Fast to build, mobile-first |
| Charts | Observable Plot | Clean, small |
| Data pipeline | Python (geopandas, shapely, gpxpy) + OSRM/Valhalla for map matching | Clean GPS, build graph and GeoJSON |
| Reports and sightings | Google Form in v1, Supabase in v2 | Free tier |
| Jepoy (v2) | LLM API with function calling, behind a Vercel serverless function | Key stays server-side |
| Hosting | Vercel or Netlify | Free, deploys on every push |

**Architecture rule:** precompute everything heavy offline (graph, speeds, isochrones, animated paths) and ship static files. That's how the best transit visualizations stay fast, and Cebu has no live feed anyway.

---

## 11. Roles (team of two)

Split by feature, so both people touch data, frontend and maps.

| | **Person A — Trips, Data and Algorithm** | **Person B — Map UX, Tourism and Story** |
|---|---|---|
| Data | OSM import, GPS cleaning and map matching, stops, speeds, fares | Spots dataset, ghost-route research, LPTRP/FOI follow-up, route history |
| Features | Fastest-first planner (graph, Dijkstra, result tabs), bus layer, Jepoy backend (v2) | Explorer and trust ledger UI, Tour Lines and ride-along, ghost routes, scrollytelling, landing page |
| Shared | Field rides (split by route), code reviews on every PR, design decisions, hallway tests | |

**Workflow:** GitHub repo, `main` always deployable, feature branches and pull requests reviewed by the other person, a GitHub Projects board, a 30-minute weekly sync to plan the week and pick routes to ride.

---

## 12. Timeline (14 weeks)

### Phase 0 — Setup (Week 1)
- [ ] Repo, Vite + React + TS, MapLibre with a custom night basemap, deploy to Vercel
- [ ] File the FOI request; email the CCTO and LTFRB-7
- [ ] Data schema (routes, stops, spots, speeds, fares, history) with trust-ledger fields
- [ ] Load the Sept 2026 fare rules as dated data
- [ ] Write the hallway-test script (Section 14)

### Phase 1 — Data foundation (Weeks 2–4)
- [ ] OSM import (jeeps + BRT + MyBus), saved raw with dates
- [ ] Python pipeline: GPX → map-matched lines → routes, stops and speeds
- [ ] Ride the priority routes both directions, with timestamps and stop names
- [ ] Check the never-seen routes (04B, 03Q, 04M, 04A)
- [ ] Terminals, hubs and about 50 named stops/landmarks
- [ ] Frontend shell: smart default view, named markers, bottom sheet, signboard components, pin/clear
- **Done when:** the priority routes render with trust badges, and stops and terminals have names

### Phase 2 — Explorer and fastest-first planner (Weeks 5–7)
- [ ] Route Explorer: tap route/stop/street, search, filters, trust ledger panel, sightings button
- [ ] Parallel lines on Colon and Osmeña Blvd
- [ ] Graph build script (street and on-board nodes, ride/board/walk edges)
- [ ] Dijkstra/A*, then Fastest / Cheapest / Fewest transfers tabs
- [ ] Result cards with time breakdown, board/alight names, fares
- [ ] Run the 20-trip test set
- [ ] Run the same 20 trips on Google Maps and Route7 and record results (H5)
- [ ] Benchmark script, Web Worker routing, results in `docs/benchmarks.md`
- [ ] GitHub Action: rebuild graph and run trip tests on every data change
- **Done when:** 18 of 20 test trips give a sensible top answer, one search runs under 100 ms on a mid-range phone, and a friend can find "which jeeps pass Fuente" in under 30 seconds

### Phase 3 — Tourism (Weeks 8–9)
- [ ] Spots dataset, field-checked alighting points
- [ ] Four Tour Lines with ride-along camera
- [ ] "Where can this jeep take me?" and last-mile connectors with prices
- [ ] **Hallway tests** with tourists and students (go/no-go on polishing tourism and on building Jepoy's chat, Section 14)
- **Done when:** a first-time visitor can plan a 17B heritage trip without help

### Phase 4 — Time machine and story (Weeks 10–11)
- [ ] Ghost-route diffing (15–25 documented ghosts) and history file
- [ ] Era slider, before/after LPTRP swipe, "Is my jeep affected?"
- [ ] Scrollytelling page (5 chapters) with GSAP pinning and counters
- **Done when:** someone new to the LPTRP can explain it after scrolling once

### Phase 5 — Polish and launch (Weeks 12–13)
- [ ] Landing page (hero with from/to fields and animated network, pinned "How it works," bento, marquee, story, route news, honest proof numbers, call to action)
- [ ] Route notices: Sinulog closures and current roadworks
- [ ] FAQ, privacy and terms pages, contact email, version number and changelog
- [ ] 30-second demo video for launch posts
- [ ] Animated jeeps on the home map (TripsLayer)
- [ ] Reduced-motion pass, accessibility pass, Bisaya/English toggle
- [ ] Report, sighting and "this changed" forms
- [ ] About page: sources, methodology, trust ledger explanation, licenses and attribution
- [ ] Calibrate travel times against real rides
- [ ] Launch on r/Cebu, school org pages, local tech groups; offer route fixes to OSM

### Phase 6 — Buffer (Week 14)
- [ ] Fix launch feedback, re-verify anything reported
- [ ] If time allows: hand-drawn schematic "metro map" poster of the trunk routes

Keep riding and verifying routes in the background through every phase.

---

## 13. After launch (v2 and beyond)

- **Jepoy** mascot chat helper, with the trap-question test set passing first (Section 5.6)
- Combined jeep + BRT trips; Ceres, Beep and V-hire layers
- Real walking paths from OSM footways
- "How far in 30 minutes?" maps for key landmarks
- Frequency-based RAPTOR planner
- More cities: Mandaue, Lapu-Lapu, Talisay, Consolacion
- Offline mode (PWA) for weak signal
- GTFS export and an open dataset release, so other apps (and maybe Google Maps) can use verified Cebu data
- Signboard scanner: point your camera at a jeep's code and see its route
- Sound toggle and day/night map tint

---

## 14. Validation: what would prove JeepOI is working

The biggest risk is demand, not code. Nobody has shown yet that tourists want a jeepney tourism layer. Test early and cheaply.

**Hallway tests (Phase 3), 10+ people at hostels, language schools and campus:**

| Hypothesis | Test | Pass | If it fails |
|---|---|---|---|
| **H1:** Tourists find code-first tourism useful | Task: "Get from IT Park to Museo Sugbo and one more heritage spot." Then ask whether they'd use Tour Lines over Google Maps. | 6 of 10 complete it unaided, and 6 of 10 say yes | Stop polishing tourism; focus on commuters and the trust ledger |
| **H2:** People notice and understand the trust ledger | Ask testers what the badge on a route means | 7 of 10 explain it correctly | Redesign the badge and wording |
| **H3:** "Fastest" is actually fast | Compare predicted vs actual ride times on 10 trips | 8 of 10 within ±25% | Ride more, recalibrate speeds |
| **H4:** The map is easier than Route7 | Same task on both apps, timed | JeepOI faster for most testers | Revisit the teardown fixes |
| **H5:** We know how JeepOI compares to Google Maps | Run the same 20 test trips on Google Maps, Route7 and JeepOI. For each, record: does it suggest a route a local would actually take, the codes suggested, predicted time vs our measured time, and whether a fare is shown. | We publish the comparison either way | If Google wins on planning, lean harder into trust, tourism and story; the planner stays a doorway. If JeepOI wins, the comparison itself becomes our best launch post. |
| **H6:** People want to chat with Jepoy | In hallway tests, ask: "Would you rather type a question to a mascot or tap start and end on the map?" | 5 of 10 prefer asking | Keep Jepoy as a mascot only, skip the chat |

**Scope boundary:** JeepOI is not a live tracker, not a booking service, and not an official LTFRB source. It says so on the About page.

---

## 15. Risks and how we handle them

| Risk | Plan |
|---|---|
| Official LPTRP data never arrives | Use news coverage for the story, mark planned routes "document only," keep following up |
| Too many routes to ride | Priority tourist and core routes first; label the rest unverified; sightings fill gaps |
| Routes change mid-project | That's content. Log it in route history. |
| Planner gives wrong answers | 20-trip test set, calibration rides, visible confidence |
| Fares change again in Jan 2027 | Fares are dated data; one file to update; monthly fare watch with a named owner |
| "Google Maps already does this" | Measure it (H5) and publish the comparison; our headline is trust, tourism and story, not the planner |
| LLM costs grow | Core has no AI; Jepoy has a small model, caching, rate limits and a hard monthly cap, and is cut first |
| Search gets slow as data grows | Performance budget and benchmark (Section 8.7); move routing to a serverless function past the stated thresholds |
| Burnout (it's a side project) | Tiers let us ship Tier 1 and stop; no feature is worth losing the fun |
| Tourism demand is weak | Hallway tests decide before polishing (H1) |
| Scope creep | Tiers in Section 5; Jepoy and stretch goals wait for v2 |
| One teammate gets busy | Features are owned end-to-end, so one can pause without blocking the other |
| Competitors copy features | The trust ledger and ghost routes rest on field data and archive research, which can't be copied overnight |

---

## 16. Licensing and attribution
- **OSM data is ODbL:** credit "© OpenStreetMap contributors" on the map; if we publish a modified dataset derived from OSM, release it under ODbL too.
- **cebujeepneys.weebly:** confirm its license before using any geometry; if used, attribute it on each route and stay non-commercial.
- **Route7, Google Maps and other apps:** never copy their data or designs.
- **Our own ridden data:** release openly (ODbL, or CC BY for non-OSM-derived parts) and contribute fixes back to OSM.

---

## 17. Repo structure

```
jeepoi/
├── app/                        # React + Vite frontend
│   ├── src/
│   │   ├── map/                # MapLibre setup, styles, layers, markers
│   │   ├── features/
│   │   │   ├── planner/        # graph search, result tabs, pins
│   │   │   ├── explorer/       # routes, trust ledger, sightings
│   │   │   ├── tourism/        # Tour Lines, ride-along, spots, last-mile
│   │   │   ├── ghosts/         # era slider, before/after
│   │   │   ├── story/          # scrollytelling
│   │   │   └── jepoy/          # v2 chat helper UI
│   │   ├── components/         # signboard placard, bottom sheet, badges
│   │   └── lib/                # fares, geo helpers, i18n (Bisaya/English)
│   └── public/data/            # built GeoJSON/JSON + graph served to the browser
├── api/                        # serverless functions (reports in v2, Jepoy in v2)
├── pipeline/                   # Python data scripts
│   ├── fetch_osm.py
│   ├── clean_gpx.py
│   ├── map_match.py
│   ├── build_routes.py
│   ├── build_speeds.py
│   ├── build_graph.py
│   └── diff_history.py         # ghost-route candidates from dated sources
├── data/
│   ├── raw/                    # osm/, gpx/, documents/, sources/ (never edited)
│   ├── processed/              # routes, stops, spots, speeds, route_history
│   └── fares.json              # dated fare rules
├── tests/
│   ├── trips.json              # 20-trip planner test set
│   └── jepoy_traps.json        # v2 chatbot trap questions
├── docs/
│   ├── methodology.md
│   ├── field-protocol.md
│   ├── hallway-tests.md
│   ├── benchmarks.md           # search-time results per graph version
│   └── baseline-comparison.md  # 20 trips: Google Maps vs Route7 vs JeepOI
├── reports/
│   └── Cebu jeepney apps and tourism.md
└── plan.md
```

---

## 18. Open questions
- [ ] Which campus or area is our home base for rides?
- [ ] Bisaya-first or English-first UI?
- [ ] Do we partner with a school org, a hostel or the CCTO for visibility and testing?
- [ ] What counts as "verified" for a route we can only ride in one direction?
- [ ] Which LLM provider for Jepoy, and what is our monthly budget for it?

---

## 19. References
- Research report: `reports/Cebu jeepney apps and tourism.md` (competitors, tourism table, visualization feasibility)
- Route7 — https://route7.vercel.app/
- Commute Bacolod (design and UX reference) — https://www.commutebacolod.com/ and https://app.commutebacolod.com/
- JTransit — https://jtransit.github.io/
- suroy.ph Cebu City Jeepney Guide 2026 (codes, Sept 2026 fares) — https://suroy.ph/cebu-city-jeepney-guide-2026/
- OSM wiki: Public transportation in Metro Cebu — https://wiki.openstreetmap.org/wiki/Public_transportation_in_Metro_Cebu
- SunStar: Cebu City LPTRP, 40 routes / 1,013 units — https://www.sunstar.com.ph/cebu/cebu-city-sets-new-limit-only-1013-jeepneys-allowed-on-40-routes
- SunStar: 40 new routes approved — https://www.sunstar.com.ph/cebu/cebu-commuter-overhaul-40-new-routes-approved
- SunStar: route shake-up threatens drivers — https://www.sunstar.com.ph/cebu/route-shake-up-threaten-drivers
- Cebu BRT overview — https://en.wikipedia.org/wiki/Cebu_Bus_Rapid_Transit_System
- Digital Matatus (how students mapped Nairobi's informal transit) — https://digitalmatatus.com/
- SFMTA "Where the Streetcars Used to Go" (inspiration for the era slider) — https://www.sfmta.com/blog/interactive-map-shows-past-present-and-future-sfs-streetcars
- deck.gl TripsLayer — https://deck.gl/docs/api-reference/geo-layers/trips-layer
- MapLibre: animate a point along a route — https://maplibre.org/maplibre-gl-js/docs/examples/animate-a-point-along-a-route/
- FOI portal — https://foi.gov.ph
