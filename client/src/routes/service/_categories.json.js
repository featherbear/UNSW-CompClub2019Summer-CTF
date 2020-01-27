import { call, GET_CATEGORIES } from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  res.end(await call(GET_CATEGORIES, req.cookies.token).then(r => r.text()))
}
