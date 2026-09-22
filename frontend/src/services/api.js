import axios from "axios";

/**
 * One axios instance for the whole app.
 * - adds the JWT access token to every request
 * - refreshes the token once when the API answers 401
 * - turns network problems into friendly messages
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

const ACCESS_KEY = "bankflow_access";
const REFRESH_KEY = "bankflow_refresh";

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: ({ access, refresh }) => {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const access = tokenStore.getAccess();
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { response, config } = error;
    const isAuthCall = config?.url?.includes("/auth/login") || config?.url?.includes("/auth/refresh");

    if (response?.status === 401 && !config._retry && !isAuthCall && tokenStore.getRefresh()) {
      config._retry = true;
      try {
        refreshPromise =
          refreshPromise ||
          axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh: tokenStore.getRefresh() });
        const { data } = await refreshPromise;
        refreshPromise = null;
        tokenStore.set({ access: data.access });
        config.headers.Authorization = `Bearer ${data.access}`;
        return api(config);
      } catch (refreshError) {
        refreshPromise = null;
        tokenStore.clear();
        window.location.href = "/login?session=expired";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

/** Convert any axios failure into a single readable sentence. */
export function getErrorMessage(error) {
  if (!error) return "Something went wrong.";
  if (error.code === "ERR_NETWORK" || !error.response) {
    return "Cannot reach the BankFlow API. Is the Django server running on port 8000?";
  }
  const { data, status } = error.response;
  if (typeof data === "string") return data;
  if (data?.detail) return data.detail;
  if (data?.message) return data.message;
  if (Array.isArray(data?.non_field_errors) && data.non_field_errors.length) {
    return data.non_field_errors[0];
  }
  if (data && typeof data === "object") {
    const [field, messages] = Object.entries(data)[0] || [];
    if (field && Array.isArray(messages) && messages.length) {
      return `${field}: ${messages[0]}`;
    }
    if (field && typeof messages === "string") return `${field}: ${messages}`;
  }
  if (status === 404) return "We could not find that record in the demo data.";
  return "The request failed. Please try again.";
}

export default api;
