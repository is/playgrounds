const fetch = require('node-fetch');
function fetchAvatarUrl(userId) {
  return fetch(`https://catappapi.herokuapp.com/users/${userId}`)
    .then(response => response.json())
    .then(data => data.imageUrl);
}

const result = fetchAvatarUrl(123);

result.then(data => {
  console.log(data);
});