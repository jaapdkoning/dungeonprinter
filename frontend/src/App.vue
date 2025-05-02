<template>
  <div class="container">
    <h1>Dungeon Generator</h1>
    <label for="theme-select">Select a Theme:</label>
    <select id="theme-select" v-model="selectedTheme">
      <option v-for="theme in themes" :key="theme" :value="theme">
        {{ theme }}
      </option>
    </select>
    <button @click="generateDungeon">Generate Dungeon</button>
    <div v-if="markdown" v-html="markdown" class="markdown-output"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const themes = ref([]);
    const selectedTheme = ref('');
    const markdown = ref('');

    onMounted(async () => {
      const response = await fetch('/api/themes');
      themes.value = await response.json();
      selectedTheme.value = themes.value[0];
    });

    const generateDungeon = async () => {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme: selectedTheme.value }),
      });
      const data = await response.json();
      markdown.value = data.markdown;
    };

    return { themes, selectedTheme, markdown, generateDungeon };
  },
};
</script>

<style>
.container {
  max-width: 800px;
  margin: auto;
  padding: 2rem;
}
.markdown-output {
  margin-top: 2rem;
  border-top: 1px solid #ccc;
  padding-top: 1rem;
}
</style>
