// # Probably a bad idea, but we'll do it anyway
// ServerResponse .cookie polyfill - because we're using Polka and not Express

import http from 'http'
import cookie from 'cookie'

if (!http.ServerResponse.prototype.cookie) {
  http.ServerResponse.prototype.cookie = function (name, value, options) {
    this.setHeader('Set-Cookie', [
      ...(this.getHeader('Set-Cookie') || []),
      cookie.serialize(name, value, options)
    ])

    return this
  }
}

export default {}
