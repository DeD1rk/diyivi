<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { NavigationMenuLink } from '@/components/ui/navigation-menu'
import { Menu } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { ArrowRightLeft, Signature, Forward, TextSearch } from 'lucide-vue-next'
</script>

<template>
  <nav class="bg-background shadow-lg w-full sticky top-0">
    <div
      class="max-w-screen-sm lg:max-w-screen-md flex flex-wrap items-center justify-between mx-auto px-8 py-3"
    >
      <div class="flex items-baseline">
        <RouterLink to="/">
          <div class="font-extrabold text-2xl tracking-tighter text-yivi-red">
            <span class="text-black">diy</span>ivi
          </div>
        </RouterLink>
        <div class="text-2xl ms-6 text-muted-foreground font-semibold hidden min-[480px]:inline">
          weet met wie je praat!
        </div>
      </div>
      <div>
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline"><Menu /></Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent class="w-72">
            <DropdownMenuLabel>Wie is wie?</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <NavigationMenuLink as-child>
              <a
                href="/exchange/start/"
                class="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
              >
                <div class="text-sm font-medium leading-none">
                  <ArrowRightLeft class="inline w-4 h-4 me-2" />Leer elkaar kennen
                </div>
                <p class="text-xs leading-snug text-muted-foreground">
                  Neem het initiatief om met zekerheid gegevens met iemand uit te wisselen.
                </p>
              </a>
            </NavigationMenuLink>
            <DropdownMenuSeparator />
            <DropdownMenuLabel>Wie zegt wat?</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <NavigationMenuLink as-child>
              <a
                href="/signature/create/"
                class="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
              >
                <div class="text-sm font-medium leading-none">
                  <Signature class="inline w-4 h-4 me-2" />Onderteken zelf
                </div>
                <p class="text-xs leading-snug text-muted-foreground">
                  Onderteken een afspraak met Yivi.
                </p>
              </a>
            </NavigationMenuLink>
            <NavigationMenuLink as-child>
              <a
                href="/signature/request/create/"
                class="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
              >
                <div class="text-sm font-medium leading-none">
                  <Forward class="inline w-4 h-4 me-2" />Vraag iemand anders te tekenen
                </div>
                <p class="text-xs leading-snug text-muted-foreground">
                  Stel een afspraak op en verzoek iemand om deze te ondertekenen met Yivi.
                </p>
              </a>
            </NavigationMenuLink>
            <NavigationMenuLink as-child>
              <a
                href="/signature/verify/"
                class="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
              >
                <div class="text-sm font-medium leading-none">
                  <TextSearch class="inline w-4 h-4 me-2" />Handtekening controleren
                </div>
                <p class="text-xs leading-snug text-muted-foreground">
                  Controleer een bericht in dat ondertekend is met DIYivi om te zien wie wat gezegd
                  heeft.
                </p>
              </a>
            </NavigationMenuLink>
            <DropdownMenuSeparator />
            <NavigationMenuLink as-child>
              <a
                href="/about/"
                class="block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
              >
                <div class="text-sm font-medium leading-none">Over DIYivi</div>
                <p class="text-xs leading-snug text-muted-foreground">
                  Hoe werkt DIYivi, en hoe zit het met privacy?
                </p>
              </a>
            </NavigationMenuLink>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  </nav>
</template>
