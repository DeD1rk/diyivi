import type { paths } from './schema.d.ts'
import createClient from 'openapi-fetch'

const client = createClient<paths>({
  baseUrl: import.meta.env.VITE_BACKEND_URL || window.origin
})

export default client
