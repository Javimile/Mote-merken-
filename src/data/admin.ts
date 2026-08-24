export const adminStats = [
  { id: 'ADM-STAT-001', label: 'Active tours', value: '12', note: 'Publicly visible' },
  { id: 'ADM-STAT-002', label: 'Pending reservations', value: '8', note: 'Awaiting action' },
  { id: 'ADM-STAT-003', label: 'Blocked dates', value: '14', note: 'Across all tours' },
  { id: 'ADM-STAT-004', label: 'Media assets', value: '86', note: 'Images + videos' },
];

export const adminReservations = [
  { id: 'AGN-000231', traveller: 'Emma Wilson', tour: 'Rapa Nui', date: '04 Sep 2026', status: 'Pending approval' },
  { id: 'AGN-000230', traveller: 'Thomas Reed', tour: 'Pucón', date: '29 Aug 2026', status: 'Approved' },
  { id: 'AGN-000229', traveller: 'Sofia Martin', tour: 'Santiago', date: '26 Aug 2026', status: 'Paid' },
  { id: 'AGN-000228', traveller: 'Noah Carter', tour: 'Atacama', date: '18 Sep 2026', status: 'Pending approval' },
];

export const adminDestinations = [
  { id: 'DES-0001', name: 'Rapa Nui', slug: 'rapa-nui', active: true, tours: 3 },
  { id: 'DES-0002', name: 'Pucón', slug: 'pucon', active: true, tours: 2 },
  { id: 'DES-0003', name: 'Santiago', slug: 'santiago', active: true, tours: 4 },
  { id: 'DES-0004', name: 'San Pedro de Atacama', slug: 'san-pedro-atacama', active: true, tours: 3 },
];

export const adminTours = [
  { id: 'TOU-0001', name: 'Living Rapa Nui', destination: 'Rapa Nui', status: 'Active', finalPrice: 'Pending pricing engine' },
  { id: 'TOU-0002', name: 'Pucón Volcano & Lakes', destination: 'Pucón', status: 'Active', finalPrice: 'Pending pricing engine' },
  { id: 'TOU-0003', name: 'Santiago Local', destination: 'Santiago', status: 'Active', finalPrice: 'Pending pricing engine' },
  { id: 'TOU-0004', name: 'Baltinache Desert', destination: 'San Pedro de Atacama', status: 'Active', finalPrice: 'Pending pricing engine' },
];

export const pricingHistory = [
  { id: 'CIE-2026-034', week: 'Week 34', date: '21 Aug 2026', tours: 12, changed: 0, status: 'Closed' },
  { id: 'CIE-2026-033', week: 'Week 33', date: '14 Aug 2026', tours: 12, changed: 0, status: 'Closed' },
  { id: 'CIE-2026-032', week: 'Week 32', date: '07 Aug 2026', tours: 12, changed: 0, status: 'Closed' },
];
