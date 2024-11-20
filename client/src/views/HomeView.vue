<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
import { ArrowRightLeft, Signature, Forward, TextSearch } from 'lucide-vue-next'
</script>

<template>
  <div class="p-8">
    <Title>Zelf aan de slag met digitale identiteit</Title>
    <p>
      In de digitale wereld weten we vaak niet zeker met wie we contact hebben. Dat kan allerlei
      problemen geven, variërend van pijnlijke misverstanden tot ordinair bedrog. Via deze webpagina
      kun je zekerheid krijgen en geven over wie met wie praat.
    </p>

    <div class="flex flex-col lg:flex-row gap-6 mt-6">
      <!-- Card 1 -->
      <div class="flex-1 bg-yivi-lightblue p-4 pt-0">
        <Header>Wie is wie?</Header>
        <p class="text-sm">
          Praat je met iemand via e-mail of chat en wil je van beide kanten meer zekerheid? Maak
          hieronder een verzoek om elkaar beter te leren kennen. Als initiatiefnemer maak jij jezelf
          eerst bekend aan deze website. Dan krijg je een link die je met de ander kunt delen (via
          e-mail of chat). Pas als de ander zich ook bekend gemaakt heeft aan deze website, worden
          jullie gegevens onderling uitgewisseld en leren jullie elkaar echt kennen. Deze website
          gooit jullie gegevens ten slotte weg en bewaart niks.
        </p>

        <Button as-child class="mt-4">
          <RouterLink to="/exchange/start/"
            ><ArrowRightLeft class="w-4 h-4 me-2" />Leer elkaar kennen</RouterLink
          >
        </Button>
      </div>

      <div class="flex-1 bg-yivi-lightblue p-4 pt-0">
        <Header>Wie zegt wat?</Header>
        <p class="text-sm">
          Met een digitale handtekening kun je onderlinge afspraken vastleggen. Met onderstaande
          knoppen stel je een afspraak op, en onderteken je deze zelf, of vraag je iemand anders om
          te tekenen.
        </p>
        <div class="flex flex-wrap gap-2 mt-4">
          <Button as-child>
            <RouterLink to="/signature/create/"
              ><Signature class="w-4 h-4 me-2" />Onderteken zelf</RouterLink
            >
          </Button>
          <Button as-child>
            <RouterLink to="/signature/request/create/"
              ><Forward class="w-4 h-4 me-2" />Vraag iemand anders te tekenen</RouterLink
            >
          </Button>
        </div>
        <p class="text-sm mt-4">
          Een al getekende tekst kun je hier ook controleren. Je weet dan zeker wie wat getekend
          heeft.
        </p>
        <Button as-child class="mt-4">
          <RouterLink to="/signature/verify/"
            ><TextSearch class="w-4 h-4 me-2" />Handtekening controleren</RouterLink
          >
        </Button>
      </div>
    </div>
  </div>
</template>
