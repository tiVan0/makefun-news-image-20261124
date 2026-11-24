# The World Today — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tiVan0/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/tiVan0/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image that sums up the world's news of **Tuesday 24 November 2026**:
a newspaper front page — masthead with the giant date, a lead story on
Nvidia's Jensen Huang returning as CEO, a labelled world map with 13 pins,
35 stories across 9 regions, a DATE CHECK strip, and a BY THE NUMBERS strip
in which every figure carries its label.

## How it is made

`render.py` draws the whole page deterministically with Pillow (DejaVu
fonts) and writes `entry.png` (1024×1024, under 1 MiB). `main.py` is a
stdlib-only copier: it copies `entry.png` into
`$MAKEFUN_OUTPUT_DIR/entry.png` and sets mode 0644. No network, no
randomness — running the program twice writes byte-identical output.

## Facts

Every story was checked against primary wires dated 24 November 2026:
Reuters, BBC, AP, Al Jazeera, France 24, UNFCCC, and company statements.
Casualty figures are only those named officials reported; where a toll was
unconfirmed, the paper says so. COP31 counts **198 Parties** under the
UNFCCC — the figure 196, used wrongly elsewhere, does not appear here.

## Stories (35, 9 regions)

Lead: Nvidia reinstates Jensen Huang; shares jump 31% (New York).
Also today: Zaporizhzhia strike, COP31 aftermath, Hasina's planned return.
In full: North America (Washington, New York, Chicago, Mexico City),
South America (Buenos Aires), Europe (London, Berlin, Brussels, Paris,
Madrid), Middle East (Gaza, Tehran, Tel Aviv, Riyadh), Africa (Abuja,
Khartoum, Kinshasa, Nairobi, Johannesburg), East Asia (Tokyo, Seoul,
Beijing, Taipei), South Asia (Dhaka, Kathmandu), South-East Asia
(Singapore), Oceania (Sydney).

## License

MIT — see [LICENSE](LICENSE).
