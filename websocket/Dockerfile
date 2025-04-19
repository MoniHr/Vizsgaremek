# Node.js alapú Docker image
FROM node:18

# Mappa létrehozása és beállítása a munkakönyvtárként
WORKDIR /app

# Csomagfájlok másolása és függőségek telepítése
COPY package*.json ./
RUN npm install -g pm2 && npm install

# Teljes alkalmazás másolása
COPY . .

# PM2 használatával indítjuk a szervert
CMD ["pm2-runtime", "start", "server.js", "--name", "websocket_server"]
