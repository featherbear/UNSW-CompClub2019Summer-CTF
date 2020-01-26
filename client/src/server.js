import sirv from 'sirv'
import polka from 'polka'
import compression from 'compression'
import * as sapper from '@sapper/server'

// https://stackoverflow.com/a/59500567
import { json } from 'body-parser'
import cookierParser from 'cookie-parser'

const { PORT, NODE_ENV } = process.env
const dev = NODE_ENV === 'development'

import "./components/ServerResponse-CookiePolyfill"

polka()
  .use(
    json(),
    cookierParser(),
    compression({ threshold: 0 }),
    sirv('static', { dev }),
    sapper.middleware()
  )
  .listen(PORT, err => {
    if (err) console.log('error', err)
  })
