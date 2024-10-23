<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
import Title from '@/components/Title.vue'
import Header from '@/components/Header.vue'
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
        <Header>Leer elkaar kennen</Header>
        <p class="text-sm">
          Praat je met iemand via e-mail of chat en wil je van beide kanten meer zekerheid? Maak
          hieronder een verzoek om elkaar beter te leren kennen. Als initiatiefnemer maak jij jezelf
          eerst bekend aan deze website. Dan krijg je een link die je met de ander kunt delen (via
          e-mail of chat). Pas als de ander zich ook bekend gemaakt heeft aan deze website, worden
          jullie gegevens onderling uitgewisseld en leren jullie elkaar echt kennen. Deze website
          gooit jullie gegevens ten slotte weg en bewaart niks.
        </p>

        <Button as-child class="mt-4">
          <RouterLink to="/exchange/start/">Leer elkaar kennen</RouterLink>
        </Button>
      </div>

      <div class="flex-1 bg-yivi-lightblue p-4 pt-0">
        <Header>Leg afspraken vast</Header>
        <p>...</p>
        <Button class="mt-4" to="/signature/create/"> Leg afspraak vast </Button>
      </div>
    </div>
  </div>
</template>
