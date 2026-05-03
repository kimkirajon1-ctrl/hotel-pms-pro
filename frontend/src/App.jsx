import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    // Render'da backend ve frontend aynı URL'de olacağı için relatif link
    axios.get('/api/rooms')
      .then(res => setRooms(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Hotel PMS Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
        {rooms.map(room => (
          <div key={room._id} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '8px' }}>
            <h3>Oda: {room.roomNumber}</h3>
            <p>Tip: {room.type}</p>
            <p>Durum: <strong>{room.status}</strong></p>
            <p>Fiyat: {room.pricePerNight}₺</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
