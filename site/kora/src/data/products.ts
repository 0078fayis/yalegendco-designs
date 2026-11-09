export type Product = {
  id: string; name: string; type: 'top' | 'pant' | 'hoodie'; price: number;
  cols: [string, string][]; fab: string; desc: string; tag?: string; look: number;
};
export const SIZES = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL'];
export const P: Product[] = [
  { id: 'coal-tee', name: 'Charcoal Boxy Tee', type: 'top', price: 69, cols: [['Charcoal', '#4a4844'], ['Bone', '#ece7dc'], ['Black', '#141414']], fab: '280 gsm combed cotton jersey', desc: 'Boxy, dropped shoulder, heavy ribbed neck. Garment-washed so the fit you buy is the fit you keep.', tag: 'Core', look: 1 },
  { id: 'light-denim', name: 'Light Wash Wide Denim', type: 'pant', price: 139, cols: [['Light wash', '#9fb3c4'], ['Grey wash', '#8a8a86']], fab: '12 oz rigid denim', desc: 'Straight wide leg, high rise, button fly. Rinsed once, no stretch, no distressing.', tag: 'Core', look: 1 },
  { id: 'bone-knit', name: 'Cream Boxy Knit', type: 'top', price: 119, cols: [['Cream', '#efe7d2'], ['Olive', '#7a7a55']], fab: 'Cotton and merino, 7 gauge', desc: 'Square body, wide neck, rolled edges. Warm without weight.', look: 2 },
  { id: 'sand-pant', name: 'Sand Wide Trouser', type: 'pant', price: 119, cols: [['Sand', '#c8b08a'], ['Brown', '#6b4f3a'], ['Navy', '#1f2436']], fab: 'Brushed cotton twill', desc: 'Single pleat, wide leg, cut to break once on the shoe.', look: 2 },
  { id: 'black-hoodie', name: 'Black Heavy Hoodie', type: 'hoodie', price: 129, cols: [['Black', '#141414'], ['Rust', '#b5552f']], fab: '400 gsm loopback fleece', desc: 'Double-layer hood, no drawcord, kangaroo pocket, heavy ribbed hem.', tag: 'New', look: 3 },
  { id: 'black-pant', name: 'Black Wide Pant', type: 'pant', price: 119, cols: [['Black', '#141414'], ['Navy', '#1f2436']], fab: 'Brushed cotton twill', desc: 'Elastic back waist, flat front, wide leg.', look: 3 },
  { id: 'olive-crew', name: 'Olive Crew', type: 'top', price: 109, cols: [['Olive', '#7a7a55'], ['Bone', '#ece7dc']], fab: '400 gsm loopback fleece', desc: 'Raglan crew, long cuffs, dropped hem.', look: 4 },
  { id: 'brown-pant', name: 'Brown Wide Trouser', type: 'pant', price: 119, cols: [['Brown', '#6b4f3a'], ['Sand', '#c8b08a']], fab: 'Brushed cotton twill', desc: 'Single pleat, wide leg, cut to break once on the shoe.', look: 4 },
  { id: 'white-tee', name: 'White Boxy Tee', type: 'top', price: 69, cols: [['White', '#f6f4ee'], ['Charcoal', '#4a4844']], fab: '280 gsm combed cotton jersey', desc: 'Same body as the charcoal, in optic white. Opaque at 280 gsm.', tag: 'Core', look: 5 },
  { id: 'grey-denim', name: 'Grey Wash Wide Denim', type: 'pant', price: 139, cols: [['Grey wash', '#8a8a86'], ['Light wash', '#9fb3c4']], fab: '12 oz rigid denim', desc: 'Straight wide leg, high rise, button fly.', look: 5 },
  { id: 'rust-hoodie', name: 'Rust Heavy Hoodie', type: 'hoodie', price: 129, cols: [['Rust', '#b5552f'], ['Black', '#141414']], fab: '400 gsm loopback fleece', desc: 'Double-layer hood, no drawcord, kangaroo pocket, heavy ribbed hem.', tag: 'New', look: 6 },
  { id: 'navy-pant', name: 'Navy Wide Pant', type: 'pant', price: 119, cols: [['Navy', '#1f2436'], ['Black', '#141414']], fab: 'Brushed cotton twill', desc: 'Elastic back waist, flat front, wide leg.', look: 6 },
];
export const money = (n: number) => 'A$' + n.toFixed(2);
