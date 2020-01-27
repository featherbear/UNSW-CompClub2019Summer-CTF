const ADDRESS = 'http://localhost:8000'
const API_VERSION = 'v2'

const BASE_URL = `${ADDRESS}/api/${API_VERSION}/`

const fetch = require('node-fetch')

const call = function (endpoint, token, data) {
  return callManual(endpoint[1], endpoint[0], token, data)
}

const callManual = function (endpoint, method, token, data = {}) {
  return fetch(endpoint, {
    method: method,
    body: Object.keys(data).length ? JSON.stringify(data) : undefined,
    headers: token
      ? {
          Authorization: `Bearer ${token}`
        }
      : undefined
  })
}

const craftURL = function (endpoint) {
  return `${BASE_URL}${endpoint}`
}

module.exports = {
  ADDRESS,
  API_VERSION,
  BASE_URL,

  call,
  callManual,

  SOLVE_QUESTION: ['POST', craftURL('question/solve')],
  GET_SCORES: ['GET', craftURL('scores.json')],
  GET_SOLVES: ['GET', craftURL('solves.json')],

  GET_USERS: ['GET', craftURL('auth')],
  CREATE_USER: ['POST', craftURL('auth')],
  DELETE_USER: ['DELETE', craftURL('auth')],
  LOGIN: ['POST', craftURL('auth/login')],
  LOGOUT: ['POST', craftURL('auth/logout')],
  VALIDATE_LOGIN: ["POST", craftURL('auth/validate')],
  USERNAME_AVAILABE: ['POST', craftURL('auth/usernameAvailable')],
  CHANGE_PASSWORD: ['PUT', craftURL('auth')],
  // CHANGE_DISPLAY_NAME: ["PUT", craftURL("auth")],

  GET_CATEGORIES: ['GET', craftURL('categories.json')],
  CREATE_CATEGORY: ['POST', craftURL('category')],
  UPDATE_CATEGORY: ['PUT', craftURL('category')],
  DELETE_CATEGORY: ['DELETE', craftURL('category')],

  GET_QUESTIONS: ['GET', craftURL('questions.json')],
  GET_QUESTION_FLAG: ['POST', craftURL('question/getFlag')],
  CREATE_QUESTION: ['POST', craftURL('question')],
  UPDATE_QUESTION: ['PUT', craftURL('question')],
  DELETE_QUESTION: ['DELETE', craftURL('question')]
}
