# Mote Merkén Travel — Astro Frontend V6

Frontend modular desarrollado con Astro + Tailwind CSS.

## Módulos implementados
- `/` Home
- `/tours` Tours
- `/tours/[slug]` Tour detail
- `/experiences` Experiences
- `/experiences/[slug]` Experience detail
- `/about` About Us

Las rutas de Contact, Login y Booking permanecen preparadas para siguientes versiones.

## Desarrollo
```bash
npm install
npm run dev
```

## Arquitectura
Los datos temporales están separados en `src/data/` y usan IDs estables para facilitar una futura conexión a Django + MongoDB sin rediseñar los componentes visuales.

## V8 — Booking frontend

Adds modular booking routes with a simulated availability calendar, occupied dates, schedule/passenger selection, 5-business-day approval window, modify/approve/reject actions and a Webpay-ready payment step. No backend or real payment is connected yet.


## V9 additions
- Traveler login and registration routes: `/login`, `/register`.
- Google Identity Services button prepared for future OAuth client ID + Django session exchange.
- All experience booking CTAs enabled.
- Booking calendar includes a friendly weather preview card.
- Tour coordinates and integration IDs are ready for Google Weather API through a future Django proxy.
- Google Weather daily forecasts are available for up to 10 days; dates further away should display forecast-unavailable until they enter that window.

## V12 — Administration frontend
New standalone administrative routes:
- `/admin`
- `/admin/tours`
- `/admin/destinations`
- `/admin/bookings`
- `/admin/calendar`
- `/admin/media`
- `/admin/users`
- `/admin/pricing-history`

This is intentionally frontend-only. CRUD buttons are visual placeholders for future Django endpoints. Tour prices are explicitly read-only: the future backend pricing engine will generate weekly closures and persist the final USD price displayed on the public website.

The V9 weather preview has been removed from the visible booking flow. Google Weather integration metadata remains available for the future Django integration.


## V12 admin prototype
The admin panel buttons now work entirely in the browser without a database. You can add/edit/disable/delete tours and destinations, upload/rename/remove media, review/change/approve/cancel reservations, edit calendar availability/capacity/schedules, and add/edit/disable users. These prototype changes intentionally reset on page refresh; later Django + MongoDB will persist the same forms and actions. Tour prices remain read-only.


## V12 additions
- Branded Mote Merkén confirmation, information and input dialogs across the admin panel.
- No native browser alert/confirm/prompt dialogs in administration flows.
- New `/admin/exchange-rate` module for daily USD/CLP values.
- Exchange-rate actions work in browser memory only and are ready to map to Django later.
