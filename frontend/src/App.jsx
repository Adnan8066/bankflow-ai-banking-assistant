import { Route, Routes } from "react-router-dom";

import AppLayout from "./components/AppLayout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import Landing from "./pages/Landing.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Account from "./pages/Account.jsx";
import Transactions from "./pages/Transactions.jsx";
import TransactionDetails from "./pages/TransactionDetails.jsx";
import Loans from "./pages/Loans.jsx";
import LoanDetails from "./pages/LoanDetails.jsx";
import EMICalculator from "./pages/EMICalculator.jsx";
import AIAssistant from "./pages/AIAssistant.jsx";
import Notifications from "./pages/Notifications.jsx";
import Profile from "./pages/Profile.jsx";
import NotFound from "./pages/NotFound.jsx";

import AdminDashboard from "./pages/admin/AdminDashboard.jsx";
import CustomerManagement from "./pages/admin/CustomerManagement.jsx";
import TransactionManagement from "./pages/admin/TransactionManagement.jsx";
import LoanManagement from "./pages/admin/LoanManagement.jsx";
import AdminAnalytics from "./pages/admin/AdminAnalytics.jsx";
import AIMonitor from "./pages/admin/AIMonitor.jsx";

/**
 * Route map
 * ─ public      : /, /login, /register
 * ─ customer    : everything inside the protected AppLayout
 * ─ bank staff  : /admin/* (role="ADMIN" guard)
 */
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/account" element={<Account />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/transactions/:id" element={<TransactionDetails />} />
          <Route path="/loans" element={<Loans />} />
          <Route path="/loans/:id" element={<LoanDetails />} />
          <Route path="/emi-calculator" element={<EMICalculator />} />
          <Route path="/assistant" element={<AIAssistant />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute role="ADMIN" />}>
        <Route element={<AppLayout />}>
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/customers" element={<CustomerManagement />} />
          <Route path="/admin/transactions" element={<TransactionManagement />} />
          <Route path="/admin/loans" element={<LoanManagement />} />
          <Route path="/admin/analytics" element={<AdminAnalytics />} />
          <Route path="/admin/ai-monitor" element={<AIMonitor />} />
        </Route>
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
