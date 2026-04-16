<script setup>
import { computed, onMounted, ref } from "vue";

const apiBase = "http://127.0.0.1:8000";

const overview = ref({
  document_count: 0,
  page_count: 0,
  chunk_count: 0,
  sources: [],
});
const loadingOverview = ref(true);
const loadingAnswer = ref(false);
const errorMessage = ref("");
const question = ref("");
const activeSources = ref([]);
const conversation = ref([
  {
    id: 1,
    role: "assistant",
    title: "Clinical briefing channel",
    content:
      "Ask a medical question grounded in your uploaded PDFs. I will answer from retrieved evidence and show the source passages used.",
  },
]);

const quickPrompts = [
  "Summarize the treatment guidance for hypertension.",
  "What are the key diagnostic criteria mentioned in the documents?",
  "List contraindications or precautions described in the source material.",
  "Compare the major recommendations across the uploaded guidelines.",
];

const sourceCountLabel = computed(() => `${activeSources.value.length} evidence cards`);

async function fetchOverview() {
  loadingOverview.value = true;
  errorMessage.value = "";

  try {
    const response = await fetch(`${apiBase}/api/overview`);
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Failed to load overview.");
    }

    overview.value = payload;
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loadingOverview.value = false;
  }
}

function usePrompt(prompt) {
  question.value = prompt;
}

async function submitQuestion() {
  const trimmed = question.value.trim();
  if (!trimmed || loadingAnswer.value) {
    return;
  }

  errorMessage.value = "";
  loadingAnswer.value = true;
  activeSources.value = [];

  conversation.value.push({
    id: Date.now(),
    role: "user",
    title: "Query",
    content: trimmed,
  });

  try {
    const response = await fetch(`${apiBase}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: trimmed }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Failed to get answer.");
    }

    conversation.value.push({
      id: Date.now() + 1,
      role: "assistant",
      title: "Evidence-grounded answer",
      content: payload.answer,
    });

    activeSources.value = payload.sources || [];
    question.value = "";
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loadingAnswer.value = false;
  }
}

onMounted(() => {
  fetchOverview();
});
</script>

<template>
  <div class="app-shell">
    <div class="ambient ambient-left"></div>
    <div class="ambient ambient-right"></div>

    <aside class="sidebar panel">
      <div class="eyebrow">Medical Knowledge Console</div>
      <h1>Document-grounded clinical assistant</h1>

      <section class="source-panel">
        <div class="section-head">
          <h2>Knowledge assets</h2>
          <button class="ghost-button" @click="fetchOverview">Refresh</button>
        </div>

        <p v-if="loadingOverview" class="muted">Indexing metadata...</p>
        <ul v-else class="source-list">
          <li v-for="source in overview.sources" :key="source">
            {{ source.split("/").pop() }}
          </li>
        </ul>
      </section>

      <section class="prompt-panel">
        <div class="section-head">
          <h2>Quick prompts</h2>
        </div>
        <div class="prompt-list">
          <button
            v-for="prompt in quickPrompts"
            :key="prompt"
            class="prompt-chip"
            @click="usePrompt(prompt)"
          >
            {{ prompt }}
          </button>
        </div>
      </section>
    </aside>

    <main class="workspace">
      <section class="hero panel">
        <div>
          <p class="eyebrow">Interactive Review</p>
          <h2 class="hero-title">Ask, inspect, and verify against the source material.</h2>
        </div>
        <div class="hero-badge">
          <span>Live retrieval</span>
          <strong>{{ sourceCountLabel }}</strong>
        </div>
      </section>

      <section class="conversation panel">
        <div class="section-head">
          <h2>Dialogue</h2>
          <span class="muted">Answers are restricted to retrieved context.</span>
        </div>

        <div class="message-list">
          <article
            v-for="message in conversation"
            :key="message.id"
            class="message"
            :class="message.role"
          >
            <div class="message-meta">
              <span>{{ message.title }}</span>
              <small>{{ message.role === "user" ? "Clinician" : "Assistant" }}</small>
            </div>
            <p>{{ message.content }}</p>
          </article>

          <article v-if="loadingAnswer" class="message assistant loading">
            <div class="message-meta">
              <span>Evidence-grounded answer</span>
              <small>Assistant</small>
            </div>
            <p>Retrieving passages, re-ranking evidence, drafting response...</p>
          </article>
        </div>

        <div class="composer">
          <textarea
            v-model="question"
            rows="4"
            placeholder="Enter a medical question based on the uploaded PDFs..."
            @keydown.enter.exact.prevent="submitQuestion"
          ></textarea>
          <div class="composer-bar">
            <p class="muted">
              Press Enter to submit, Shift + Enter for a new line.
            </p>
            <button class="primary-button" :disabled="loadingAnswer" @click="submitQuestion">
              {{ loadingAnswer ? "Thinking..." : "Ask assistant" }}
            </button>
          </div>
        </div>

        <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>
      </section>

      <section class="evidence panel">
        <div class="section-head">
          <h2>Evidence cards</h2>
          <span class="muted">Top reranked passages returned by the backend.</span>
        </div>

        <div v-if="!activeSources.length" class="empty-state">
          Ask a question to inspect the retrieved passages and source metadata.
        </div>

        <div v-else class="evidence-grid">
          <article v-for="(source, index) in activeSources" :key="`${source.source}-${index}`" class="evidence-card">
            <div class="evidence-top">
              <span class="evidence-index">0{{ index + 1 }}</span>
              <div>
                <h3>{{ source.source.split("/").pop() }}</h3>
                <p>Page {{ source.page ?? "N/A" }}</p>
              </div>
            </div>
            <p class="evidence-body">{{ source.content }}</p>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>
