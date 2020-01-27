import { call, LOGIN } from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  res.redirect(301, '/invite')
  res.end()
}

export async function post (req, res, next) {
  let resp = await call(LOGIN, undefined, req.body)

  if (resp.status) {
    res.cookie('token', resp.data.token)
    res.redirect('/')
    res.end()
  }

  res.statusCode = 400
  res.end()
}
