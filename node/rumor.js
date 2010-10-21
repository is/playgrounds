var events = require('events'),
    http = require('http'),
    sys = require('sys'),
    url = require('url'),
		urlparse = require('url').parse,
//		htmlparser = require('htmlparser'),
		BufferList = require('bufferlist').BufferList;

var cllog = console.log
var clinfo = console.log
var _reHref = /<a\s[^>]*href="([^"]+)"|<a\s[^>]*href='([^']+)'/img
var _reHref2 = /href=["'](.*)["']$/i

// ---- Configuration ----
var C = {
	"version": '0.0.1',
	'content.sizelimit': 1024 * 1024 * 4,
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
		this.pathname = ui.pathname;

		if (this.pathname === undefined)
			this.pathname = '/';
		if (this.port === undefined)
			if (this.protocol === 'http:')
				this.port = 80;
			else if (this.protocol === 'https:')
				this.port = 443;
		return this;
	};
	this.parse();
};

// ---- Rumor ----
function Rumor(C) {
	events.EventEmitter.call(this);

	this.conf = C;
	this.entries = new Array;
	this.entriesMap = new Object;

	this.entriesLimit1 = 2500;
	this.entriesLimit2 = 5000;

	this.sites = new Object;
	this.tasks = new Object;

	this.curFetcherId = 0;
	this.curFetchers = 0;
	this.curFetcherLimit = 6000;

	// ----
	this.genFetcherId = function() {
		this.curFetcherId ++;
		return this.curFetcherId;
	};

	// ----
	this.fireFetcher = function(entry) {
		var fetcher = new Fetcher(this, entry);
		this.addFetcher(fetcher);
		fetcher.fire();
		return fetcher;
	};

	this.fireFetchers = function() {
		while (true) {
			if (this.entries.length == 0)
				return;

			if (this.curFetchers >= this.curFetcherLimit) {
				return;
			}

			var ei = this.entries.shift();
			delete this.entriesMap[ei.url];
			if (this.sites[ei.hostname] && this.sites[ei.hostname] > 8)
				continue;

			this.fireFetcher(ei);
		}
	};

	// ----
	this.addEntry = function(entry) {
		if (this.entriesMap[entry.url] !== undefined)
			return;

		this.entriesMap[entry.url] = entry;
		this.entries.push(entry);
	};

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
		else {
			// cllog("[site] " + task.entry.host +  " <= " + task.entry.referer + " | " + this.curFetcherId + " | " + this.entries.length + " | " + this.curFetchers);
			sites[task.entry.host] = 1;
		}

		task.registered = true;
	};

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
	};

	this.onFetcherFinished = function(fetcher) {
		this.planner.onFetcherFinished(fetcher);
	};

	// ----
	this.version = function() {
		return C.version;
	};

	this.tagline = function() { 
		clinfo("Rumor -- " + this.version());
	};
};
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
		this.co.on('error', function(exception) {
			self.clear();
			self.co.destroy();
		});

		var headers = {};
		headers.host = this.entry.host;
		headers.agent = 'rumor-' + this.rumor.version();

		if (this.entry.referer)
			headers.referer = this.entry.referer;

		this.request = this.co.request('GET', this.entry.pathname, headers);
		this.request.on('response', function(response) { 
			self.onResponse(response);
		});
		this.request.on('error', function(exception) { 
			self.onRequestError(exception)
		});
		this.request.end();
	};

	this.onResponse = function(response) {
		var self = this;
		this.response = response;
		this.retCode = response.statusCode;

		if (this.retCode != 200) {
			this.finished();
			return;
		}

		this.content = new BufferList;
		response.on('data', function(chunk) { self.onResponseData(chunk); }).
			on('error', function(exception) { self.onResponseError(exception); }).
			on('end', function() { self.onResponseEnd(); });
	};

	this.onResponseData = function(chunk) {
		this.content.push(chunk);
		if (this.contentSizeLimit) {
			if (this.content.length > this.contentSizeLimit) {
				this.onResponseError('too-big-contents');
			}
		}
	};

	this.onRequestError = function(error) {
		this.clear();
		this.co.destroy();
	};

	this.onResponseError = function(error) {
		this.clear();
		this.response.client.destroy();
	};

	this.onResponseEnd = function() {
		this.finished();
	};

	this.clear = function() {
		this.rumor.removeFetcher(this);
	};

	this.finished = function() {
		this.clear();
		this.rumor.onFetcherFinished(this);
	};
};

// ---- 
function Planner(rumor) {
	this.rumor = rumor;
	this.onFetcherFinished = function(fetcher) {
		var retCode = fetcher.retCode;
		if (retCode == 301 || retCode == 302 || retCode == 307) {
			this.onRedirect(fetcher);
			return;
		}

		if (retCode == 200) {
			this.onContent(fetcher);
			return;
		}
		
		// cllog("[" + fetcher.retCode + "] " + fetcher.entry.url);
		return;
	};

	this.onContent = function(fetcher) {
		if (!fetcher.content && !fetcher.content.length) {
			// cllog("[200] " + fetcher.entry.url + " {empty}");
			return;
		}

		var contentType = fetcher.response.headers['content-type'];
		var contentLength = fetcher.response.headers['content-length'];

		if (!contentType)
			contentType = "-";

		if (!contentLength)
			contentLength = fetcher.content.length;

		// if (fetcher.entry.referer)
		//	if (fetcher.entry.host !== urlparse(fetcher.entry.referer).host)
		//		cllog(" vvv  " + fetcher.entry.referer);
	
		var accu = rumor.entries.length;
		if (accu >= rumor.entriesLimit2) {
			// cllog("[200] " + fetcher.entry.url + " === " + contentType + ":" + contentLength + " | " + rumor.curFetcherId + " | " + rumor.entries.length + " | " + rumor.curFetchers);
			return;
		}

		var self = this;

		/*
		var handler = new htmlparser.DefaultHandler();
		var parser = new htmlparser.Parser(handler);
		try {
			parser.parseComplete(fetcher.content);
		} catch(e) {
			return;
		}
		
		linktags = htmlparser.DomUtils.getElementsByTagName('a', handler.dom);
		*/

		var entries = [];
		var entriesMap = {};

		var linktags = fetcher.content.toString().match(_reHref);
		if (linktags) {
			for (var i = 0; i < linktags.length; i++) {
				var res = _reHref2.exec(linktags[i]);
				if (!res)
					continue;
				var u = url.resolve(fetcher.entry.url, res[1]);
				var e = new Entry(u, fetcher.entry.url);
				if (e.protocol === 'http:') {
					if (!entriesMap[u]) {
						entries.push(e);
						entriesMap[u] = 1;
					}
				}
			}
		}

		/*
		for (var i = 0; i < linktags.length; i++) {
			var l = linktags[i];
			if (!l.attribs || !l.attribs.href)
				continue;
			href = l.attribs.href;
			var u = url.resolve(fetcher.entry.url, href);
			var e = new Entry(u, fetcher.entry.url);
			if (e.protocol === 'http:') {
				if (!entriesMap[u]) {
					entries.push(e);
					entriesMap[u] = 1;
				}
			}
		}
		*/

		var added = entries.length
		if (accu >= rumor.entriesLimit1 && added > 30) {
			added = 15;
		}

		var swapper = function(a, L, e) {
			var r = Math.floor(Math.random() * L);
			var x = a[e];
			a[e] = a[r];
			a[r] = a[e];
		};

		for (var i = 0, L = entries.length; i < added; i++)
			swapper(entries, L, i);

		for (var i = 0; i < added; i++) {
			if (entries[i].protocol === "http:")
				rumor.addEntry(entries[i]);
		}

		// cllog("[200] " + fetcher.entry.url + " === " + contentType + ":" + contentLength + " | " + added + " links | " + rumor.curFetcherId + " | " + rumor.entries.length + " | " + rumor.curFetchers);
		rumor.fireFetchers();
	};

	this.onRedirect = function(fetcher) {
		var redirectURL = fetcher.response.headers['location'];
		if (!redirectURL)
			return;

		redirectURL = url.resolve(fetcher.entry.url, redirectURL);
		// cllog("[" + fetcher.retCode + "] " + fetcher.entry.url + " -> " + redirectURL);
		this.addEntry(redirectURL, fetcher.referer, true);
	};


	this.addEntry = function(url, referer, fire) {
		var e = new Entry(url, referer);
		if (e.protocol === 'http:') {
			rumor.addEntry(e);
		}
		if (fire) {
			rumor.fireFetchers();
		}
	};
}

// ---- Main ----
function main() {
/*
	cl.setInfoPrefix(' = ');
	cl.setLogPrefix(' . ');
	cl.setErrorPrefix(' ! ');
	cl.setWarnPrefix(' + ');

	cl.setLogColor('BLUE');
	cl.setInfoColor('MAGENTA');
	cl.setErrorColor('RED');
	cl.setWarnColor('RED');
*/
	var r = new Rumor(C);
	r.planner = new Planner(r);
	r.tagline();
	var ei = new Entry('http://github.com/');
	r.fireFetcher(ei);
}

main();


process.on('exit', function() {
	console.log('--- END ---');
});

process.on('uncaughtException', function(err) {
	console.log('--- EXCEPTION --- ' + err);
});

/*
process.on('SIGINT', function() {
	console.log('--- Got SIGINT. Press Control-D to exit.');
});
*/
