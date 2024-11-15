import type { components } from './schema'

export type InitiatorExchangeResponse = components['schemas']['InitiatorExchangeResponse']
export type RecipientExchangeResponse = components['schemas']['RecipientExchangeResponse']
export type RecipientResponseResponse = components['schemas']['RecipientResponseResponse']

export type SignatureRequestResponse = components['schemas']['SignatureRequestResponse']
export type RecipientSignatureRequestResponse =
  components['schemas']['RecipientSignatureRequestResponse']

export type TranslatedString = components['schemas']['TranslatedString']
export type DisclosedValue = components['schemas']['DisclosedValue']
export type ExchangeReply = DisclosedValue[]
