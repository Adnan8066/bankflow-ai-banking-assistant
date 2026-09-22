import api, { tokenStore } from "./api";

const authService = {
  async register(payload) {
    const { data } = await api.post("/auth/register/", payload);
    return data;
  },

  async login({ email, password }) {
    const { data } = await api.post("/auth/login/", { email, password });
    tokenStore.set(data);
    return data;
  },

  async profile() {
    const { data } = await api.get("/profile/");
    return data;
  },

  async updateProfile(payload) {
    const { data } = await api.put("/profile/", payload);
    return data;
  },

  logout() {
    tokenStore.clear();
  },
};

export default authService;
