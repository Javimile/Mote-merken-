export type Tour = {
  id: string;
  destinationId: string;
  slug: string;
  name: string;
  location: string;
  region: string;
  image: string;
  eyebrow: string;
  summary: string;
  description: string;
  experience: 'Culture' | 'Adventure' | 'Nature' | 'City';
  format: 'Private' | 'Tailor-made';
  highlights: string[];
  latitude: number;
  longitude: number;
};

// Frontend seed data only. When Django is connected, this module can be
// replaced by API responses without changing the TourCard/TourDetail UI.
export const tours: Tour[] = [
  {
    id: 'TOU-0001',
    destinationId: 'DES-0001',
    slug: 'atacama-baltinache',
    name: 'Baltinache & Atacama',
    location: 'San Pedro de Atacama',
    region: 'Atacama Desert',
    image: '/assets/baltinache.jpg',
    eyebrow: 'Northern Chile',
    summary: 'Salt lagoons, desert light and otherworldly landscapes in the driest desert on Earth.',
    description: 'A private Atacama experience shaped around the landscapes and rhythms of northern Chile. The final route, schedule and services will be supplied by the booking backend once confirmed with the client.',
    experience: 'Nature',
    format: 'Tailor-made',
    latitude: -22.9112,
    longitude: -68.2011,
    highlights: ['Baltinache lagoons', 'Atacama landscapes', 'Private travel style'],
  },
  {
    id: 'TOU-0002',
    destinationId: 'DES-0002',
    slug: 'rapa-nui',
    name: 'Rapa Nui',
    location: 'Easter Island',
    region: 'Rapa Nui',
    image: '/assets/rapa-nui.jpg',
    eyebrow: 'Pacific Chile',
    summary: 'Ancestral culture, volcanic scenery and the extraordinary heritage of Rapa Nui.',
    description: 'Discover Rapa Nui through a carefully curated private journey. Detailed itinerary, availability and confirmed rates will come from Django when the reservation module is connected.',
    experience: 'Culture',
    format: 'Private',
    latitude: -27.1127,
    longitude: -109.3497,
    highlights: ['Rapa Nui heritage', 'Volcanic landscapes', 'Local cultural context'],
  },
  {
    id: 'TOU-0003',
    destinationId: 'DES-0003',
    slug: 'pucon',
    name: 'Pucón',
    location: 'Pucón',
    region: 'Araucanía',
    image: '/assets/pucon.jpg',
    eyebrow: 'Southern Chile',
    summary: 'Volcanoes, forests and outdoor experiences surrounded by the landscapes of Araucanía.',
    description: 'A flexible southern Chile experience centered on Pucón and its natural setting. Activities, operational times and availability remain ready to be populated from the future API.',
    experience: 'Adventure',
    format: 'Tailor-made',
    latitude: -39.282,
    longitude: -71.9543,
    highlights: ['Volcanic scenery', 'Outdoor experiences', 'Southern forests'],
  },
  {
    id: 'TOU-0004',
    destinationId: 'DES-0004',
    slug: 'santiago',
    name: 'Santiago',
    location: 'Santiago',
    region: 'Metropolitan Region',
    image: '/assets/santiago.jpg',
    eyebrow: 'Central Chile',
    summary: 'Architecture, gastronomy, neighborhoods and the Andes from Chile’s capital.',
    description: 'A private introduction to Santiago designed around culture, city life and the Andes. Confirmed schedules and bookable services will later be managed from Django and MongoDB.',
    experience: 'City',
    format: 'Private',
    latitude: -33.4489,
    longitude: -70.6693,
    highlights: ['Urban culture', 'Local gastronomy', 'Andean setting'],
  },
];

export const getTourBySlug = (slug: string) => tours.find((tour) => tour.slug === slug);
