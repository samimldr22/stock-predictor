// Health check
fetch('/predict?ticker=check')
  .then(() => {
    document.getElementById('health-badge').textContent = 'API Online';
  })
  .catch(() => {
    document.getElementById('health-badge').textContent = 'API Offline';
    document.getElementById('health-badge').style.color = '#f87171';
  });

// Form submit
document.getElementById('predict-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const ticker = 'AAPL';
  const btn = document.getElementById('predict-btn');
  const btnText = btn.querySelector('.btn-text');
  const btnSpinner = btn.querySelector('.btn-spinner');
  const resultPanel = document.getElementById('result-panel');
  const errorPanel = document.getElementById('error-panel');

  btn.disabled = true;
  btnText.textContent = 'Predicting...';
  btnSpinner.classList.remove('hidden');
  resultPanel.classList.add('hidden');
  errorPanel.classList.add('hidden');

  try {
    const res = await fetch(`/predict?ticker=${ticker}`);
    const data = await res.json();

    if (data.status === 'success') {
      document.getElementById('result-value').textContent = '$' + data.predicted_price;
      document.getElementById('result-meta').textContent = ticker + ' · USD · Next Trading Day Estimate';
      resultPanel.classList.remove('hidden');
    } else {
      document.getElementById('error-msg').textContent = data.message;
      errorPanel.classList.remove('hidden');
    }
  } catch (err) {
    document.getElementById('error-msg').textContent = 'Could not connect to server.';
    errorPanel.classList.remove('hidden');
  }

  btn.disabled = false;
  btnText.textContent = 'Predict Close Price';
  btnSpinner.classList.add('hidden');
});