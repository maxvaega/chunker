import { api } from '../../services/api'

describe('API Service', () => {
  test('sets auth token in headers', () => {
    const token = 'test-token'
    api.setToken(token)
    expect(api.defaults.headers.common['Authorization']).toBe(`Bearer ${token}`)
  })

  test('clears auth token', () => {
    api.clearToken()
    expect(api.defaults.headers.common['Authorization']).toBeUndefined()
  })

  test('handles API errors', async () => {
    try {
      await api.post('/invalid-endpoint')
    } catch (error) {
      expect(error.response.status).toBe(404)
    }
  })
})