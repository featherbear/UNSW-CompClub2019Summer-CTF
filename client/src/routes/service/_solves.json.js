import { call, GET_SOLVES } from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  res.end(await call(GET_SOLVES, req.cookies.token).then(r => r.text()))
}
