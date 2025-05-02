<template>
  <div class="container">
    <h1>🧙‍♂️ Dungeon Encounter Generator</h1>

    <label for="theme-input">Enter a Theme:</label>
    <input
      id="theme-input"
      v-model="theme"
      placeholder="e.g. Sunken Temple of the Frog-God"
    />

    <label for="difficulty-select">Select Difficulty:</label>
    <select id="difficulty-select" v-model="difficulty">
      <option value="1-3">Levels 1–3 (Beginner)</option>
      <option value="4-7">Levels 4–7 (Intermediate)</option>
      <option value="8+">Levels 8+ (Advanced)</option>
    </select>

    <button @click="generateEncounters">Generate Encounters</button>

    <div v-if="loading" class="loading">Loading encounters...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="encounters.length" class="output">
      <h2>Encounters for: {{ theme }} (Level {{ difficulty }})</h2>
      <div
        v-for="(encounter, index) in encounters"
        :key="index"
        class="encounter"
      >
        <h3>{{ encounter.title }} <span class="type">[{{ encounter.type }}]</span></h3>
        <p><strong>Situation:</strong> {{ encounter.situation }}</p>
        <p><strong>Challenge:</strong> {{ encounter.challenge }}</p>
        <p><strong>Reward:</strong> {{ encounter.reward }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const theme = ref("Undead Crypt");
    const difficulty = ref("1-3");
    const encounters = ref([]);
    const loading = ref(false);
    const error = ref("");

    const generateEncounters = async () => {
      loading.value = true;
      error.value = "";
      encounters.value = [];

      try {
        const res = await fetch("/api/encounters", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ theme: theme.value, difficulty: difficulty.value }),
        });

        if (!res.ok)
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);

        const data = await res.json();
        encounters.value = data.encounters;
      } catch (err) {
        error.value = err.message || "Failed to generate encounters.";
      } finally {
        loading.value = false;
      }
    };

    return {
      theme,
      difficulty,
      encounters,
      loading,
      error,
      generateEncounters,
    };
  },
};
</script>

<style>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: Georgia, serif;
}

input,
select {
  width: 100%;
  padding: 0.5rem;
  margin: 1rem 0;
  font-size: 1rem;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
}

.loading {
  margin: 1rem 0;
  font-style: italic;
}

.output {
  margin-top: 2rem;
}

.encounter {
  background: #f9f9f9;
  padding: 1rem;
  border-left: 4px solid #444;
  margin-bottom: 1.5rem;
  border-radius: 4px;
}

.encounter h3 {
  margin-bottom: 0.5rem;
}

.type {
  font-size: 0.9rem;
  color: #666;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
