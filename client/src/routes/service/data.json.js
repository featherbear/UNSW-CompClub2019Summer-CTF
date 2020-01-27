import {
  call,
  GET_QUESTIONS,
  GET_CATEGORIES,
  GET_SOLVES
} from '../../components/CTFAPI.js'

export async function get (req, res, next) {
  let token = req.cookies.token

  const questionsFn = () =>
    call(GET_QUESTIONS, token)
      .then(r => r.json())
      .then(json => json.data)

  const categoriesFn = () =>
    call(GET_CATEGORIES, token)
      .then(r => r.json())
      .then(json => json.data)

  const solvesFn = () =>
    call(GET_SOLVES, token)
      .then(r => r.json())
      .then(json => json.data)

  let [questions, categories, solves] = await Promise.all([
    questionsFn(),
    categoriesFn(),
    solvesFn()
  ])

  res.end(
    JSON.stringify(
      questions.map(question => {
        let [id, title, description, points, categoryID] = question
        return {
          id,
          title,
          description,
          points,
          categoryID,
          categoryName: categories[categoryID] || '',
          solves: solves[id] || 0
        }
      })
    )
  )
}
