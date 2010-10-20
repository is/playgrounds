var events = require('events'),
    http = require('http'),
    sys = require('sys'),
    url = require('url'),
		urlparse = require('url').parse,
		BufferList = require('bufferlist').BufferList;

// ---- Configuration ----
var C = {
	"version": '0.0.1',
	'content.sizelimit': 1024 * 1024 * 10,
};

// ---- Entry ----
function Entry(url, referer) {
	this.url = url;
	this.referer = referer;

	this.parse = function() {
		if (!this.url)
			return this;
	
		var ui = urlparse(this.url);
		this.host = ui.host;
		this.port = ui.port;
		this.hostname = ui.hostname;
		this.protocol = ui.protocol;
		this.path = ui.path;

		if (this.path === undefined)
			this.path = '/';
		if (this.port === undefined)
			this.port = 80;
		return this;
	}
	this.parse();
}

// ---- Rumor ----
function Rumor(C) {
	events.EventEmitter.call(this);

	this.conf = C;
	this.entries = new Array;
	this.sites = new Object;
	this.tasks = new Object;

	this.curFetcherId = 0;
	this.curFetchers = 0;
	this.curFetcherLimit = 10000;

	// ----
	this.genFetcherId = function() {
		this.curFetcherId ++;
		return this.curFetcherId;
	}

	// ----
	this.fireFetcher = function(entry) {
		var fetcher = new Fetcher(this, entry);
		this.addFetcher(fetcher);
		fetcher.fire();
		return fetcher;
	}

	// ----
	this.addFetcher = function(task) {
		if (task.registered)
			return;

		this.curFetchers ++;
		this.tasks[task.id] = task;

		// Add to sites map
		var sites = this.sites;
		if (sites[task.entry.host] != undefined)
			sites[task.entry.host] += 1;
		else
			sites[task.entry.host] = 1;

		task.registered = true;
	}

	// ----
	this.removeFetcher = function(task) {
		if (!task.registered)
			return;

		this.curFetchers --;
		delete this.tasks[task.id];

		// Remove from sites
		var sites = this.sites;
		if (sites[task.entry.host] != undefined) {
			sites[task.entry.host] -= 1;
			if (sites[task.entry.host] <= 0)
				delete sites[task.entry.host];
		}
			
		task.registered = false;
	}

	this.onFetcherFinished = function(fetcher) {
		// console.log('Fetcher Finished');
		// console.log(fetcher.retCode);
		if (fetcher.content == undefined) {
			console.log("   fetched " + fetcher.entry.url + " (" + fetcher.retCode + ")");
		} else {
			console.log(fetcher.content.length);
		}
	}

	// ----
	this.version = function() {
		return C.version;
	}

	this.tagline = function() { 
		console.log(" = Rumor -- " + this.version());
	}
}
sys.inherits(Rumor, events.EventEmitter);

// ---- Fetcher ----
function Fetcher(R, ei) {
	this.rumor = R;
	this.entry = ei;
	this.id = R.genFetcherId();
	this.registered = false;

	if (this.entry.contentSizeLimit)
		this.contentSizeLimit = this.entry.contentSizeLimit;
	else
		this.contentSizeLimit = this.rumor.conf['content.sizelimit'];

	this.fire = function() {
		var self = this;
		this.co = http.createClient(this.entry.port, this.entry.hostname);
		var headers = {};
		headers.host = this.entry.host;

		if (this.entry.referer)
			headers.referer = this.entry.referer;

		this.request = this.co.request('GET', this.entry.path, headers);
		this.request.on('response', function(response) { 
			self.onResponse(response);
		});
		this.request.on('error', function(exception) { 
			self.onRequestError(exception)
		});
		this.request.end();
	}

	this.onResponse = function(response) {
		var self = this;
		this.response = response;
		this.retCode = response.statusCode;
		this.resHeaders = response.headers;

		if (this.retCode != 200) {
			this.finished();
			return;
		}

		this.content = new BufferList;
		response.on('data', function(chunk) { self.onResponseData(chunk); }).
			on('error', function(exception) { self.onResponseError(exception); }).
			on('end', function() { self.onResponseEnd(); });
	}

	this.onResponseData = function(chunk) {
		this.content.push(chunk);
		if (this.contentSizeLimit) {
			if (this.content.length > this.contentSizeLimit) {
				this.onResponseError('too-big-contents');
			}
		}
	}

	this.onRequestError = function(error) {
		this.clear();
		this.co.destroy();
	}

	this.onResponseError = function(error) {
		this.clear();
		this.response.client.destroy();
	}

	this.onResponseEnd = function() {
		this.finished();
	}

	this.clear = function() {
		this.rumor.removeFetcher(this);
	}

	this.finished = function() {
		this.clear();
		this.rumor.onFetcherFinished(this);
	}
}


// ---- Main ----
var r = new Rumor(C);
r.tagline();
var ei = new Entry('http://www.sun.com/');
r.fireFetcher(ei);
