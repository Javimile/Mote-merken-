export const integrations = {
  googleIdentity: {
    id: 'INT-GOOGLE-AUTH-0001',
    provider: 'Google Identity Services',
    endpointKey: 'GOOGLE_AUTH',
    status: 'frontend-ready',
  },
  weather: {
    id: 'INT-GOOGLE-WEATHER-0001',
    provider: 'Google Maps Platform Weather API',
    endpointKey: 'WEATHER_FORECAST',
    dailyForecastDays: 10,
    status: 'frontend-ready',
  },
  webpay: {
    id: 'INT-WEBPAY-0001',
    provider: 'Transbank Webpay',
    endpointKey: 'WEBPAY_CREATE',
    status: 'frontend-ready',
  },
} as const;
