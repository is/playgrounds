const ProxyList = require('free-proxy')
const proxyList = new ProxyList()

async function main() {
  proxies = await proxyList.get()
  console.log(proxies)
}

main()