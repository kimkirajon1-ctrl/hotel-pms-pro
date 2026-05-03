const mongoose = require('mongoose');

const RoomSchema = new mongoose.Schema({
  roomNumber: String,
  type: { type: String, enum: ["Single", "Double", "Suite"] },
  status: { type: String, default: "Available" },
  pricePerNight: Number
});

const BookingSchema = new mongoose.Schema({
  room: { type: mongoose.Schema.Types.ObjectId, ref: 'Room' },
  guestName: String,
  checkIn: Date,
  checkOut: Date,
  status: { type: String, default: "Confirmed" }
});

const Room = mongoose.model('Room', RoomSchema);
const Booking = mongoose.model('Booking', BookingSchema);

module.exports = { Room, Booking };
