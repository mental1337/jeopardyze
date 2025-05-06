import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  styles: {
    global: {
      body: {
        color: 'gray.800',
        fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        minHeight: '100vh',
        backgroundImage: 
          'radial-gradient(circle at 25px 25px, rgba(148, 128, 255, 0.3) 5px, transparent 0), ' + 
          'radial-gradient(circle at 75px 75px, rgba(148, 128, 255, 0.3) 5px, transparent 0)',
        backgroundSize: '100px 100px',

      }
    }
  }
})

export default theme 