function activate() {
  displayFeedback();

  // Call API with credentials here
  fetch('/api/setup_auth')
  .then(response => response.json())
  .then(displayQR)
  .catch(retrieveFailed);
}

function displayFeedback() {
  const current = document.getElementById('qrcode');
  current.innerHTML = "Retrieving secret key...";
}

function retrieveFailed(e) {
  const current = document.getElementById('qrcode');
  current.innerHTML = `Error! Could not retrieve secret key: ${e}`;
}

function displayQR(response) {
  const current = document.getElementById('qrcode');

  const qrcode = document.createElement('div');
  qrcode.setAttribute('id', 'qrcode');
  new QRCode(qrcode, response);

  current.parentNode.replaceChild(qrcode, current);
}
