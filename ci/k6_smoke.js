// G5 — Smoke de rendimiento. Si un threshold no se cumple, k6 termina con exit code 99
// y el pipeline se detiene (fail-fast). Recorre los flujos tocados por D-001, D-002 y D-003.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:3001';
const JSON_HEADERS = { 'Content-Type': 'application/json', Accept: 'application/json' };

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
    checks: ['rate>0.99'],
  },
};

export function setup() {
  const res = http.post(`${BASE}/auth`, JSON.stringify({ username: 'admin', password: 'password123' }), { headers: JSON_HEADERS });
  return { token: res.json('token') };
}

export default function (data) {
  const booking = {
    firstname: 'Smoke',
    lastname: `VU${__VU}`,
    totalprice: 150,
    depositpaid: true,
    bookingdates: { checkin: '2026-12-01', checkout: '2026-12-04' },
  };

  const created = http.post(`${BASE}/booking`, JSON.stringify(booking), { headers: JSON_HEADERS });
  check(created, {
    'crear reserva válida → 200': (r) => r.status === 200,
    'precio persistido (D-003)': (r) => r.json('booking.totalprice') === 150,
  });
  const id = created.json('bookingid');

  check(http.get(`${BASE}/booking/${id}`, { headers: JSON_HEADERS }), {
    'consultar reserva → 200': (r) => r.status === 200,
  });

  booking.totalprice = 175;
  const updated = http.put(`${BASE}/booking/${id}`, JSON.stringify(booking), {
    headers: Object.assign({ Cookie: `token=${data.token}` }, JSON_HEADERS),
  });
  check(updated, { 'actualizar con token → 200 (D-001)': (r) => r.status === 200 });

  sleep(1);
}
