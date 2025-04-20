import React from 'react';

function UserFilter({ userId, setUserId, fetch }) {
  return (
    <div>
      <input
        type="text"
        placeholder="Enter User ID"
        value={userId}
        onChange={e => setUserId(e.target.value)}
      />
      <button onClick={fetch}>Get User Data</button>
    </div>
  );
}

export default UserFilter;
