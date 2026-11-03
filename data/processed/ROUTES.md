# JeepOI routes

Generated 2026-11-03 by `pipeline/build_routes.py`. This file is an output. Change a route by editing `data/overrides.yaml`, or replace a bad line by riding it, then rebuild.

The map reads `routes.geojson`. Lists and the trust ledger read `routes.json`. Nothing here is marked verified: verification still means a GPS ride.

- 70 codes
- 69 with geometry (53 drawn from OpenStreetMap, 16 drawn from weebly because OSM had no line)
- 1 disputed
- 1 still need a waypoint list or a ride

OpenStreetMap routes were read with `network=LTFRB Region VII` and `route=bus`. The older wiki tag `PH:PUJ:Metro Cebu` matched nothing on 3 Nov 2026.

Licenses, per feature: OpenStreetMap geometry is ODbL (© OpenStreetMap contributors). Weebly geometry is CC BY-NC 3.0, Cebu Jeepney Maps by John Mercado Lee. Keep both credits. Do not sell the dataset. Route7 was not used.

## Priority routes

| Code | On the map | Status | Geometry | Note |
|---|---|---|---|---|
| 17B | yes | unconfirmed | weebly |  |
| 04L | yes | unconfirmed | osm |  |
| 01K | yes | unconfirmed | osm |  |
| 14D | yes | unconfirmed | weebly |  |
| 12G | yes | unconfirmed | osm |  |
| 04B | yes | unconfirmed | osm | suroy.ph lists it in 2026. The team has not seen it on the road. Field-check before treating it as active. |
| 13C | yes | unconfirmed | osm | OSM and weebly both draw Talamban-Ayala-Colon and the lines match. A 3D Universal page says SM/Ayala/IT Park instead. Ignore 3D Universal. Ride it before marking it verified. |
| 06H | yes | unconfirmed | osm |  |
| 23 | yes | unconfirmed | weebly |  |
| MI-01A | yes | unconfirmed | weebly |  |
| 03Q | yes | unconfirmed | osm | Listed in guides. The team has not seen it on the road. Field-check. |
| 04M | yes | unconfirmed | osm | The team has not seen it on the road. Field-check. |
| 04A | no line | unconfirmed | none | The team has not seen it on the road. Field-check. |
| 04I | yes | disputed | osm | One guide says Plaza Housing-Carbon, another says Busay-Carbon. Ride it before picking an endpoint. |

## Disputed or worth a look

Disputed means the two maps disagree, or `overrides.yaml` says so. A ride settles it.

| Code | Overlap OSM inside weebly | Overlap weebly inside OSM | Note |
|---|---|---|---|
| 01KX | — | — | OSM tags this 01Kx: SM Seaside-Parkmall via Urgello. Plain 01K is Urgello-Parkmall. Check the windshield before treating 01Kx as its own code. |
| 03Q | 1.0 | 1.0 | Listed in guides. The team has not seen it on the road. Field-check. |
| 04A | — | — | The team has not seen it on the road. Field-check. |
| 04B | 0.981 | 0.946 | suroy.ph lists it in 2026. The team has not seen it on the road. Field-check before treating it as active. |
| 04I | 1.0 | 0.663 | One guide says Plaza Housing-Carbon, another says Busay-Carbon. Ride it before picking an endpoint. |
| 04M | 1.0 | 1.0 | The team has not seen it on the road. Field-check. |
| 13C | 1.0 | 1.0 | OSM and weebly both draw Talamban-Ayala-Colon and the lines match. A 3D Universal page says SM/Ayala/IT Park instead. Ignore 3D Universal. Ride it before marking it verified. |

## All codes

| Code | Name | Status | Geometry | Longest km | Stops named | Sources |
|---|---|---|---|---|---|---|
| 01B | Sambag-Pier 1 & 2 | unconfirmed | osm | 4.23 | 24 | OSM 20587182, 20587183; weebly |
| 01C | Robinsons-Colon-Sambag | unconfirmed | osm | 3.91 | 13 | OSM 21251283, 21251284; weebly |
| 01K | Urgello-Parkmall via eMall, Colon, SM, City Health | unconfirmed | osm | 8.91 | 30 | OSM 21251289, 21251290; weebly |
| 01KX | SM Seaside-Parkmall via Urgello | unconfirmed | osm | 13.0 | 36 | OSM 21452000, 21452001 |
| 02B | San Nicolas-Robinsons | unconfirmed | osm | 4.05 | 27 | OSM 21251287, 21251288; weebly |
| 03A | Mabolo-Carbon | unconfirmed | osm | 6.08 | 24 | OSM 21251279, 21251280; weebly |
| 03B | Mabolo-Fuente-Carbon | unconfirmed | osm | 6.0 | 31 | OSM 21251277, 21251278; weebly |
| 03L | Mabolo-Luyo-Carbon | unconfirmed | osm | 5.63 | 24 | OSM 21251273, 21251274; weebly |
| 03Q | Ayala Center-SM City Cebu | unconfirmed | osm | 4.02 | 12 | OSM 21267107, 21267108; weebly |
| 04A | 04A | unconfirmed | none | — | 0 |  |
| 04B | Campo Lahug-Escario-Carbon | unconfirmed | osm | 6.6 | 29 | OSM 21251271, 21251272; weebly |
| 04C | Campo Lahug-Ramos-Carbon | unconfirmed | osm | 7.37 | 36 | OSM 21251269, 21251270; weebly |
| 04D | Plaza Housing-Carbon via Escario, Jones | unconfirmed | osm | 9.48 | 59 | OSM 21254495, 21254496, 21256979, 21256981; weebly |
| 04H | Plaza Housing-Lahug-Carbon-Magallanes | unconfirmed | osm | 8.62 | 31 | OSM 21256982; weebly |
| 04I | Plaza Housing-Lahug-Ramos-Carbon | disputed | osm | 9.13 | 34 | OSM 21256980; weebly |
| 04L | Lahug-SM Cebu | unconfirmed | osm | 4.77 | 22 | OSM 14991302, 14991303; weebly |
| 04M | Ayala Center-Lahug | unconfirmed | osm | 2.36 | 10 | OSM 20587180, 20587181; weebly |
| 06B | Guadalupe-Jones-Carbon | unconfirmed | osm | 6.23 | 28 | OSM 21142705, 21142706; weebly |
| 06C | Guadalupe-Carbon via Jones, B. Rodriguez, Englis | unconfirmed | osm | 6.6 | 23 | OSM 21265626, 21265627; weebly |
| 06F | Guadalupe-Magallanes | unconfirmed | osm | 5.98 | 25 | OSM 21267111, 21267112 |
| 06G | Guadalupe-San Nicolas | unconfirmed | osm | 6.08 | 22 | OSM 21142707, 21142708; weebly |
| 06H | Guadalupe-SM City Cebu | unconfirmed | osm | 8.53 | 38 | OSM 21267109, 21267110; weebly |
| 07B | Banawa-Carbon via Capitol, Jones | unconfirmed | osm | 6.15 | 27 | OSM 21267105, 21267106; weebly |
| 08G | Alumnos-Colon | unconfirmed | osm | 4.96 | 25 | OSM 21241370, 21241371; weebly |
| 09C | Pardo-Carbon | unconfirmed | osm | 7.72 | 33 | OSM 21267103, 21267104; weebly |
| 09F | Pardo-Colon | unconfirmed | osm | 7.62 | 35 | OSM 21267101, 21267102; weebly |
| 09G | Basak-Colon | unconfirmed | osm | 7.2 | 33 | OSM 21241368, 21241369; weebly |
| 10F | Bulacao-Colon | unconfirmed | osm | 7.16 | 23 | OSM 21267099, 21267100; weebly |
| 10G | Pardo-Magallanes | unconfirmed | osm | 6.85 | 28 | OSM 21251285, 21251286; weebly |
| 10H | Bulacao-Pardo-North Reclamation | unconfirmed | osm | 10.89 | 44 | OSM 21267097, 21267098; weebly |
| 10M | Bulacao-Pardo-SM Cebu | unconfirmed | osm | 10.63 | 41 | OSM 21267095, 21267096; weebly |
| 11A | Inayawan-Colon | unconfirmed | osm | 8.4 | 35 | OSM 21363724, 21363725; weebly |
| 12D | Jeepney 12D: Downtown - Punta Princesa | unconfirmed | osm | 9.45 | 0 | OSM 3203006; weebly |
| 12G | Jeepney 12G: Labangon - Colon - Pier - SM | unconfirmed | osm | 16.07 | 0 | OSM 3203041; weebly |
| 12I | Jeepney 12I: SM Cebu - Downtown - Punta Princesa | unconfirmed | osm | 15.6 | 0 | OSM 3203115; weebly |
| 12L | Jeepney 12L: Ayala - Escario- Labangon | unconfirmed | osm | 14.3 | 0 | OSM 3169782; weebly |
| 13B | Talamban-Ayala-Carbon | unconfirmed | osm | 13.06 | 43 | OSM 21251281, 21251282; weebly |
| 13C | Talamban-Ayala-Colon | unconfirmed | osm | 11.62 | 40 | OSM 21251275, 21251276; weebly |
| 13H | Pit-os to Mandaue Public Market | unconfirmed | weebly | 12.03 | 0 | weebly |
| 14D | Ayala Terminal to Colon | unconfirmed | weebly | 7.68 | 0 | weebly |
| 17B | Apas to Carbon | unconfirmed | weebly | 9.48 | 0 | weebly |
| 17C | Jeepney 17C: Apas - Lahug - Carbon via Ramos, San Nicolas | unconfirmed | osm | 13.18 | 0 | OSM 3203945; weebly |
| 17D | Jeepney 17D: Apas - Lahug - Carbon via Escario, Jones, San Nicolas | unconfirmed | osm | 14.91 | 0 | OSM 3204007; weebly |
| 20A | Ayala Center-Pacific Mall | unconfirmed | osm | 11.7 | 40 | OSM 3207109, 3207166; weebly |
| 20B | Ayala terminal to Ibabao - Estancia | unconfirmed | weebly | 10.1 | 0 | weebly |
| 21A | Cathedral-Pacific Mall | unconfirmed | osm | 12.36 | 52 | OSM 21241575, 21241576; weebly |
| 21D | P. Burgos–Pacific Mall (odd) | unconfirmed | osm | 21.99 | 0 | OSM 3210109, 3211723; weebly |
| 22A | Ouano (Mandaue City)-Cebu City | unconfirmed | osm | 8.99 | 44 | OSM 21241366, 21241367; weebly |
| 22D | Ibabaw (Mandaue City)-Manalili-Cebu City | unconfirmed | osm | 9.4 | 44 | OSM 3208008, 3208066; weebly |
| 22G | Cathedral to Mandaue (Ouano) | unconfirmed | weebly | 10.41 | 0 | weebly |
| 22I | Country Mall to Mandaue Public Market | unconfirmed | weebly | 5.86 | 0 | weebly |
| 23 | Parkmall to Punta Engano | unconfirmed | weebly | 18.66 | 0 | weebly |
| 23D | Opon to Mandaue | unconfirmed | weebly | 8.12 | 0 | weebly |
| 24 | Consolacion to White Gold via Sm and Mabolo | unconfirmed | weebly | 12.72 | 0 | weebly |
| 25 | Mandaue–Lilo-an via Makro | unconfirmed | osm | 15.4 | 0 | OSM 3279746; weebly |
| 44 | Jeepney 44: Naga - Basak - Punta Princesa | unconfirmed | osm | 23.31 | 3 | OSM 3183060 |
| 52 | Guba-Fuente | unconfirmed | osm | 24.06 | 0 | OSM 3171936, 14140743 |
| 60 | Jeepney 60: Bonbon - Lahug - Carbon | unconfirmed | osm | 40.64 | 0 | OSM 3171907 |
| 62B | Pit-os to Carbon | unconfirmed | weebly | 14.03 | 0 | weebly |
| 62C | Pit-os to Carbon | unconfirmed | weebly | 14.9 | 0 | weebly |
| MI-01A | Punta Engano to Opon Public Market | unconfirmed | weebly | 13.1 | 0 | weebly |
| MI-02B | Mandaue to Maribago | unconfirmed | weebly | 18.16 | 0 | weebly |
| MI-03A | Cordova to Opon Public Market | unconfirmed | weebly | 7.61 | 0 | weebly |
| MI-03B | Cordova to Mepz1 via Opon Public Market | unconfirmed | weebly | 13.34 | 0 | weebly |
| MI-04A | Tamiya-SM City JMall | unconfirmed | osm | 8.16 | 25 | OSM 20605538, 20605539, 20605540, 20605541; weebly |
| MI-04B | Tamiya-MEPZ1 (inbound) | unconfirmed | osm | 5.91 | 13 | OSM 20605536, 20605537; weebly |
| MI-05A | Mactan Airport to Opon Church (Ferry Boat Terminal) | unconfirmed | weebly | 6.1 | 0 | weebly |
| MY01 | MyBus 01: SRP-SM Cebu | unconfirmed | osm | 18.89 | 1 | OSM 6197178 |
| MY02 | MyBus 02: SM Seaside-Talisay Anjo World | unconfirmed | osm | 21.31 | 1 | OSM 6260176 |
| MY05 | MyBus 05: Fuente-SM Seaside | unconfirmed | osm | 4.81 | 1 | OSM 6257505 |
