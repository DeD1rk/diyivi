import type { TranslatedString } from '@/api/types'

export const publicAttributeOptions: {
  [key: string]: { label: string; description: string | null; attributeId: string }
} = {
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    description: 'Bijvoorbeeld via WhatsApp of Signal.',
    attributeId: 'pbdf.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    description: null,
    attributeId: 'pbdf.sidn-pbdf.email.email'
  }
}

export const attributeOptions: {
  [key: string]: { label: string; attributes: string[] }
} = {
  name: {
    label: 'Volledige naam',
    attributes: ['pbdf.gemeente.personalData.fullname']
  },
  birthdate: {
    label: 'Geboortedatum',
    attributes: ['pbdf.gemeente.personalData.dateofbirth']
  },
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    attributes: ['pbdf.sidn-pbdf.mobilenumber.mobilenumber']
  },
  email: {
    label: 'E-mailadres',
    attributes: ['pbdf.sidn-pbdf.email.email']
  },
  address: {
    label: 'Woonadres',
    attributes: [
      'pbdf.gemeente.address.street',
      'pbdf.gemeente.address.houseNumber',
      'pbdf.gemeente.address.zipcode',
      'pbdf.gemeente.address.city'
    ]
  }
}

export const publicAttributeDisplayOptions: {
  [key: string]: {
    label: string
  }
} = {
  'pbdf.gemeente.personalData.fullname': {
    label: 'naam'
  },
  'pbdf.gemeente.personalData.dateofbirth': {
    label: 'geboortedatum'
  },
  'pbdf.sidn-pbdf.mobilenumber.mobilenumber': {
    label: 'mobiel telefoonnummer'
  },
  'pbdf.sidn-pbdf.email.email': {
    label: 'e-mailadres'
  }
}

export type DisclosedMap = { [key: string]: TranslatedString }
export const attributeDisplayOptions: {
  label: string
  requiredAttributes: string[]
  display: (disclosed: DisclosedMap) => string
}[] = [
  {
    label: 'Volledige naam',
    requiredAttributes: ['pbdf.gemeente.personalData.fullname'],
    display: (values: DisclosedMap) => values['pbdf.gemeente.personalData.fullname']!.nl
  },
  {
    label: 'E-mailadres',
    requiredAttributes: ['pbdf.sidn-pbdf.email.email'],
    display: (values: DisclosedMap) => values['pbdf.sidn-pbdf.email.email']!.nl
  },
  {
    label: 'Mobiel telefoonnummer',
    requiredAttributes: ['pbdf.sidn-pbdf.mobilenumber.mobilenumber'],
    display: (values: DisclosedMap) => values['pbdf.sidn-pbdf.mobilenumber.mobilenumber']!.nl
  },
  {
    label: 'Geboortedatum',
    requiredAttributes: ['pbdf.gemeente.personalData.dateofbirth'],
    display: (values: DisclosedMap) => values['pbdf.gemeente.personalData.dateofbirth']!.nl
  },
  {
    label: 'Woonadres',
    requiredAttributes: [
      'pbdf.gemeente.address.street',
      'pbdf.gemeente.address.houseNumber',
      'pbdf.gemeente.address.zipcode',
      'pbdf.gemeente.address.city'
    ],
    display: (values: DisclosedMap) => {
      const address = values['pbdf.gemeente.address.street']!.nl
      const houseNumber = values['pbdf.gemeente.address.houseNumber']!.nl
      const zipcode = values['pbdf.gemeente.address.zipcode']!.nl
      const city = values['pbdf.gemeente.address.city']!.nl
      return `${address} ${houseNumber}, ${zipcode} ${city}`
    }
  }
]
