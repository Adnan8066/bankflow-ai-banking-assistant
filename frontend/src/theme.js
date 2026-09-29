import { createTheme } from "@mui/material/styles";

/**
 * BankFlow design tokens.
 * One builder serves light and dark mode so every page stays consistent.
 */
const LIGHT = {
  primary: { main: "#1b3a8f", light: "#4361ee", dark: "#122a68", contrastText: "#ffffff" },
  secondary: { main: "#0ea5e9", contrastText: "#ffffff" },
  success: { main: "#16a34a" },
  error: { main: "#e11d48" },
  warning: { main: "#f59e0b" },
  info: { main: "#6366f1" },
  background: { default: "#f4f6fb", paper: "#ffffff" },
  text: { primary: "#111a2e", secondary: "#5a6478" },
  divider: "#e6e9f2",
};

const DARK = {
  primary: { main: "#7b96ff", light: "#a9baff", dark: "#5a76e6", contrastText: "#0b1020" },
  secondary: { main: "#4fc3f7", contrastText: "#0b1020" },
  success: { main: "#4ade80" },
  error: { main: "#fb7185" },
  warning: { main: "#fbbf24" },
  info: { main: "#8b95f8" },
  background: { default: "#0d1220", paper: "#161d2f" },
  text: { primary: "#e9edf9", secondary: "#9fabc4" },
  divider: "#28324a",
};

export function createAppTheme(mode = "light") {
  const palette = mode === "dark" ? DARK : LIGHT;
  const isDark = mode === "dark";

  return createTheme({
    palette: { mode, ...palette },
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
        styleOverrides: { root: { backgroundImage: "none" } },
      },
      MuiCard: {
        defaultProps: { elevation: 0 },
        styleOverrides: {
          root: {
            backgroundImage: "none",
            border: "1px solid",
            borderColor: palette.divider,
            boxShadow: isDark
              ? "none"
              : "0 1px 2px rgba(17, 26, 46, 0.04), 0 8px 24px rgba(17, 26, 46, 0.04)",
          },
        },
      },
      MuiButton: {
        defaultProps: { disableElevation: true },
        styleOverrides: { root: { borderRadius: 10, paddingInline: 18 } },
      },
      MuiChip: { styleOverrides: { root: { fontWeight: 600 } } },
      MuiTableCell: {
        styleOverrides: {
          head: {
            fontWeight: 700,
            color: palette.text.secondary,
            backgroundColor: "var(--bf-surface)",
          },
        },
      },
      MuiAppBar: { defaultProps: { elevation: 0, color: "inherit" } },
    },
  });
}

export default createAppTheme("light");
