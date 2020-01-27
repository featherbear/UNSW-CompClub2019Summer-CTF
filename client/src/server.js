import sirv from 'sirv'
import polka from 'polka'
import compression from 'compression'
import * as sapper from '@sapper/server'

// https://stackoverflow.com/a/59500567
import { json } from 'body-parser'
import cookierParser from 'cookie-parser'

const { PORT, NODE_ENV } = process.env
const dev = NODE_ENV === 'development'

import './components/ServerResponse-CookiePolyfill'
import './components/ServerResponse-RedirectPolyfill'

import jwt_decode from 'jwt-decode'

polka()
  .use(
    json(),
    cookierParser(),
    compression({ threshold: 0 }),
    sirv('static', { dev }),
    sapper.middleware({
      session: (req, res) => {
        let data = null

        try {
          data = jwt_decode(req.cookies.token)
          data.token = req.cookies.token
          
          if (data.exp < Date.now() / 1000) {
            data = null
          }
        } catch (e) {
          data = null
        }

        return data
      }
    })
  )
  .listen(PORT, err => {
    if (err) console.log('error', err)
  })
