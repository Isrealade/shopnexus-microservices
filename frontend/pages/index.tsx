import React, { useState, useEffect } from 'react'
import { Box, Container, Heading, SimpleGrid, Text, VStack, Button, useToast, HStack, Badge } from '@chakra-ui/react'
import axios from 'axios'
import AuthForm from '../components/AuthForm'

interface Product {
  id: number
  name: string
  description: string
  price: number
  stock: number
  category: string
}

interface User {
  id: number
  username: string
  email: string
}

const API_URL = process.env.NEXT_PUBLIC_PRODUCT_API_URL || 'http://localhost:5002'

const Home: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [user, setUser] = useState<User | null>(null)
  const [showAuth, setShowAuth] = useState(false)
  const [token, setToken] = useState('')
  const toast = useToast()

  const fetchProducts = async () => {
    try {
      console.log('Fetching products from:', `${API_URL}/api/products`)
      
      const response = await axios.get(`${API_URL}/api/products`)
      console.log('Products response:', response.data)
      
      setProducts(response.data)
      setLoading(false)
    } catch (err: any) {
      console.error('Error fetching products:', err)
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status,
        config: err.config
      })
      
      setError(`Failed to fetch products: ${err.message}`)
      setLoading(false)
      
      toast({
        title: 'Error',
        description: 'Failed to fetch products',
        status: 'error',
        duration: 5000,
        isClosable: true
      })
    }
  }

  const fetchUserProfile = async (token: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_USER_API_URL || 'http://localhost:5001'
      const response = await axios.get(`${apiUrl}/api/users/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setUser(response.data)
      localStorage.setItem('token', token)
    } catch (error) {
      console.error('Error fetching user profile:', error)
      localStorage.removeItem('token')
    }
  }

  const handleAuthSuccess = async (newToken: string) => {
    setToken(newToken)
    setShowAuth(false)
    await fetchUserProfile(newToken)
    toast({
      title: 'Success',
      description: 'You are now logged in',
      status: 'success',
      duration: 3000,
      isClosable: true
    })
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('token')
    toast({
      title: 'Logged out successfully',
      status: 'success',
      duration: 3000,
      isClosable: true
    })
  }

  useEffect(() => {
    fetchProducts()
    const token = localStorage.getItem('token')
    if (token) {
      fetchUserProfile(token)
    }
  }, [])

  if (loading) return <Text>Loading...</Text>
  if (error) return <Text color="red.500">{error}</Text>

  return (
    <Container maxW="container.xl" py={10}>
      <VStack spacing={8} align="stretch">
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Heading as="h1" size="2xl" color="blue.600">
            Welcome to ShopNexus
          </Heading>
          {user ? (
            <VStack align="end" spacing={2}>
              <Text>Welcome, {user.username}!</Text>
              <Button colorScheme="red" size="sm" onClick={handleLogout}>
                Logout
              </Button>
            </VStack>
          ) : (
            <Button colorScheme="blue" onClick={() => setShowAuth(true)}>
              Login / Register
            </Button>
          )}
        </Box>

        {showAuth && !user && (
          <AuthForm 
            onAuthSuccess={handleAuthSuccess}
            isOpen={showAuth}
            onClose={() => setShowAuth(false)}
          />
        )}

        <Text textAlign="center" fontSize="xl" color="gray.600">
          Your One-Stop Shop for Everything
        </Text>
        
        {products.length === 0 ? (
          <Text textAlign="center" color="gray.500">No products available</Text>
        ) : (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {products.map((product: Product) => (
              <Box
                key={product.id}
                p={6}
                shadow="md"
                borderWidth="1px"
                borderRadius="lg"
                _hover={{ shadow: 'lg' }}
              >
                <VStack align="start" spacing={3}>
                  <Heading size="md">{product.name}</Heading>
                  <Text>{product.description}</Text>
                  <Text fontWeight="bold">${product.price}</Text>
                  <HStack>
                    <Badge colorScheme={product.stock > 0 ? 'green' : 'red'}>
                      {product.stock > 0 ? `In Stock: ${product.stock}` : 'Out of Stock'}
                    </Badge>
                    <Badge colorScheme="purple">{product.category}</Badge>
                  </HStack>
                </VStack>
              </Box>
            ))}
          </SimpleGrid>
        )}
      </VStack>
    </Container>
  )
}

export default Home 