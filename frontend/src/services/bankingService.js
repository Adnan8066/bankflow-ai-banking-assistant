import api from "./api";

const bankingService = {
  getDashboard: () => api.get("/dashboard/").then((r) => r.data),
  getAccount: () => api.get("/account/").then((r) => r.data),

  getTransactions: (params = {}) =>
    api.get("/transactions/", { params }).then((r) => r.data),
  getTransaction: (id) => api.get(`/transactions/${id}/`).then((r) => r.data),

  getLoans: (params = {}) => api.get("/loans/", { params }).then((r) => r.data),
  getLoan: (id) => api.get(`/loans/${id}/`).then((r) => r.data),
  applyLoan: (payload) => api.post("/loans/", payload).then((r) => r.data),

  calculateEmi: (payload) => api.post("/emi/", payload).then((r) => r.data),

  getNotifications: () => api.get("/notifications/").then((r) => r.data),
  markNotificationRead: (id, isRead = true) =>
    api.put(`/notifications/${id}/`, { is_read: isRead }).then((r) => r.data),
  markAllNotificationsRead: () =>
    api.post("/notifications/read-all/").then((r) => r.data),
};

export default bankingService;
