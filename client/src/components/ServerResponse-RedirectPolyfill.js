// # Probably a bad idea, but we'll do it anyway
// ServerResponse .redirect polyfill - because we're using Polka and not Express

import http from 'http'
import { isNumber } from 'util'

if (!http.ServerResponse.prototype.redirect) {
  http.ServerResponse.prototype.redirect = function (code, url) {
    if (typeof url === 'undefined' && !isNumber(code)) {
      // No code given, so set code to 302, and url to the contents of code
      url = code
      code = 302
    }

    this.statusCode = code
    this.setHeader('Location', url)

    return this
  }
}

export default {}
