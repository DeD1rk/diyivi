import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Make a ConDisCon that includes the given attributes, but is grouped by credential.
 *
 * This prevents issues with the requirement that each inner conjunction can consist of
 * attributes of at most one non-singleton credential, while still guaranteeing that all
 * the disclosed values of all attributes of a credential come from the same single instance
 * of that credential.
 *
 * @param attributes A list a attribute IDs.
 * @returns A CondDisCon of attribute IDs grouped by their credential.
 */
export function createConDisCon(attributes: string[]): string[][][] {
  const credentials: Map<string, Set<string>> = new Map()

  // Populate the Map with attributes grouped by their credential
  for (const attribute of attributes) {
    const credential = attribute.slice(0, attribute.lastIndexOf('.'))
    if (!credentials.has(credential)) {
      credentials.set(credential, new Set())
    }
    credentials.get(credential)!.add(attribute)
  }

  // Create the condiscon structure
  const condiscon: string[][][] = []
  for (const [key, value] of credentials) {
    condiscon.push([Array.from(value)])
  }

  return condiscon
}
