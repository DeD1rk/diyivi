import type { InitiatorExchangeResponse } from '@/api/types'
import type { InjectionKey, Ref } from 'vue'

export const initiatorExchangeKey = Symbol() as InjectionKey<Ref<InitiatorExchangeResponse | null>>
