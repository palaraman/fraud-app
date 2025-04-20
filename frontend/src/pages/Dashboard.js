import React, { useState, useEffect } from 'react';
import UserFilter from '../components/UserFilter';
import TransactionTable from '../components/TransactionTable';
import GPSStatus from '../components/GPSStatus';
import QRCodeAlert from '../components/QRCodeAlert';
import ReCAPTCHA from 'react-google-recaptcha';
import axios from 'axios';

function Dashboard() {
  const [userId, setUserId] = useState('');
  const [transactions, setTransactions] = useState([]);
  const [fraud, setFraud] = useState(null);
  const [captchaToken, setCaptchaToken] = useState('');

  const fetchTransactions = async () => {
    if (!userId) return;
    const res = await axios.get(`http://localhost:5000/transactions/${userId}`);
    setTransactions(res.data);
  };

  const handleSubmit = async () => {
    const data = {
      user_id: userId,
      features: [0.5, 0.6, 0.1], // example input
      amount: 120.55,
      location: "New York",
      captcha_token: captchaToken
    };
    const res = await axios.post("http://localhost:5000/predict", data);
    setFraud(res.data);
    fetchTransactions();
  };

  return (
    <div>
      <h1>Credit Card Fraud Detection Dashboard</h1>
      <UserFilter userId={userId} setUserId={setUserId} fetch={fetchTransactions} />
      <ReCAPTCHA sitekey="YOUR_RECAPTCHA_SITE_KEY" onChange={setCaptchaToken} />
      <button onClick={handleSubmit}>Submit Prediction</button>
      {fraud && (
        <div>
          <p>Fraud: {fraud.fraud ? "Yes" : "No"} | Confidence: {fraud.confidence}</p>
        </div>
      )}
      <TransactionTable data={transactions} />
      <GPSStatus blocked={fraud?.fraud} />
      <QRCodeAlert userId={userId} />
    </div>
  );
}

export default Dashboard;
