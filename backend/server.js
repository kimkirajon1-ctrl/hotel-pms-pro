const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB Bağlantısı (Hata kontrolü eklendi)
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("✅ MongoDB Bağlantısı Başarılı"))
  .catch(err => console.error("❌ MongoDB Hatası:", err));

// Örnek API Endpoint
app.get('/api/status', (req, res) => {
  res.json({ message: "Sistem Aktif" });
});

// --- RENDER DEPLOYMENT AYARI ---
// Frontend 'dist' klasörünü statik olarak sun
const __frontendPath = path.join(__dirname, '../frontend/dist');
app.use(express.static(__frontendPath));

// API dışındaki tüm istekleri React'e (index.html) yönlendir
app.get('*', (req, res) => {
  res.sendFile(path.join(__frontendPath, 'index.html'));
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server ${PORT} portunda çalışıyor`));
