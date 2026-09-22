import { useEffect, useState } from "react";
import {
  AppBar,
  Avatar,
  Badge,
  Box,
  Chip,
  Divider,
  IconButton,
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
import { useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import bankingService from "../services/bankingService";
import { initials } from "../utils/formatCurrency.js";

const TITLES = {
  "/dashboard": "Dashboard",
  "/account": "My Account",
  "/transactions": "Transactions",
  "/loans": "Loans",
  "/emi-calculator": "EMI Calculator",
  "/assistant": "AI Banking Assistant",
  "/notifications": "Notifications",
  "/profile": "Profile",
  "/admin": "Admin Dashboard",
  "/admin/customers": "Customer Management",
  "/admin/transactions": "Transaction Management",
  "/admin/loans": "Loan Management",
  "/admin/analytics": "Analytics",
  "/admin/ai-monitor": "AI Assistant Monitoring",
};

export default function Navbar({ onMenuClick }) {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState(null);
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const notifications = await bankingService.getNotifications();
        if (!cancelled) {
          setUnread(notifications.filter((item) => !item.is_read).length);
        }
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

  const title = TITLES[location.pathname] || "BankFlow";

  const handleLogout = () => {
    setAnchorEl(null);
    logout();
    navigate("/login");
  };

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "rgba(255,255,255,.92)",
        backdropFilter: "blur(8px)",
        borderBottom: "1px solid #e6e9f2",
      }}
    >
      <Toolbar sx={{ gap: 1.5 }}>
        <IconButton edge="start" onClick={onMenuClick} sx={{ display: { md: "none" } }}>
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" sx={{ flexGrow: 1, fontSize: { xs: 16, md: 18 } }}>
          {title}
        </Typography>

        <Tooltip title="Ask BankFlow AI">
          <IconButton onClick={() => navigate("/assistant")} sx={{ display: { xs: "none", sm: "inline-flex" } }}>
            <SmartToyIcon />
          </IconButton>
        </Tooltip>

        <Tooltip title="Notifications">
          <IconButton onClick={() => navigate("/notifications")}>
            <Badge color="error" badgeContent={unread} max={9}>
              <NotificationsNoneIcon />
            </Badge>
          </IconButton>
        </Tooltip>

        <Divider orientation="vertical" flexItem sx={{ my: 1.5 }} />

        <Stack
          direction="row"
          spacing={1}
          alignItems="center"
          onClick={(event) => setAnchorEl(event.currentTarget)}
          sx={{ cursor: "pointer", borderRadius: 2, px: 0.5, py: 0.5 }}
        >
          <Avatar sx={{ width: 34, height: 34, bgcolor: "primary.main", fontSize: 13 }}>
            {initials(user?.name || "BF")}
          </Avatar>
          <Box sx={{ display: { xs: "none", md: "block" } }}>
            <Typography variant="subtitle2" lineHeight={1.2}>
              {user?.name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {isAdmin ? "Bank Employee" : "Customer"}
            </Typography>
          </Box>
        </Stack>

        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={() => setAnchorEl(null)}>
          <MenuItem disabled sx={{ opacity: "1 !important" }}>
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2">{user?.email}</Typography>
              <Chip size="small" label={isAdmin ? "ADMIN" : "CUSTOMER"} color="primary" />
            </Stack>
          </MenuItem>
          <Divider />
          <MenuItem
            onClick={() => {
              setAnchorEl(null);
              navigate("/profile");
            }}
          >
            <PersonOutlineIcon fontSize="small" style={{ marginRight: 10 }} /> My profile
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <LogoutIcon fontSize="small" style={{ marginRight: 10 }} /> Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
