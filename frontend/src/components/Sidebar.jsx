import {
  Avatar,
  Box,
  Chip,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Tooltip,
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
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import LogoutIcon from "@mui/icons-material/Logout";
import GitHubIcon from "@mui/icons-material/GitHub";
import { NavLink, useNavigate } from "react-router-dom";

import { BRAND } from "../branding.js";
import { useAuth } from "../context/AuthContext.jsx";
import { initials } from "../utils/formatCurrency.js";
import BrandLogo from "./BrandLogo.jsx";

export const DRAWER_WIDTH = 264;

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
  { to: "/admin", label: "Admin Dashboard", icon: <DashboardIcon />, end: true },
  { to: "/admin/customers", label: "Customers", icon: <GroupIcon /> },
  { to: "/admin/transactions", label: "Transactions", icon: <ReceiptLongIcon /> },
  { to: "/admin/loans", label: "Loan Management", icon: <RequestQuoteIcon /> },
  { to: "/admin/analytics", label: "Analytics", icon: <InsightsIcon /> },
  { to: "/admin/ai-monitor", label: "AI Monitoring", icon: <MonitorHeartIcon /> },
  { to: "/admin/users", label: "User Management", icon: <ManageAccountsIcon /> },
];

const itemSx = {
  borderRadius: 2,
  mb: 0.5,
  pl: 1.75,
  color: "text.secondary",
  position: "relative",
  "& .MuiListItemIcon-root": { color: "text.secondary", minWidth: 42 },
  "&::before": {
    content: '""',
    position: "absolute",
    left: 0,
    top: 8,
    bottom: 8,
    width: 3,
    borderRadius: 3,
    backgroundColor: "primary.main",
    opacity: 0,
    transition: "opacity .18s ease",
  },
  "&:hover": { backgroundColor: "var(--bf-tint)" },
  "&.active": {
    backgroundColor: "var(--bf-tint)",
    color: "primary.main",
    "&::before": { opacity: 1 },
    "& .MuiListItemIcon-root": { color: "primary.main" },
    "& .MuiListItemText-primary": { fontWeight: 700 },
  },
};

function SectionLabel({ children }) {
  return (
    <Typography
      variant="overline"
      sx={{ px: 2, mt: 2, mb: 0.5, display: "block", color: "text.secondary", fontWeight: 700, fontSize: 10.5, letterSpacing: "0.09em" }}
    >
      {children}
    </Typography>
  );
}

function SidebarContent({ onNavigate }) {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <Toolbar sx={{ px: 2, minHeight: { xs: 64, md: 72 } }}>
        <BrandLogo size={36} onClick={() => navigate("/dashboard")} />
      </Toolbar>
      <Divider />

      <List sx={{ px: 1.25, py: 1.5, flexGrow: 1, overflowY: "auto" }}>
        <SectionLabel>Banking</SectionLabel>
        {CUSTOMER_LINKS.map((link) => (
          <ListItemButton key={link.to} component={NavLink} to={link.to} onClick={onNavigate} sx={itemSx}>
            <ListItemIcon>{link.icon}</ListItemIcon>
            <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
          </ListItemButton>
        ))}

        {isAdmin && (
          <>
            <SectionLabel>Bank employee</SectionLabel>
            {ADMIN_LINKS.map((link) => (
              <ListItemButton
                key={link.to}
                component={NavLink}
                to={link.to}
                end={link.end}
                onClick={onNavigate}
                sx={itemSx}
              >
                <ListItemIcon>{link.icon}</ListItemIcon>
                <ListItemText primaryTypographyProps={{ fontSize: 14 }} primary={link.label} />
              </ListItemButton>
            ))}
          </>
        )}
      </List>

      <Box sx={{ px: 1.5, pb: 1 }}>
        <Chip
          size="small"
          variant="outlined"
          label="Demo data only"
          sx={{ width: "100%", justifyContent: "flex-start" }}
        />
      </Box>

      <Divider />
      <Stack direction="row" spacing={1.25} alignItems="center" sx={{ p: 1.75 }}>
        <Avatar sx={{ width: 38, height: 38, fontSize: 14, background: BRAND.gradient }}>
          {initials(user?.name || "BF")}
        </Avatar>
        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
          <Typography variant="subtitle2" noWrap>
            {user?.name || "Demo Customer"}
          </Typography>
          <Typography variant="caption" color="text.secondary" noWrap sx={{ display: "block" }}>
            {user?.email}
          </Typography>
        </Box>
        <Tooltip title="Source code">
          <ListItemButton
            component="a"
            href={BRAND.github}
            target="_blank"
            rel="noreferrer"
            sx={{ borderRadius: 2, minWidth: 36, justifyContent: "center", p: 0.75 }}
          >
            <GitHubIcon fontSize="small" />
          </ListItemButton>
        </Tooltip>
        <Tooltip title="Sign out">
          <ListItemButton onClick={handleLogout} sx={{ borderRadius: 2, minWidth: 36, justifyContent: "center", p: 0.75 }}>
            <LogoutIcon fontSize="small" />
          </ListItemButton>
        </Tooltip>
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
            borderRight: "1px solid",
            borderColor: "divider",
            backgroundColor: "background.paper",
          },
        }}
      >
        <SidebarContent />
      </Drawer>
    </Box>
  );
}
