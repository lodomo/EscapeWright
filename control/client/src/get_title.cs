// File: readRoomInfo.js
const fs = require('fs');
const path = require('path');

function getRoomName() {
  const filePath = path.join(__dirname, '../roominfo.ew');
  const fileContent = fs.readFileSync(filePath, 'utf-8');

  // Extract the room name using regex
  const roomName = fileContent.match(^RoomName:(.*)$)[1];
  
  return roomName || 'Unknown Room';
}

module.exports = { getRoomName };
