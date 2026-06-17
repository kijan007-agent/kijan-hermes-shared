# Chart.js Zone + Spoon Icon Pattern

## Context
Kijan Personal Tracker dashboard uses Chart.js for the "Today's Check-in" energy progression graph.
Need background color zones (red/yellow/green) and spoon icons at data points.

## Zone Background Plugin

```javascript
const zonePlugin = {
  id: 'zonesPlugin',
  beforeDatasetsDraw(chart) {
    const ctx = chart.ctx;
    const yScale = chart.scales.y;
    const xScale = chart.scales.x;
    const zones = [
      { min: 0, max: 10, color: 'rgba(239, 68, 68, 0.15)' },  // Red
      { min: 10, max: 20, color: 'rgba(245, 158, 11, 0.15)' }, // Yellow
      { min: 20, max: 30, color: 'rgba(34, 197, 94, 0.15)' }   // Green
    ];
    zones.forEach(zone => {
      if (zone.max <= chart.options.scales.y.max) {
        const y1 = yScale.getPixelForValue(zone.min);
        const y2 = yScale.getPixelForValue(zone.max);
        ctx.fillStyle = zone.color;
        ctx.fillRect(xScale.left, y1, xScale.right - xScale.left, y2 - y1);
      }
    });
  }
};
```

## Spoon Icon Plugin

```javascript
const spoonPlugin = {
  id: 'spoonIconPlugin',
  afterDraw(chart) {
    const meta = chart.getDatasetMeta(4); // Today dataset (index 4)
    if (!meta || !meta.data) return;
    const ctx = chart.ctx;
    const data = chart.data.datasets[4].data;
    for (let i = 0; i < data.length; i++) {
      const val = data[i];
      if (!val || val.y <= 0) continue;
      const x = meta.data[i].x;
      const y = meta.data[i].y;
      const icon = val.y >= 20 ? '/static/spoon-green.png'
                 : val.y >= 10 ? '/static/spoon-yellow.png'
                 : '/static/spoon-red.png';
      const img = new Image();
      img.src = icon;
      ctx.drawImage(img, x - 10, y - 10, 20, 20);
    }
  }
};
```

## Chart Config

```javascript
new Chart(ctx, {
  data: { labels, datasets: [...] },
  options: { scales: { y: { min: 0, max: Math.max(totalUnits, 30) } } },
  plugins: [zonePlugin, spoonPlugin]
});
```

## Pitfalls
- Zone bounds must not exceed chart's Y-axis max (`chart.options.scales.y.max`)
- Spoon images are async-loaded; use `new Image()` per point or pre-load in a pool
- If today dataset index shifts, update the hardcoded `4` in spoonPlugin
- Y-axis max must be at least 30 to accommodate all three zones
- Chart.js v4 compatible — uses `beforeDatasetsDraw` and `afterDraw` hooks