import { useEffect, useState } from "react";
import {
  AppBar,
  Box,
  Button,
  Container,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";
import BrandLogo from "./BrandLogo.jsx";

export const PUBLIC_NAV = [
  { label: "Home", href: "#home" },
  { label: "Features", href: "#features" },
  { label: "AI Assistant", href: "#assistant" },
  { label: "Security", href: "#security" },
  { label: "About", href: "#about" },
];

/** Sticky public header used on the landing page: brand, section links and the two calls to action. */
export default function PublicHeader() {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin } = useAuth();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [active, setActive] = useState("#home");

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const sections = PUBLIC_NAV.map((link) => document.querySelector(link.href)).filter(Boolean);
    if (!sections.length) return undefined;
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting);
        if (visible.length) setActive(`#${visible[0].target.id}`);
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
    return () => observer.disconnect();
  }, []);

  const openApp = () => navigate(isAuthenticated ? (isAdmin ? "/admin" : "/dashboard") : "/login");
  const go = (href) => {
    setMenuOpen(false);
    if (href.startsWith("#")) {
      document.querySelector(href)?.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      navigate(href);
    }
  };

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "rgba(var(--bf-header-rgb), 0.86)",
        backdropFilter: "blur(14px)",
        borderBottom: "1px solid",
        borderColor: "divider",
        boxShadow: scrolled ? "0 10px 30px rgba(11, 25, 60, 0.08)" : "none",
        transition: "box-shadow .25s ease",
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ minHeight: { xs: 64, md: 72 }, gap: 2 }}>
          <Box sx={{ flexGrow: { xs: 1, md: 0 } }}>
            <BrandLogo onClick={() => go("#home")} />
          </Box>

          <Stack
            direction="row"
            spacing={0.5}
            sx={{ display: { xs: "none", md: "flex" }, flexGrow: 1, justifyContent: "center" }}
          >
            {PUBLIC_NAV.map((link) => (
              <Button
                key={link.label}
                onClick={() => go(link.href)}
                sx={{
                  color: active === link.href ? "primary.main" : "text.secondary",
                  fontWeight: 600,
                  px: 1.5,
                  position: "relative",
                  "&:hover": { color: "primary.main", backgroundColor: "transparent" },
                  "&::after": {
                    content: '""',
                    position: "absolute",
                    left: 12,
                    right: 12,
                    bottom: 6,
                    height: 2,
                    borderRadius: 2,
                    backgroundColor: "primary.main",
                    transform: active === link.href ? "scaleX(1)" : "scaleX(0)",
                    transition: "transform .2s ease",
                  },
                }}
              >
                {link.label}
              </Button>
            ))}
          </Stack>

          <Stack direction="row" spacing={1.5} alignItems="center" sx={{ ml: "auto" }}>
            <Button
              onClick={() => navigate("/login")}
              sx={{ display: { xs: "none", sm: "inline-flex" }, color: "text.primary" }}
            >
              Sign in
            </Button>
            <Button
              variant="contained"
              endIcon={<ArrowForwardIcon fontSize="small" />}
              onClick={isAuthenticated ? openApp : () => navigate("/register")}
              sx={{ display: { xs: "none", sm: "inline-flex" }, boxShadow: "0 8px 20px rgba(19,45,110,.22)" }}
            >
              {isAuthenticated ? "Open app" : "Get started"}
            </Button>
            <IconButton
              onClick={() => setMenuOpen(true)}
              sx={{ display: { md: "none" } }}
              aria-label="Open menu"
            >
              <MenuIcon />
            </IconButton>
          </Stack>
        </Toolbar>
      </Container>

      <Drawer anchor="right" open={menuOpen} onClose={() => setMenuOpen(false)}>
        <Box sx={{ width: 288, p: 2 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
            <BrandLogo size={34} subtitle={null} />
            <IconButton onClick={() => setMenuOpen(false)} aria-label="Close menu">
              <CloseIcon />
            </IconButton>
          </Stack>
          <Divider sx={{ my: 1.5 }} />
          <List disablePadding>
            {PUBLIC_NAV.map((link) => (
              <ListItemButton key={link.label} onClick={() => go(link.href)} sx={{ borderRadius: 2 }}>
                <ListItemText primary={link.label} />
              </ListItemButton>
            ))}
          </List>
          <Divider sx={{ my: 1.5 }} />
          <Stack spacing={1.5}>
            <Button fullWidth variant="outlined" onClick={() => navigate("/login")}>
              Sign in
            </Button>
            <Button
              fullWidth
              variant="contained"
              onClick={isAuthenticated ? openApp : () => navigate("/register")}
            >
              {isAuthenticated ? "Open app" : "Get started"}
            </Button>
            <Typography variant="caption" color="text.secondary" sx={{ textAlign: "center" }}>
              Demo application with fictional data only.
            </Typography>
          </Stack>
        </Box>
      </Drawer>
    </AppBar>
  );
}
