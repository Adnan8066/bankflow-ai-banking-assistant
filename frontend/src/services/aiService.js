import api from "./api";

const aiService = {
  chat: (message) => api.post("/assistant/chat/", { message }).then((r) => r.data),
  history: () => api.get("/assistant/history/").then((r) => r.data),
  suggestions: () => api.get("/assistant/suggestions/").then((r) => r.data),
  clearHistory: () => api.delete("/assistant/history/").then((r) => r.data),
};

export default aiService;
