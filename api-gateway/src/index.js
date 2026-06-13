require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const logger = require('./utils/logger')

const { verifyToken } = require('./middleware/auth');

const app = express()
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());

app.use(morgan('combined', {
  stream: { write: message => logger.info(message.trim()) }
}));

app.use(express.json());

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: { error: 'Demasiados requests, espera unos minutos.'}
});

app.use(limiter);

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'api-gateway' });
});

// Ruta pública - no requiere token
app.get('/public', (req, res) => {
  res.json({ mensaje: 'Esta ruta es pública' });
});

// Ruta protegida - requiere token
app.get('/privado', verifyToken, (req, res) => {
  res.json({ mensaje: 'Acceso permitido', usuario: req.user });
});

// Rutas no encontradas
app.use((req, res) => {
  res.status(404).json({ error: 'Ruta no encontrada' });
});

// Errores generales
app.use((err, req, res, next) => {
  logger.error(err.message);
  res.status(500).json({ error: 'Error interno del servidor' });
});

app.listen(PORT, () => {
  logger.info(`API Gateway corriendo en puerto ${PORT}`);
});