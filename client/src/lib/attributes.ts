export const publicAttributeOptions: {
  [key: string]: { label: string; description: string | null; attributeId: string }
} = {
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    description: 'Bijvoorbeeld via WhatsApp of Signal.',
    attributeId: 'irma-demo.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    description: null,
    attributeId: 'irma-demo.sidn-pbdf.email.email'
  }
}

export const attributeOptions: {
  [key: string]: { label: string; attributeId: string }
} = {
  name: {
    label: 'Naam',
    attributeId: 'irma-demo.gemeente.personalData.fullname'
  },
  birthdate: {
    label: 'Geboortedatum',
    attributeId: 'irma-demo.gemeente.personalData.dateofbirth'
  },
  mobilenumber: {
    label: 'Mobiel telefoonnumer',
    attributeId: 'irma-demo.sidn-pbdf.mobilenumber.mobilenumber'
  },
  email: {
    label: 'E-mailadres',
    attributeId: 'irma-demo.sidn-pbdf.email.email'
  }
}
