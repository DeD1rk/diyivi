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
  [key: string]: { label: string; attributeId: string }
} = {
  name: {
    label: 'Volledige naam',
    attributeId: 'pbdf.gemeente.personalData.fullname'
  },
  birthdate: {
    label: 'Geboortedatum',
    attributeId: 'pbdf.gemeente.personalData.dateofbirth'
  },
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    attributeId: 'pbdf.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    attributeId: 'pbdf.sidn-pbdf.email.email'
  }
  // TODO: adres
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

export const attributeDisplayOptions: {
  [key: string]: {
    label: string
  }
} = {
  'pbdf.gemeente.personalData.fullname': {
    label: 'Volledige naam'
  },
  'pbdf.gemeente.personalData.dateofbirth': {
    label: 'Geboortedatum'
  },
  'pbdf.sidn-pbdf.mobilenumber.mobilenumber': {
    label: 'Mobiel telefoonnummer'
  },
  'pbdf.sidn-pbdf.email.email': {
    label: 'E-mailadres'
  }
  // TODO: adres
}
