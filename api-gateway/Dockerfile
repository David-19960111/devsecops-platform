#---Etapa 1: Construccion
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production 

#--Etapa 2: Produccion
FROM node:20-alpine AS production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup 
WORKDIR /app 
COPY --from=builder /app/node_modules ./node_modules
COPY src/ ./src/
COPY package.json ./
USER appuser 
EXPOSE 3000
CMD [ "node", "src/index.js" ]