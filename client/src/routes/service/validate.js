import { call, VALIDATE_LOGIN } from '../../components/CTFAPI.js'

async function validate (req, res) {
  let data = await call(VALIDATE_LOGIN, req.cookies.token).then(r => r.json())
  res.statusCode = data.status ? 200 : 401
  res.end()
}

export async function get (req, res, next) {
  return validate(req, res)
}

export async function post (req, res, next) {
  return validate(req, res)
}
