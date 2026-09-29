import { useEffect, useState } from "react";
import {
  AppBar,
  Avatar,
  Badge,
  Box,
  Button,
  Chip,
  Divider,
  IconButton,
  ListItemIcon,
  Menu,
  MenuItem,
  Stack,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import LogoutIcon from "@mui/icons-material/Logout";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import { useColorMode } from "../context/ColorModeContext.jsx";
import bankingService from "../services/bankingService";
import { initials } from "../utils/formatCurrency.js";

const PAGES = {
  "/dashboard": { title: "Dashboard", subtitle: "Balances, spending and loans at a glance" },
  "/account": { title: "My Account", subtitle: "Simulated account details" },
  "/transactions": { title: "Transactions", subtitle: "Search, filter and export your activity" },
  "/loans": { title: "Loans", subtitle: "Applications, EMIs and outstanding amounts" },
  "/emi-calculator": { title: "EMI Calculator", subtitle: "Plan an instalment before you apply" },
  "/assistant": { title: "AI Assistant", subtitle: "Ask about your own demo data" },
  "/notifications": { title: "Notifications", subtitle: "Simulated banking alerts" },
  "/profile": { title: "Profile", subtitle: "Your details and password" },
  "/admin": { title: "Admin Dashboard", subtitle: "Portfolio overview for bank employees" },
  "/admin/customers": { title: "Customer Management", subtitle: "Search and open a customer 360 view" },
  "/admin/transactions": { title: "Transaction Management", subtitle: "Every simulated transaction" },
  "/admin/loans": { title: "Loan Management", subtitle: "Review and decide on applications" },
  "/admin/analytics": { title: "Analytics", subtitle: "Portfolio trends and totals" },
  "/admin/ai-monitor": { title: "AI Monitoring", subtitle: "What customers ask the assistant" },
};

/** Application header: page context on the left, quick actions and the account menu on the right. */
export default function Navbar({ onMenuClick }) {
  const { user, isAdmin, logout } = useAuth();
  const { mode, toggleColorMode } = useColorMode();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState(null);
  const [unread, setUnread] = useState(0);
  const [scrolled, setScrolled] = useState(false);

  const page = PAGES[location.pathname] || { title: "BankFlow", subtitle: "AI Banking Assistant" };

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const notifications = await bankingService.getNotifications();
        if (!cancelled) setUnread(notifications.filter((item) => !item.is_read).length);
      } catch {
        if (!cancelled) setUnread(0);
      }
    };
    load();
    const timer = setInterval(load, 60000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [location.pathname]);

  const handleLogout = () => {
    setAnchorEl(null);
    logout();
    navigate("/login");
  };

  const closeMenu = () => setAnchorEl(null);

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "rgba(var(--bf-header-rgb), 0.92)",
        backdropFilter: "blur(14px)",
        borderBottom: "1px solid",
        borderColor: "divider",
        boxShadow: scrolled ? "0 10px 30px rgba(11, 25, 60, 0.08)" : "none",
        transition: "box-shadow .25s ease",
      }}
    >
      <Toolbar sx={{ gap: 1.5, minHeight: { xs: 64, md: 72 } }}>
        <IconButton edge="start" onClick={onMenuClick} sx={{ display: { md: "none" } }} aria-label="Open navigation">
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1, minWidth: 0 }}>
          <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.08em", textTransform: "uppercase", fontSize: 10 }}>
            BankFlow
          </Typography>
          <Typography variant="h6" noWrap sx={{ fontSize: { xs: 16, md: 19 }, lineHeight: 1.2 }}>
            {page.title}
          </Typography>
          <Typography
            variant="caption"
            color="text.secondary"
            noWrap
            sx={{ display: { xs: "none", sm: "block" } }}
          >
            {page.subtitle}
          </Typography>
        </Box>

        <Button
          variant="outlined"
          startIcon={<SmartToyIcon fontSize="small" />}
          onClick={() => navigate("/assistant")}
          sx={{ display: { xs: "none", md: "inline-flex" }, borderRadius: 999, px: 2 }}
        >
          Ask AI
        </Button>

        <Tooltip title={mode === "dark" ? "Switch to light mode" : "Switch to dark mode"}>
          <IconButton onClick={toggleColorMode} aria-label="Toggle dark mode">
            {mode === "dark" ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Tooltip>

        <Tooltip title="Notifications">
          <IconButton onClick={() => navigate("/notifications")} aria-label="Notifications">
            <Badge color="error" badgeContent={unread} max={9}>
              <NotificationsNoneIcon />
            </Badge>
          </IconButton>
        </Tooltip>

        <Divider orientation="vertical" flexItem sx={{ my: 2, display: { xs: "none", sm: "block" } }} />

        <Button
          onClick={(event) => setAnchorEl(event.currentTarget)}
          endIcon={<KeyboardArrowDownIcon fontSize="small" />}
          sx={{ px: 1, borderRadius: 2, minWidth: 0, color: "text.primary" }}
        >
          <Stack direction="row" spacing={1} alignItems="center">
            <Avatar sx={{ width: 34, height: 34, background: "linear-gradient(135deg, #16357f 0%, #3f74ff 100%)", fontSize: 13 }}>
              {initials(user?.name || "BF")}
            </Avatar>
            <Box sx={{ display: { xs: "none", md: "block" }, textAlign: "left" }}>
              <Typography variant="subtitle2" lineHeight={1.2}>
                {user?.name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {isAdmin ? "Bank Employee" : "Customer"}
              </Typography>
            </Box>
          </Stack>
        </Button>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={closeMenu}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
          slotProps={{ paper: { sx: { mt: 1, minWidth: 260, borderRadius: 3, border: "1px solid", borderColor: "divider" } } }}
        >
          <Box sx={{ px: 2, py: 1.5 }}>
            <Typography variant="subtitle2">{user?.name}</Typography>
            <Typography variant="caption" color="text.secondary">
              {user?.email}
            </Typography>
            <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
              <Chip size="small" color="primary" label={isAdmin ? "BANK EMPLOYEE" : "CUSTOMER"} />
              <Chip size="small" variant="outlined" label="Demo data" />
            </Stack>
          </Box>
          <Divider />
          <MenuItem
            onClick={() => {
              closeMenu();
              navigate("/profile");
            }}
          >
            <ListItemIcon>
              <PersonOutlineIcon fontSize="small" />
            </ListItemIcon>
            My profile
          </MenuItem>
          {isAdmin && (
            <MenuItem
              onClick={() => {
                closeMenu();
                navigate("/admin");
              }}
            >
              <ListItemIcon>
                <AdminPanelSettingsOutlinedIcon fontSize="small" />
              </ListItemIcon>
              Bank employee area
            </MenuItem>
          )}
          <MenuItem
            onClick={() => {
              closeMenu();
              toggleColorMode();
            }}
          >
            <ListItemIcon>
              {mode === "dark" ? <Brightness7Icon fontSize="small" /> : <Brightness4Icon fontSize="small" />}
            </ListItemIcon>
            {mode === "dark" ? "Light mode" : "Dark mode"}
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleLogout} sx={{ color: "error.main" }}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" sx={{ color: "error.main" }} />
            </ListItemIcon>
            Sign out
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
