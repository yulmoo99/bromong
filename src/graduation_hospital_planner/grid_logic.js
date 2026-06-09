function buildAdaptiveCorridorNetwork() {
  const b = usableBounds();
  if (!b) return [];
  const corridorCells = [];
  const padding = 4;
  for (let r = b.minR + padding; r <= b.maxR - padding; r++) {
    for (let c = b.minC + padding; c <= b.maxC - padding; c++) {
      if (r === b.minR + padding || r === b.maxR - padding || 
          c === b.minC + padding || c === b.maxC - padding) {
        markCorridorWide(r, c, corridorCells);
      }
    }
  }
  return corridorCells;
}
