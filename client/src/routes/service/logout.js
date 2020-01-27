import { call, LOGOUT } from '../../components/CTFAPI.js'

const logout = async function (req, res) {
  call(LOGOUT, req.cookies.token, req.body)

  res.cookie('token', '', {
    path: "/"
  })
  res.redirect(302, '/invite')
  res.end()
}

export async function post (req, res, next) {
  logout(req, res)
}

export async function get (req, res, next) {
  logout(req, res)
}
