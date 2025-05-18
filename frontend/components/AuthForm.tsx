import React, { useState } from 'react'
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Text,
  useToast,
  Switch,
  FormHelperText,
  Stack,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton
} from '@chakra-ui/react'
import axios from 'axios'

interface AuthFormProps {
  onAuthSuccess: (token: string) => void
  isOpen: boolean
  onClose: () => void
}

const AuthForm: React.FC<AuthFormProps> = ({ onAuthSuccess, isOpen, onClose }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<{ [key: string]: string }>({})
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setErrors({})

    try {
      const apiUrl = process.env.NEXT_PUBLIC_USER_API_URL || 'http://localhost:5001'
      const endpoint = isLogin ? '/api/users/login' : '/api/users/register'
      console.log('Making request to:', `${apiUrl}${endpoint}`)
      
      const response = await axios.post(`${apiUrl}${endpoint}`, {
        username,
        email: isLogin ? undefined : email,
        password
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        timeout: 10000
      })

      console.log('Response:', response.data)

      if (isLogin) {
        const { access_token } = response.data
        onAuthSuccess(access_token)
        toast({
          title: 'Login successful',
          status: 'success',
          duration: 3000,
          isClosable: true
        })
        onClose()
      } else {
        toast({
          title: 'Registration successful',
          description: 'Please login with your credentials',
          status: 'success',
          duration: 3000,
          isClosable: true
        })
        setIsLogin(true)
      }
    } catch (error: any) {
      console.error('Auth error:', error)
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config
      })
      
      if (error.response?.data?.error) {
        setErrors({ submit: error.response.data.error })
      } else {
        setErrors({ submit: 'Something went wrong' })
      }
      
      toast({
        title: 'Error',
        description: error.response?.data?.error || 'Something went wrong',
        status: 'error',
        duration: 5000,
        isClosable: true
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader textAlign="center">
          {isLogin ? 'Login' : 'Register'}
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          <form onSubmit={handleSubmit}>
            <Stack spacing={4}>
              <Box>
                <FormLabel>Username</FormLabel>
                <Input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  isRequired
                />
              </Box>

              {!isLogin && (
                <Box>
                  <FormLabel>Email</FormLabel>
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    isRequired
                  />
                </Box>
              )}

              <Box>
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  isRequired
                />
              </Box>

              {errors.submit && (
                <Text color="red.500" fontSize="sm">
                  {errors.submit}
                </Text>
              )}

              <Button
                type="submit"
                colorScheme="blue"
                width="full"
                isLoading={loading}
              >
                {isLogin ? 'Login' : 'Register'}
              </Button>
            </Stack>
          </form>

          <Box textAlign="center" mt={4}>
            <Box display="flex" alignItems="center" justifyContent="center">
              <Text mr={2}>
                {isLogin ? 'Need an account?' : 'Already have an account?'}
              </Text>
              <Switch
                isChecked={!isLogin}
                onChange={() => {
                  setIsLogin(!isLogin)
                  setErrors({})
                }}
              />
            </Box>
            <Text fontSize="sm" color="gray.500" mt={1}>
              {isLogin ? 'Switch to register' : 'Switch to login'}
            </Text>
          </Box>
        </ModalBody>
      </ModalContent>
    </Modal>
  )
}

export default AuthForm 