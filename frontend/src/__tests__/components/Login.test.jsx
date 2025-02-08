import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Login } from '../../components/Login'
import { rest } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  rest.post('/auth/login', (req, res, ctx) => {
    const { username, password } = req.body
    if (username === 'admin' && password === 'password') {
      return res(ctx.json({ token: 'fake-token' }))
    }
    return res(ctx.status(401))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Login Component', () => {
  test('renders login form', () => {
    render(<Login />)
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
  })

  test('successful login', async () => {
    const onSuccess = jest.fn()
    render(<Login onSuccess={onSuccess} />)
    
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'admin' }
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password' }
    })
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalledWith('fake-token')
    })
  })

  test('failed login shows error', async () => {
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'wrong' }
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrong' }
    })
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
})