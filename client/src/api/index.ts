import type { paths } from './schema.d.ts'
import createClient from 'openapi-fetch'

const client = createClient<paths>({ baseUrl: window.location.origin })

export default client
