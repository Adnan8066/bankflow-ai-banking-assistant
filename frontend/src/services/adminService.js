import api from "./api";

const adminService = {
  analytics: () => api.get("/admin/analytics/").then((r) => r.data),
  overview: () => api.get("/admin/analytics/overview/").then((r) => r.data),
  customers: (params = {}) => api.get("/admin/customers/", { params }).then((r) => r.data),
  customer: (id) => api.get(`/admin/customers/${id}/`).then((r) => r.data),
  transactions: (params = {}) =>
    api.get("/admin/transactions/", { params }).then((r) => r.data),
  loans: (params = {}) => api.get("/admin/loans/", { params }).then((r) => r.data),
  updateLoanStatus: (id, status) =>
    api.patch(`/admin/loans/${id}/`, { status }).then((r) => r.data),
  users: () => api.get("/admin/users/").then((r) => r.data),
  aiMonitor: (params = {}) => api.get("/assistant/monitor/", { params }).then((r) => r.data),
};

export default adminService;
