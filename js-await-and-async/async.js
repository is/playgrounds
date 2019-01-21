const fetch = require('node-fetch');
async function fetchAvatarUrl(userId) {
  console.log("l1");
  const response = await fetch(`https://catappapi.herokuapp.com/users/${userId}`)
  console.log("l2");
  const data = await response.json();
  console.log("l3");
  return data.imageUrl;
}

const result = fetchAvatarUrl(123);
result.then(data => {
  console.log(data);
});

