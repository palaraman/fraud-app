import React from 'react';

function TransactionTable({ data }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Amount</th>
          <th>Location</th>
          <th>Confidence</th>
          <th>Fraud?</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {data.map((t, idx) => (
          <tr key={idx}>
            <td>{t.amount}</td>
            <td>{t.location}</td>
            <td>{t.confidence}</td>
            <td>{t.is_fraud ? "Yes" : "No"}</td>
            <td>{t.timestamp}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TransactionTable;
