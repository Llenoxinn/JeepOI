# Design direction

**JeepOI sells trust and time, wrapped in the best-looking map in Cebu.** It should feel Cebuano, not like a generic transit template. Source: `plan.md` sections 3a and 6.

## Principles

1. **Honest first.** Show only what we know, and say how we know it. Unverified routes look unverified. No vanity stats, no "live" claims without live data, no made-up ratings.
2. **The signboard is the brand.** Route codes always appear as windshield placards: on the map, in results, in the marquee.
3. **Fastest answer first.** Every screen should get someone closer to "which jeep, where to board, where to get off."
4. **Local voice.** Bisaya headings with plain English beside them: "Asa ka padulong?", "Unsa'y mga jeep?", "Laag gamit jeep", "Para sa Fuente."
5. **Motion explains, never decorates.** Animation shows a jeep's path, a step in a trip, or a change over time.

## Visual identity

| Element | Choice |
|---|---|
| Base | Deep night map and UI |
| Accent | Signboard yellow |
| Secondary UI | Chrome silver |
| Route families | Color-blind-safe set starting from Okabe-Ito. Color is never the only signal: line pattern and placard label carry meaning too. |
| Headlines | Cabinet Grotesk |
| UI text | Geist |
| Codes and fares | Geist Mono |
| Not | Inter, purple gradients, glow effects |
| Themes | Light and dark, each designed on purpose, not one inverted from the other |

## Map language

Line style shows how much we trust a route, so a glance is enough:

| Status | Line |
|---|---|
| verified | solid |
| unconfirmed | thin |
| disputed | hatched |
| planned | outlined |
| discontinued (ghost) | faded, dashed |

- Shared corridors (Colon, Osmeña Blvd) use parallel offset lines so overlapping routes stay readable.
- Terminals, hubs and landmark stops are named markers, decluttered by zoom.
- Spots no jeep reaches get dashed last-mile connectors with prices, never fake jeep stops.

## Landing page

Floating glass pill nav, then:

1. **Hero:** live network map with animated jeeps under a dark wash, a 2-line headline, the from/to fields, and exactly two buttons ("Plan a trip", "Ride a Tour Line"). No stats or badges.
2. **How it works:** pinned phone mockup, four steps light up as you scroll.
3. **Bento** of 4 cards: Trust ledger, Time machine, Tour Lines, Fastest first. No empty cells.
4. **Story:** pinned map while chapters scroll past.
5. **Route news**, then **proof** (only provable numbers: routes verified, km ridden, last update), then a big call to action and a full footer with sources and OSM attribution.

The app lives at `/app`, with a Jepoy loading screen and a visible version number.

## Trip results

- Summary chips: time, fare, km, number of rides, trust badge.
- Steps: walk → board ("Board at Gaisano Fuente") → ride → get off ("Para sa Colon"). Tapping a step flies the map to it.
- Each ride step has a traditional/modern toggle that updates the fare live.
- Show which fare rule was used and its date.

## Motion

- GSAP ScrollTrigger for the story: pinned map, scrubbed reveals, stacking Tour Line cards.
- Infinite marquee of route placards.
- deck.gl `TripsLayer` jeeps with fading trails, ride-along camera, smooth fly-to.
- Hover and press feedback on everything tappable.
- **Reduced motion is mandatory:** everything settles to its final state. No pinning, scrubbing or auto-scrolling.

## Accessibility

Keyboard navigation and visible focus everywhere. Contrast checked on both themes. Every route and trip on the map can also be read as a list. Animated counters render their real final value in the HTML.

## Don't copy

Route7's data, geometry or look, Google Maps' design, or any other app's design (`plan.md` section 16). Commute Bacolod is a reference for structure only (`plan.md` section 3a).
