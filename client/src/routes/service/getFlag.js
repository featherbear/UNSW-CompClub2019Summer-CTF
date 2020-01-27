import { call, GET_QUESTION_FLAG } from '../../components/CTFAPI.js'

export async function post (req, res, next) {
  console.log(req.body)
  let response = await call(
    GET_QUESTION_FLAG,
    req.cookies.token,
    req.body
  ).then(r => r.json())
  res.end(response.data)
}
