var events = require('events'),
    fs = require('fs'),
    http = require('http'),
    sys = require('sys'),
    url = require('url'),
    urlparse = require('url').parse,
    log = require('log'),
    sprintf = require('./sprintf-0.6').sprintf
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

var slog = new log(log.INFO, fs.createWriteStream('sites.log'));
var ulog = new log(log.INFO, fs.createWriteStream('urls.log'));
var clog = new log(log.INFO);

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
	this.curFetcherLimit = 250;

	this.curFinished = 0;
	this.curFinishedContent = 0;

	this.tickCount = 0;

	this.tick10S = function(self) {
		self.tickCount += 1;
		clog.info(sprintf("T:%d I:%d, CF:%d, EI:%d, FS:%d, FB:%.1fm", 
			self.tickCount, self.curFetcherId, self.curFetchers, 
			self.entries.length, self.curFinished, self.curFinishedContent / 1048576.0));

		//clog.info("C:" + self.curFetcherId + " S:" + self.curFetchers + " ES:" + self.entries.length + " FS:" + self.curFinished + " FB:" + self.curFinishedContent);
		self.curFinished = 0;
		self.curFinishedContent = 0;
		self.fireFetchers();
	}

	this.tick10STimerId = setInterval(this.tick10S, 10000, this);

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
			slog.info(task.entry.host + " == " + task.entry.referer);
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
		this.curFinished ++;
		if (fetcher.content)
			this.curFinishedContent += fetcher.content.length;
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
	this.beginTick = this.rumor.tickCount;
	this.registered = false;

	if (this.entry.contentSizeLimit)
		this.contentSizeLimit = this.entry.contentSizeLimit;
	else
		this.contentSizeLimit = this.rumor.conf['content.sizelimit'];

	this.fire = function() {
		var self = this;
		this.co = http.createClient(this.entry.port, this.entry.hostname);
		this.co.setTimeout(30 * 1000);

		this.co.on('error', function(exception) {
			self.clear();
			self.co.destroy();
		});

		var headers = {};
		headers.host = this.entry.host;
		headers.agent = 'rumor-' + this.rumor.version() + " http://github.com/is/Demos/blob/master/node/rumor.js";

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
		if (!fetcher.entry.referer)
			fetcher.entry.referer = "{empty}"

		var retCode = fetcher.retCode;
		if (retCode == 301 || retCode == 302 || retCode == 307) {
			this.onRedirect(fetcher);
			return;
		}

		if (retCode == 200) {
			this.onContent(fetcher);
			return;
		}
		
		ulog.info("[" + fetcher.retCode + "] " + fetcher.entry.url + " == " + fetcher.entry.referer);
		return;
	};

	this.onContent = function(fetcher) {
		if (!fetcher.content && !fetcher.content.length) {
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
		ulog.info("[200] " + fetcher.entry.url + " == " + fetcher.entry.referer + " {" + contentLength + ":"+ contentType + "} <" + fetcher.id + "/" + (this.rumor.tickCount - fetcher.beginTick) + ">");
		if (accu >= rumor.entriesLimit2) {
			return;
		}

		if (contentType.search("text/html") == -1)
			return;

		var self = this;

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
		var handler = new htmlparser.DefaultHandler();
		var parser = new htmlparser.Parser(handler);
		try {
			parser.parseComplete(fetcher.content);
		} catch(e) {
			return;
		}
		
		linktags = htmlparser.DomUtils.getElementsByTagName('a', handler.dom);
	
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

		rumor.fireFetchers();
	};

	this.onRedirect = function(fetcher) {
		var redirectURL = fetcher.response.headers['location'];
		if (!redirectURL)
			return;

		redirectURL = url.resolve(fetcher.entry.url, redirectURL);
		// cllog("[" + fetcher.retCode + "] " + fetcher.entry.url + " -> " + redirectURL);
		this.addEntry(redirectURL, fetcher.entry.referer, true);
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
	console.log(err);
});

/*
process.on('SIGINT', function() {
	console.log('--- Got SIGINT. Press Control-D to exit.');
});
*/
