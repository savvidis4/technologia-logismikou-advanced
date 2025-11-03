import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000' // Flask backend URL

export const api = axios.create({
  baseURL: API_URL,
})

// optional helper to set Authorization header
export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}
