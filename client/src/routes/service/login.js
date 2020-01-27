import { call, LOGIN } from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  res.redirect(301, '/invite')
  res.end()
}

export async function post (req, res, next) {
  let resp = await call(LOGIN, undefined, req.body).then(r => r.json())

  if (!resp.status) {
    res.statusCode = 401
    res.end()
    return
  }

  res.cookie('token', resp.data.token, {
    path: '/'
  })
  res.statusCode = 200
  res.end()
}
