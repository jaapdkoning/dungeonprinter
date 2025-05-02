<template>
  <div class="container">
    <h1>Dungeon Generator</h1>

    <label for="theme-select">Select a Theme:</label>
    <select id="theme-select" v-model="selectedTheme">
      <option v-for="theme in themes" :key="theme" :value="theme">{{ theme }}</option>
    </select>

    <button @click="generateDungeon">Generate Dungeon</button>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="loading">🧙‍♂️ Generating dungeon...</div>

    <div v-if="rooms.length" id="pdf-output" class="output">
      <h2>Generated Dungeon: {{ themeUsed }}</h2>
      <div v-for="(room, index) in rooms" :key="index" v-html="room" class="room"></div>
    </div>

    <button v-if="rooms.length" @click="downloadPDF">📄 Download as PDF</button>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";
import { marked } from "marked";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

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
        rooms.value = data.rooms.map((r) => marked.parse(r));
        themeUsed.value = data.theme;
      } catch (err) {
        error.value = err.message || "Something went wrong.";
      } finally {
        loading.value = false;
      }
    };

    const downloadPDF = async () => {
      const el = document.getElementById("pdf-output");
      const canvas = await html2canvas(el);
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      const width = pdf.internal.pageSize.getWidth();
      const height = (canvas.height * width) / canvas.width;
      pdf.addImage(imgData, "PNG", 0, 0, width, height);
      pdf.save(`dungeon_${themeUsed.value.replace(/\\s/g, '_')}.pdf`);
    };

    return {
      themes,
      selectedTheme,
      rooms,
      loading,
      error,
      themeUsed,
      generateDungeon,
      downloadPDF,
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
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
.room {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f9f9f9;
  border-left: 4px solid #999;
}
.output h2 {
  border-bottom: 2px solid #ccc;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}
</style>
