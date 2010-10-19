var a = new Array;

a.push('a');
a.push('b');

console.log(a);
console.log(a.length);


console.log('--object-0--');
b = Object();
b.hello = 0;
console.log(b.hello);
console.log(b.hello2);

if (b['hello']) {
	console.log('b.hello');
}

if (b['hello'] != undefined) {
	console.log('b.hello-defined');
}

if (b['hello2']) {
	console.log('b.hello2');
}
