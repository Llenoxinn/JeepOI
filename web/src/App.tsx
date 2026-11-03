import { useEffect, useRef } from 'react'
import * as maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

// shortcut: stock OpenFreeMap dark style, swap for our own night style (design.md) later
const BASEMAP = 'https://tiles.openfreemap.org/styles/dark'
const CEBU: [number, number] = [123.9, 10.315]

export default function App() {
  const container = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const map = new maplibregl.Map({
      container: container.current!,
      style: BASEMAP,
      center: CEBU,
      zoom: 12.5,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    return () => map.remove()
  }, [])

  return <div ref={container} style={{ height: '100%' }} />
}
