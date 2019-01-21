const fetch = require('node-fetch');

function *G() {
  const uri = 'http://jsonplaceholder.typicode.com/posts/1';
  const response = yield fetch(uri);
  const post = yield response.json();
  console.log(post);
};

function run(generator) {
  const iterator = generator();
  const iteration = iterator.next();
  const promise = iteration.value
  promise.then( x => {
    const anotherIterator = iterator.next(x);
    const anotherPromise = anotherIterator.value;
    anotherPromise.then(y => iterator.next(y));
  });
}
const g = G();
v = g.next();
console.log(v);