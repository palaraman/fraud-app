import React from 'react';

function GPSStatus({ blocked }) {
  return (
    <div style={{ color: blocked ? 'red' : 'green' }}>
      GPS Status: {blocked ? "Blocked" : "Active"}
    </div>
  );
}

export default GPSStatus;
