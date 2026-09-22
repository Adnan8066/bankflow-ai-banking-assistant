import { createTheme } from "@mui/material/styles";

/**
 * BankFlow design tokens.
 * A light, professional banking palette: deep navy + trustworthy blue + teal accent.
 */
const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#1b3a8f", light: "#4361ee", dark: "#122a68", contrastText: "#ffffff" },
    secondary: { main: "#0ea5e9", contrastText: "#ffffff" },
    success: { main: "#16a34a" },
    error: { main: "#e11d48" },
    warning: { main: "#f59e0b" },
    info: { main: "#6366f1" },
    background: { default: "#f4f6fb", paper: "#ffffff" },
    text: { primary: "#111a2e", secondary: "#5a6478" },
    divider: "#e6e9f2",
  },
  shape: { borderRadius: 12 },
  typography: {
    fontFamily: '"Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    h1: { fontWeight: 800, letterSpacing: "-0.02em" },
    h2: { fontWeight: 800, letterSpacing: "-0.02em" },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 700 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { textTransform: "none", fontWeight: 600 },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: { backgroundImage: "none" },
      },
    },
    MuiCard: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          border: "1px solid #e6e9f2",
          boxShadow: "0 1px 2px rgba(17, 26, 46, 0.04), 0 8px 24px rgba(17, 26, 46, 0.04)",
        },
      },
    },
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { borderRadius: 10, paddingInline: 18 },
        containedPrimary: { "&:hover": { backgroundColor: "#122a68" } },
      },
    },
    MuiChip: { styleOverrides: { root: { fontWeight: 600 } } },
    MuiTableCell: {
      styleOverrides: {
        head: { fontWeight: 700, color: "#5a6478", backgroundColor: "#f8f9fd" },
      },
    },
    MuiAppBar: {
      defaultProps: { elevation: 0, color: "inherit" },
    },
  },
});

export default theme;
