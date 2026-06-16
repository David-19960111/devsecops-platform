const request = require('supertest');
const app = require('../src/index');

describe('API Gateway', () => {
  it('GET /health devuelve status ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  it('GET /ruta-inexistente devuelve 404', async () => {
    const res = await request(app).get('/ruta-inexistente');
    expect(res.statusCode).toBe(404);
  });
});