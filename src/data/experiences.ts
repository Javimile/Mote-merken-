export type Experience = {
  id: string;
  slug: string;
  title: string;
  category: 'Adventure' | 'Culture' | 'Wellness' | 'Urban';
  destination: string;
  destinationId: string;
  image: string;
  shortDescription: string;
  description: string;
  duration: string;
  level: string;
  highlights: string[];
  relatedTourIds: string[];
  bookingEnabled: boolean;
};

export const experiences: Experience[] = [
  {
    id: 'EXP-0001',
    slug: 'volcano-and-lakes',
    title: 'Volcano & Lakes',
    category: 'Adventure',
    destination: 'Pucón',
    destinationId: 'DES-0003',
    image: '/assets/pucon.jpg',
    shortDescription: 'Raw southern landscapes shaped by volcanoes, forests and water.',
    description: 'A nature-first experience in Chile’s Lake District, designed around dramatic scenery, outdoor exploration and a slower connection with the south.',
    duration: 'Full day / flexible',
    level: 'Active',
    highlights: ['Volcanic landscapes', 'Native forest', 'Lakes and viewpoints', 'Private local guidance'],
    relatedTourIds: ['TOU-0003'],
    bookingEnabled: true,
  },
  {
    id: 'EXP-0002',
    slug: 'living-rapa-nui',
    title: 'Living Rapa Nui',
    category: 'Culture',
    destination: 'Rapa Nui',
    destinationId: 'DES-0002',
    image: '/assets/rapa-nui.jpg',
    shortDescription: 'Culture, landscape and ancestral memory in one of the world’s most remote islands.',
    description: 'Explore Rapa Nui through its archaeological heritage, landscapes and living culture with an itinerary designed to go beyond a checklist of landmarks.',
    duration: 'Half / full day',
    level: 'Easy',
    highlights: ['Moai heritage', 'Local culture', 'Archaeological landscapes', 'Small-group approach'],
    relatedTourIds: ['TOU-0002'],
    bookingEnabled: true,
  },
  {
    id: 'EXP-0003',
    slug: 'desert-wellness',
    title: 'Desert Wellness',
    category: 'Wellness',
    destination: 'Atacama & Spa',
    destinationId: 'DES-0001',
    image: '/assets/spa-experience.jpg',
    shortDescription: 'A softer side of travel built around rest, landscape and restorative moments.',
    description: 'Balance adventure with intentional rest. This experience brings together remote landscapes, calm spaces and wellness moments that complement a journey through northern Chile.',
    duration: 'Flexible',
    level: 'Relaxed',
    highlights: ['Wellness moments', 'Calm-paced itinerary', 'Premium service', 'Can be paired with Atacama tours'],
    relatedTourIds: ['TOU-0001'],
    bookingEnabled: true,
  },
  {
    id: 'EXP-0004',
    slug: 'santiago-local',
    title: 'Santiago, Local',
    category: 'Urban',
    destination: 'Santiago',
    destinationId: 'DES-0004',
    image: '/assets/santiago.jpg',
    shortDescription: 'See the capital through neighbourhoods, food, viewpoints and local rhythm.',
    description: 'A curated introduction to Santiago that mixes iconic places with neighbourhood life, local flavour and flexible stops according to the traveller’s interests.',
    duration: 'Half day',
    level: 'Easy',
    highlights: ['Neighbourhoods', 'Local gastronomy', 'City viewpoints', 'Flexible private route'],
    relatedTourIds: ['TOU-0004'],
    bookingEnabled: true,
  },
];

export const experienceCategories = ['All', 'Adventure', 'Culture', 'Wellness', 'Urban'] as const;
