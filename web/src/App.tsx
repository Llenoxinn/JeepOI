import { useEffect, useRef } from 'react'
import * as maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import routesUrl from '../../data/processed/routes.geojson?url'
import stopsUrl from '../../data/processed/stops.geojson?url'

// shortcut: stock OpenFreeMap dark style, swap for our own night style (design.md) later
const BASEMAP = 'https://tiles.openfreemap.org/styles/dark'
// MapLibre 6 loads its worker from a separate file the bundler doesn't follow on its own.
maplibregl.setWorkerUrl(workerUrl)

const CEBU: [number, number] = [123.9, 10.315]

// Okabe-Ito, cycled by code family. Color is never the only signal: line style carries status.
const FAMILY_COLOR: maplibregl.ExpressionSpecification = [
  'match',
  ['%', ['to-number', ['slice', ['get', 'family'], 0, 2], 0], 7],
  0, '#E69F00',
  1, '#56B4E9',
  2, '#009E73',
  3, '#F0E442',
  4, '#0072B2',
  5, '#D55E00',
  /* 6 */ '#CC79A7',
]

// Line weight by trust (design.md): verified solid and thick, unconfirmed thin.
const WIDTH: maplibregl.ExpressionSpecification = ['match', ['get', 'status'], 'verified', 4, 2]

export default function App() {
  const container = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const map = new maplibregl.Map({
      container: container.current!,
      style: BASEMAP,
      center: CEBU,
      zoom: 12.5,
      attributionControl: false,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    map.addControl(new maplibregl.AttributionControl({
      customAttribution: '© OpenStreetMap contributors · Cebu Jeepney Maps by John Mercado Lee (CC BY-NC 3.0)',
    }))

    map.on('load', () => {
      map.addSource('routes', { type: 'geojson', data: routesUrl })
      map.addSource('stops', { type: 'geojson', data: stopsUrl })
      map.addLayer({
        id: 'routes',
        type: 'line',
        source: 'routes',
        filter: ['!', ['in', ['get', 'status'], ['literal', ['disputed', 'discontinued']]]],
        layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: { 'line-color': FAMILY_COLOR, 'line-width': WIDTH, 'line-opacity': 0.85 },
      })
      map.addLayer({
        id: 'routes-dashed',
        type: 'line',
        source: 'routes',
        filter: ['in', ['get', 'status'], ['literal', ['disputed', 'discontinued']]],
        paint: {
          'line-color': FAMILY_COLOR,
          'line-width': 2,
          'line-dasharray': [2, 2],
          'line-opacity': ['match', ['get', 'status'], 'discontinued', 0.35, 0.85],
        },
      })
      map.addLayer({
        id: 'stops',
        type: 'circle',
        source: 'stops',
        minzoom: 14,
        paint: {
          'circle-radius': 4,
          'circle-color': '#0b0f17',
          'circle-stroke-color': '#FFD23F',
          'circle-stroke-width': 2,
        },
      })
    })

    for (const layer of ['routes', 'routes-dashed']) {
      map.on('click', layer, (e) => {
        const p = e.features?.[0]?.properties
        if (!p) return
        // GeoJSON sources hand nested properties back as JSON strings.
        const sources: string[] = JSON.parse(p.sources)
        const verification = JSON.parse(p.verification)
        const box = document.createElement('div')
        box.style.color = '#111'
        box.append(
          Object.assign(document.createElement('strong'), { textContent: `${p.code} · ${p.direction}` }),
          Object.assign(document.createElement('div'), { textContent: p.name }),
          Object.assign(document.createElement('div'), {
            textContent: `Status: ${p.status} · last verified: ${verification.last_verified ?? 'never'}`,
          }),
          Object.assign(document.createElement('div'), { textContent: `Sources: ${sources.join(', ')}` }),
        )
        new maplibregl.Popup().setLngLat(e.lngLat).setDOMContent(box).addTo(map)
      })
      map.on('mouseenter', layer, () => (map.getCanvas().style.cursor = 'pointer'))
      map.on('mouseleave', layer, () => (map.getCanvas().style.cursor = ''))
    }

    return () => map.remove()
  }, [])

  return <div ref={container} style={{ height: '100%' }} />
}
