import { call, GET_QUESTIONS } from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  res.end(await call(GET_QUESTIONS, req.cookies.token).then(r => r.text()))
}
