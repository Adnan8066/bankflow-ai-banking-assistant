import {
  Avatar,
  Box,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import RequestQuoteIcon from "@mui/icons-material/RequestQuote";
import CalculateIcon from "@mui/icons-material/Calculate";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import NotificationsIcon from "@mui/icons-material/Notifications";
import PersonIcon from "@mui/icons-material/Person";
import GroupIcon from "@mui/icons-material/Group";
import InsightsIcon from "@mui/icons-material/Insights";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import LogoutIcon from "@mui/icons-material/Logout";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { initials } from "../utils/formatCurrency.js";

export const DRAWER_WIDTH = 252;

const CUSTOMER_LINKS = [
  { to: "/dashboard", label: "Dashboard", icon: <DashboardIcon /> },
  { to: "/account", label: "My Account", icon: <AccountBalanceIcon /> },
  { to: "/transactions", label: "Transactions", icon: <ReceiptLongIcon /> },
  { to: "/loans", label: "Loans", icon: <RequestQuoteIcon /> },
  { to: "/emi-calculator", label: "EMI Calculator", icon: <CalculateIcon /> },
  { to: "/assistant", label: "AI Assistant", icon: <SmartToyIcon /> },
  { to: "/notifications", label: "Notifications", icon: <NotificationsIcon /> },
  { to: "/profile", label: "Profile", icon: <PersonIcon /> },
];

const ADMIN_LINKS = [
  { to: "/admin", label: "Admin Dashboard", icon: <DashboardIcon /> },
  { to: "/admin/customers", label: "Customers", icon: <GroupIcon /> },
  { to: "/admin/transactions", label: "Transactions", icon: <ReceiptLongIcon /> },
  { to: "/admin/loans", label: "Loan Management", icon: <RequestQuoteIcon /> },
  { to: "/admin/analytics", label: "Analytics", icon: <InsightsIcon /> },
  { to: "/admin/ai-monitor", label: "AI Monitoring", icon: <MonitorHeartIcon /> },
];

function SidebarContent({ onNavigate }) {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <Toolbar sx={{ px: 2 }}>
        <Stack direction="row" spacing={1.25} alignItems="center">
          <Box
            sx={{
              display: "grid",
              placeItems: "center",
              width: 36,
              height: 36,
              borderRadius: 2,
              backgroundColor: "primary.main",
              color: "#fff",
            }}
          >
            <AccountBalanceWalletIcon fontSize="small" />
          </Box>
          <Box>
            <Typography variant="subtitle1" fontWeight={800} lineHeight={1.1}>
              BankFlow
            </Typography>
            <Typography variant="caption" color="text.secondary">
              AI Banking Assistant
            </Typography>
          </Box>
        </Stack>
      </Toolbar>
      <Divider />

      <List sx={{ px: 1.5, py: 2, flexGrow: 1 }}>
        <Typography
          variant="overline"
          sx={{ px: 1.5, color: "text.secondary", fontWeight: 700 }}
        >
          Banking
        </Typography>
        {CUSTOMER_LINKS.map((link) => (
          <ListItemButton
            key={link.to}
            component={NavLink}
            to={link.to}
            onClick={onNavigate}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              color: "text.secondary",
              "& .MuiListItemIcon-root": { color: "text.secondary", minWidth: 42 },
              "&.active": {
                backgroundColor: "#eef2fd",
                color: "primary.main",
                "& .MuiListItemIcon-root": { color: "primary.main" },
                "& .MuiListItemText-primary": { fontWeight: 700 },
              },
            }}
          >
            <ListItemIcon>{link.icon}</ListItemIcon>
            <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
          </ListItemButton>
        ))}

        {isAdmin && (
          <>
            <Typography
              variant="overline"
              sx={{ px: 1.5, mt: 2, display: "block", color: "text.secondary", fontWeight: 700 }}
            >
              Bank Employee
            </Typography>
            {ADMIN_LINKS.map((link) => (
              <ListItemButton
                key={link.to}
                component={NavLink}
                to={link.to}
                end={link.to === "/admin"}
                onClick={onNavigate}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  color: "text.secondary",
                  "& .MuiListItemIcon-root": { color: "text.secondary", minWidth: 42 },
                  "&.active": {
                    backgroundColor: "#eef2fd",
                    color: "primary.main",
                    "& .MuiListItemIcon-root": { color: "primary.main" },
                    "& .MuiListItemText-primary": { fontWeight: 700 },
                  },
                }}
              >
                <ListItemIcon>{link.icon}</ListItemIcon>
                <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
              </ListItemButton>
            ))}
          </>
        )}
      </List>

      <Divider />
      <Stack direction="row" spacing={1.5} alignItems="center" sx={{ p: 2 }}>
        <Avatar sx={{ bgcolor: "primary.main", width: 38, height: 38, fontSize: 14 }}>
          {initials(user?.name || "BF")}
        </Avatar>
        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
          <Typography variant="subtitle2" noWrap>
            {user?.name || "Demo Customer"}
          </Typography>
          <Typography variant="caption" color="text.secondary" noWrap>
            {user?.email}
          </Typography>
        </Box>
        <ListItemButton
          onClick={handleLogout}
          sx={{ borderRadius: 2, minWidth: 40, justifyContent: "center", p: 1 }}
        >
          <LogoutIcon fontSize="small" />
        </ListItemButton>
      </Stack>
    </Box>
  );
}

export default function Sidebar({ mobileOpen, onClose }) {
  return (
    <Box component="nav" sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: "block", md: "none" },
          "& .MuiDrawer-paper": { width: DRAWER_WIDTH, boxSizing: "border-box" },
        }}
      >
        <SidebarContent onNavigate={onClose} />
      </Drawer>
      <Drawer
        variant="permanent"
        open
        sx={{
          display: { xs: "none", md: "block" },
          "& .MuiDrawer-paper": {
            width: DRAWER_WIDTH,
            boxSizing: "border-box",
            borderRight: "1px solid #e6e9f2",
          },
        }}
      >
        <SidebarContent />
      </Drawer>
    </Box>
  );
}
