import { auth } from '../../utils/auth'

describe('Auth Utilities', () => {
  test('stores token in localStorage', () => {
    auth.setToken('test-token')
    expect(localStorage.getItem('token')).toBe('test-token')
  })

  test('retrieves token from localStorage', () => {
    localStorage.setItem('token', 'test-token')
    expect(auth.getToken()).toBe('test-token')
  })

  test('clears token on logout', () => {
    localStorage.setItem('token', 'test-token')
    auth.logout()
    expect(localStorage.getItem('token')).toBeNull()
  })
})