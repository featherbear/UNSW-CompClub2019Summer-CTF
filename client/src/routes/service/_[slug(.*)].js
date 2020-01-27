import { callManual, BASE_URL } from '../../components/CTFAPI'

export async function get (req, res, next) {
  res.end(await callManual(`${BASE_URL}${req.params.slug}`, 'GET', req.cookies.token).then(r=>r.text()))
}

export async function post (req, res, next) {
  res.end(await callManual(`${BASE_URL}${req.params.slug}`, 'POST', req.cookies.token, req.body).then(r=>r.text()))
}

export async function put (req, res, next) {
  res.end(await callManual(`${BASE_URL}${req.params.slug}`, 'PUT', req.cookies.token, req.body).then(r=>r.text()))
}

export async function del (req, res, next) {
  res.end(await callManual(`${BASE_URL}${req.params.slug}`, 'DELETE', req.cookies.token, req.body).then(r=>r.text()))
}
