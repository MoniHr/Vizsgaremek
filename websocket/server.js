const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const Redis = require("ioredis");

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: "*" },
  transports: ["websocket"],
});

const redisClient = new Redis({ host: "redis", port: 6379 });

let chatRooms = {}; // Szobák nyilvántartása
let messages = {}; // Üzenetek tárolása memóriában

// ✅ Felhasználó csatlakozik a szerverhez
io.on("connection", (socket) => {
  console.log(`✅ User connected: ${socket.id}`);

  // 🏠 Felhasználó belép egy szobába
  socket.on("joinRoom", (data) => {
    const { chat_room, user_email } = data;
    socket.join(chat_room);

    if (!chatRooms[chat_room]) {
      chatRooms[chat_room] = [];
    }
    if (!chatRooms[chat_room].includes(user_email)) {
      chatRooms[chat_room].push(user_email);
    }

    console.log(`📩 ${user_email} joined room: ${chat_room}`);
  });

  // 💬 Üzenet küldése (Django kezeli a mentést, csak továbbítjuk)
  socket.on("sendMessage", (data) => {
    const { chat_room, sender, message } = data;

    const messageData = {
      sender: sender,
      message: message,
      timestamp: new Date().toISOString(),
    };

    io.to(chat_room).emit("message", messageData);
  });

  // 📝 Valaki gépel
  socket.on("typing", (data) => {
    const { chat_room, sender } = data;
    io.to(chat_room).emit("typing", { sender: sender });
  });

  // ⏹️ Valaki abbahagyta a gépelést
  socket.on("stopTyping", (data) => {
    const { chat_room, sender } = data;
    io.to(chat_room).emit("stopTyping", { sender: sender });
  });

  // ✅ Üzenetek lekérése
  socket.on("getMessages", (chat_room) => {
    const chatHistory = messages[chat_room] || [];
    socket.emit("chat", chatHistory);
  });

  // 👀 Üzenetek olvasottá tétele
  socket.on("mark_messages_read", (data) => {
    const { chat_room, sender } = data;
    io.to(chat_room).emit("messageSeen", { sender: sender });
  });

  // 👀 Üzenet olvasva esemény
  socket.on("message_seen", (data) => {
    console.log(`👀 Üzenet olvasva szobában: ${data.chat_room}`);
    io.to(data.chat_room).emit("messageSeen", { user: data.user });
  });

  // ❌ Amikor a felhasználó kilép
  socket.on("disconnect", () => {
    console.log(`❌ User disconnected: ${socket.id}`);
  });
});

// 🔥 Redis csatorna figyelése a Celery által mentett üzenetekhez
redisClient.subscribe("chat_messages");

redisClient.on("message", (channel, message) => {
  if (channel === "chat_messages") {
    const messageData = JSON.parse(message);
    console.log(
      `🔥 WebSocket: Új üzenet érkezett a szobába ${messageData.chat_room}`
    );

    // 🔄 A megfelelő szobába küldjük az új üzenetet
    io.to(messageData.chat_room).emit("message", messageData);

    // 🔄 Chat lista frissítése az összes felhasználónak
    io.emit("chat_list_update", {
      chat_room: messageData.chat_room,
      last_message_time: messageData.timestamp,
      last_message: messageData.message,
      other_user: messageData.sender,
      unread_count: 1,
    });
  }
});

redisClient.subscribe("chat_unread_count");

redisClient.on("message", (channel, message) => {
  if (channel === "chat_unread_count") {
    const data = JSON.parse(message);
    console.log(`📬 Olvasatlan üzenet számláló frissült: ${data.user} - ${data.unread_count}`);

    // Küldjük az adott kliensnek target user_email alapján
    io.emit(`unread_count_${data.user}`, {
      unread_count: data.unread_count,
    });
  }
});



// 🚀 Szerver indítása
server.listen(3001, "0.0.0.0", () => {
  console.log(
    "🚀 WebSocket server running on port 3001 (ONLY WebSocket, no polling!)"
  );
});
