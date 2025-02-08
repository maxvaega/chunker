import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Dashboard } from '../../components/Dashboard'

describe('Dashboard Component', () => {
  test('renders file upload section', () => {
    render(<Dashboard />)
    expect(screen.getByText(/upload markdown/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /upload/i })).toBeInTheDocument()
  })

  test('handles file upload success', async () => {
    const file = new File(['# Test'], 'test.md', { type: 'text/markdown' })
    render(<Dashboard />)
    
    const input = screen.getByLabelText(/choose file/i)
    fireEvent.change(input, { target: { files: [file] } })
    
    await waitFor(() => {
      expect(screen.getByText(/file uploaded successfully/i)).toBeInTheDocument()
    })
  })

  test('shows error on invalid file', async () => {
    const file = new File(['invalid'], 'test.txt', { type: 'text/plain' })
    render(<Dashboard />)
    
    const input = screen.getByLabelText(/choose file/i)
    fireEvent.change(input, { target: { files: [file] } })
    
    await waitFor(() => {
      expect(screen.getByText(/invalid file type/i)).toBeInTheDocument()
    })
  })

  test('displays chunked content after processing', async () => {
    render(<Dashboard />)
    // Mock successful API response
    await waitFor(() => {
      expect(screen.getByTestId('chunks-display')).toBeInTheDocument()
    })
  })
})