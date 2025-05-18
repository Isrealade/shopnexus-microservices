import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import Home from '../pages/index'
import { ChakraProvider } from '@chakra-ui/react'

// Mock axios
jest.mock('axios', () => ({
  get: jest.fn()
}))

// Mock Chakra UI components
jest.mock('@chakra-ui/react', () => {
  const originalModule = jest.requireActual('@chakra-ui/react')
  return {
    ...originalModule,
    Box: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    Container: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    Heading: ({ children, ...props }: any) => <h1 {...props}>{children}</h1>,
    SimpleGrid: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    Text: ({ children, ...props }: any) => <p {...props}>{children}</p>,
    VStack: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  }
})

describe('Home Page', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders loading state initially', () => {
    render(
      <ChakraProvider>
        <Home />
      </ChakraProvider>
    )
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders error state when API call fails', async () => {
    const axios = require('axios')
    axios.get.mockRejectedValueOnce(new Error('Failed to fetch'))

    render(
      <ChakraProvider>
        <Home />
      </ChakraProvider>
    )

    await waitFor(() => {
      expect(screen.getByText(/Failed to fetch products: Failed to fetch/)).toBeInTheDocument()
    })
  })

  it('renders products when API call succeeds', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Test Product',
        description: 'Test Description',
        price: 99.99,
        stock: 10,
        category: 'Test Category'
      }
    ]

    const axios = require('axios')
    axios.get.mockResolvedValueOnce({ data: mockProducts })

    render(
      <ChakraProvider>
        <Home />
      </ChakraProvider>
    )

    await waitFor(() => {
      expect(screen.getByText('Test Product')).toBeInTheDocument()
      expect(screen.getByText('Test Description')).toBeInTheDocument()
      expect(screen.getByText('$99.99')).toBeInTheDocument()
    })
  })

  it('shows out of stock message when stock is 0', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Test Product',
        description: 'Test Description',
        price: 99.99,
        stock: 0,
        category: 'Test Category'
      }
    ]

    const axios = require('axios')
    axios.get.mockResolvedValueOnce({ data: mockProducts })

    render(
      <ChakraProvider>
        <Home />
      </ChakraProvider>
    )

    await waitFor(() => {
      expect(screen.getByText('Out of Stock')).toBeInTheDocument()
    })
  })
}) 