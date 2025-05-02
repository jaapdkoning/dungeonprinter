<template>
  <div class="container">
    <h1>Dungeon Generator</h1>

    <label for="theme-select">Select a Theme:</label>
    <select id="theme-select" v-model="selectedTheme">
      <option v-for="theme in themes" :key="theme" :value="theme">{{ theme }}</option>
    </select>

    <button @click="generateDungeon">Generate Dungeon</button>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="loading">🧙‍♂️ Generating dungeon...</div>

    <div v-if="rooms.length" class="output">
      <h2>Generated Dungeon ({{ themeUsed }})</h2>
      <div v-for="(room, index) in rooms" :key="index" v-html="room" class="room"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const themes = ref([]);
    const selectedTheme = ref("");
    const rooms = ref([]);
    const loading = ref(false);
    const error = ref("");
    const themeUsed = ref("");

    onMounted(async () => {
      const res = await fetch("/api/themes");
      themes.value = await res.json();
      selectedTheme.value = themes.value[0];
    });

    const generateDungeon = async () => {
      loading.value = true;
      error.value = "";
      rooms.value = [];

      try {
        const res = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: selectedTheme.value, count: 4 }),
        });

        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);

        const data = await res.json();
        rooms.value = data.rooms;
        themeUsed.value = data.theme;
      } catch (err) {
        error.value = err.message || "Something went wrong.";
      } finally {
        loading.value = false;
      }
    };

    return {
      themes,
      selectedTheme,
      rooms,
      loading,
      error,
      themeUsed,
      generateDungeon,
    };
  },
};
</script>

<style>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
.room {
  margin: 1rem 0;
  padding: 1rem;
  background: #f4f4f4;
  border-radius: 8px;
  white-space: pre-wrap;
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>
