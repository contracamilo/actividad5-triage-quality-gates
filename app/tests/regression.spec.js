// Pruebas de regresión de la Actividad 5.
// Cada caso empieza con el código del defecto (D-00X) del acta de triage
// (triage/defects.json); triage.py las usa para verificar el criterio de cierre.
const request = require('supertest'),
    expect = require('chai').expect,
    Booking = require('../models/booking');

const server = require('../app');

const BASIC_HARDCODED = 'Basic YWRtaW46cGFzc3dvcmQxMjM=';

const booking = function(overrides) {
  return Object.assign({
    firstname: 'Ana',
    lastname: 'Triage',
    totalprice: 120,
    depositpaid: true,
    bookingdates: {checkin: '2026-12-01', checkout: '2026-12-05'},
    additionalneeds: 'Breakfast'
  }, overrides);
};

// Accept explícito: sin él la API responde 418 antes de validar y la prueba pasaría por la razón equivocada.
const createBooking = function(payload) {
  return request(server).post('/booking').set('Accept', 'application/json').send(payload);
};

const token = async function() {
  const res = await request(server).post('/auth').send({username: 'admin', password: 'password123'});
  return res.body.token;
};

const totalBookings = async function() {
  const res = await request(server).get('/booking');
  return res.body.length;
};

describe('Actividad 5 - regresión de defectos triados', function() {

  beforeEach(function(done) {
    Booking.deleteAll(function() { done(); });
  });

  describe('D-001 escritura sin autenticación real (header Basic hardcodeado)', function() {

    it('D-001 PUT con el header Basic hardcodeado responde 403 y no modifica la reserva', async function() {
      await createBooking(booking());
      const res = await request(server).put('/booking/1')
          .set('Authorization', BASIC_HARDCODED)
          .send(booking({firstname: 'Atacante'}));
      expect(res.status).to.equal(403);
      const after = await request(server).get('/booking/1').set('Accept', 'application/json');
      expect(after.body.firstname).to.equal('Ana');
    });

    it('D-001 PATCH con el header Basic hardcodeado responde 403', async function() {
      await createBooking(booking());
      const res = await request(server).patch('/booking/1')
          .set('Authorization', BASIC_HARDCODED)
          .send({firstname: 'Atacante'});
      expect(res.status).to.equal(403);
    });

    it('D-001 DELETE con el header Basic hardcodeado responde 403 y la reserva sigue existiendo', async function() {
      await createBooking(booking());
      const res = await request(server).delete('/booking/1').set('Authorization', BASIC_HARDCODED);
      expect(res.status).to.equal(403);
      expect(await totalBookings()).to.equal(1);
    });

    it('D-001 con un token válido de /auth la escritura sigue funcionando', async function() {
      await createBooking(booking());
      const res = await request(server).put('/booking/1')
          .set('Accept', 'application/json')
          .set('Cookie', 'token=' + await token())
          .send(booking({firstname: 'Autorizada'}));
      expect(res.status).to.equal(200);
      expect(res.body.firstname).to.equal('Autorizada');
    });
  });

  describe('D-002 fechas de reserva invertidas', function() {

    it('D-002 rechaza checkout anterior a checkin y no persiste la reserva', async function() {
      const res = await createBooking(booking({bookingdates: {checkin: '2026-09-10', checkout: '2026-09-01'}}));
      expect(res.status).to.be.at.least(400);
      expect(await totalBookings()).to.equal(0);
    });

    it('D-002 rechaza checkout igual a checkin (0 noches)', async function() {
      const res = await createBooking(booking({bookingdates: {checkin: '2026-09-10', checkout: '2026-09-10'}}));
      expect(res.status).to.be.at.least(400);
    });

    it('D-002 rechaza fechas que no son válidas', async function() {
      const res = await createBooking(booking({bookingdates: {checkin: 'no-es-fecha', checkout: '2026-09-10'}}));
      expect(res.status).to.be.at.least(400);
    });

    it('D-002 PUT con fechas invertidas responde 400', async function() {
      await createBooking(booking());
      const res = await request(server).put('/booking/1')
          .set('Cookie', 'token=' + await token())
          .send(booking({bookingdates: {checkin: '2026-12-05', checkout: '2026-12-01'}}));
      expect(res.status).to.equal(400);
    });

    it('D-002 valor límite: una noche (checkout = checkin + 1 día) se acepta', async function() {
      const res = await createBooking(booking({bookingdates: {checkin: '2026-09-10', checkout: '2026-09-11'}}));
      expect(res.status).to.equal(200);
    });
  });

  describe('D-003 totalprice inválido', function() {

    it('D-003 rechaza totalprice negativo', async function() {
      const res = await createBooking(booking({totalprice: -50}));
      expect(res.status).to.be.at.least(400);
      expect(await totalBookings()).to.equal(0);
    });

    it('D-003 rechaza totalprice no numérico en lugar de convertirlo en null', async function() {
      const res = await createBooking(booking({totalprice: 'abc'}));
      expect(res.status).to.be.at.least(400);
      expect(await totalBookings()).to.equal(0);
    });

    it('D-003 valor límite: totalprice 0 se acepta', async function() {
      const res = await createBooking(booking({totalprice: 0}));
      expect(res.status).to.equal(200);
      expect(res.body.booking.totalprice).to.equal(0);
    });
  });

  describe('D-004 reservas solapadas (abierto, P2: pendiente de aclarar el requisito)', function() {

    // Pendiente hasta que exista la entidad habitación (acción A-09). Se activa cambiando it.skip por it.
    it.skip('D-004 una segunda reserva solapada de la misma habitación responde 409', async function() {
      await createBooking(booking({roomid: 1}));
      const res = await createBooking(booking({roomid: 1}));
      expect(res.status).to.equal(409);
    });
  });

  describe('D-005 código de estado al borrar un recurso inexistente', function() {

    it('D-005 DELETE de una reserva inexistente responde 404', async function() {
      const res = await request(server).delete('/booking/10000000').set('Cookie', 'token=' + await token());
      expect(res.status).to.equal(404);
    });
  });
});
