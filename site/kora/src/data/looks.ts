export type Look = { name: string; cut: string; img: string; top: string; bottom: string; pins: [number, number][] };
export const LOOKS: Look[] = [
  { name: 'Studio Day', cut: '/cut/look1.webp', img: '/models/look1.webp', top: 'coal-tee', bottom: 'light-denim', pins: [[0.5, 0.3], [0.46, 0.66]] },
  { name: 'Market Run', cut: '/cut/look2.webp', img: '/models/look2.webp', top: 'bone-knit', bottom: 'sand-pant', pins: [[0.5, 0.3], [0.5, 0.66]] },
  { name: 'Night Shift', cut: '/cut/look3.webp', img: '/models/look3.webp', top: 'black-hoodie', bottom: 'black-pant', pins: [[0.5, 0.32], [0.5, 0.7]] },
  { name: 'Late Arvo', cut: '/cut/look4.webp', img: '/models/look4.webp', top: 'olive-crew', bottom: 'brown-pant', pins: [[0.5, 0.3], [0.5, 0.68]] },
  { name: 'City Edit', cut: '/cut/look5.webp', img: '/models/look5.webp', top: 'white-tee', bottom: 'grey-denim', pins: [[0.5, 0.3], [0.5, 0.68]] },
  { name: 'Sunday Slow', cut: '/cut/look6.webp', img: '/models/look6.webp', top: 'rust-hoodie', bottom: 'navy-pant', pins: [[0.52, 0.32], [0.5, 0.7]] },
];
