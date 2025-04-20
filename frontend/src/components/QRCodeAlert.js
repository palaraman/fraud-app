import React from 'react';
import QRCode from 'qrcode.react';

function QRCodeAlert({ userId }) {
  const url = `https://dashboard.fraudapp.com/user/${userId}`;

  return (
    <div>
      <h4>QR Code Alert</h4>
      <QRCode value={url} />
    </div>
  );
}

export default QRCodeAlert;
