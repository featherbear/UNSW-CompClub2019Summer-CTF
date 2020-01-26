const ADDRESS = 'http://localhost:8000'
const API_VERSION = 'v2'

const fetch = require('node-fetch')

const call = function (endpoint, data = {}) {
  return fetch(endpoint[1], {
    method: endpoint[0],
    body: JSON.stringify(data)
  }).then(r => r.json())
}

const craftURL = function (endpoint) {
  return `${ADDRESS}/api/${API_VERSION}/${endpoint}`
}

module.exports = {
  call,

  SOLVE_QUESTION: ['POST', craftURL('question/solve')],
  GET_SCORES: ['GET', craftURL('scores.json')],
  GET_SOLVES: ['GET', craftURL('solves.json')],

  GET_USERS: ['GET', craftURL('auth')],
  CREATE_USER: ['POST', craftURL('auth')],
  DELETE_USER: ['DELETE', craftURL('auth')],
  LOGIN: ['POST', craftURL('auth/login')],
  LOGOUT: ['POST', craftURL('auth/logout')],
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
