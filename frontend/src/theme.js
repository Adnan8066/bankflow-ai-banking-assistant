import { createTheme } from "@mui/material/styles";

/**
 * BankFlow design tokens.
 * A deep navy brand colour with a teal accent, tuned separately for light and dark mode.
 */
const LIGHT = {
  primary: { main: "#16357f", light: "#3f74ff", dark: "#0d2258", contrastText: "#ffffff" },
  secondary: { main: "#0f9d8f", contrastText: "#ffffff" },
  // Slightly darker than a typical "success" green so white text on a filled chip stays readable.
  success: { main: "#15803d" },
  error: { main: "#e11d48" },
  warning: { main: "#b45309" },
  info: { main: "#4f46e5" },
  background: { default: "#f5f7fc", paper: "#ffffff" },
  text: { primary: "#0e1729", secondary: "#5a6784" },
  divider: "#e6eaf3",
  action: {
    disabled: "#58627a",
    disabledBackground: "#eaedf5",
  },
};

const DARK = {
  primary: { main: "#7f9dff", light: "#a8bcff", dark: "#5677e8", contrastText: "#071022" },
  secondary: { main: "#2dd4bf", contrastText: "#04211d" },
  success: { main: "#4ade80" },
  error: { main: "#fb7185" },
  warning: { main: "#fbbf24" },
  info: { main: "#a5b4fc" },
  background: { default: "#080d19", paper: "#111a2c" },
  text: { primary: "#e9eefb", secondary: "#98a5c0" },
  divider: "#232e46",
  action: {
    disabled: "#9aa4bb",
    disabledBackground: "#1c2436",
  },
};

export function createAppTheme(mode = "light") {
  const palette = mode === "dark" ? DARK : LIGHT;
  const isDark = mode === "dark";

  return createTheme({
    palette: { mode, ...palette },
    shape: { borderRadius: 14 },
    typography: {
      fontFamily: '"Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
      h1: { fontWeight: 800, letterSpacing: "-0.025em" },
      h2: { fontWeight: 800, letterSpacing: "-0.025em" },
      h3: { fontWeight: 700, letterSpacing: "-0.02em" },
      h4: { fontWeight: 700, letterSpacing: "-0.015em" },
      h5: { fontWeight: 700, letterSpacing: "-0.01em" },
      h6: { fontWeight: 700 },
      subtitle1: { fontWeight: 600 },
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
            borderRadius: 16,
            border: "1px solid",
            borderColor: palette.divider,
            boxShadow: isDark
              ? "none"
              : "0 1px 2px rgba(16, 28, 58, 0.04), 0 12px 28px rgba(16, 28, 58, 0.05)",
          },
        },
      },
      MuiButton: {
        defaultProps: { disableElevation: true },
        styleOverrides: {
          root: { borderRadius: 10, paddingInline: 18, fontWeight: 600 },
          containedPrimary: {
            background: isDark
              ? undefined
              : "linear-gradient(135deg, #16357f 0%, #2b53ba 100%)",
          },
        },
      },
      MuiChip: { styleOverrides: { root: { fontWeight: 600 } } },
      MuiAvatar: {
        // Every avatar in this app sits on the brand gradient, so the initials are always white.
        styleOverrides: { root: { color: "#ffffff" } },
      },
      MuiTableCell: {
        styleOverrides: {
          head: {
            fontWeight: 700,
            color: palette.text.secondary,
            backgroundColor: "var(--bf-surface)",
            borderBottomColor: palette.divider,
            letterSpacing: "0.02em",
          },
          body: { borderBottomColor: palette.divider },
        },
      },
      MuiAppBar: { defaultProps: { elevation: 0, color: "inherit" } },
      MuiDrawer: {
        styleOverrides: { paper: { backgroundImage: "none" } },
      },
      MuiTooltip: {
        styleOverrides: {
          tooltip: { backgroundColor: isDark ? "#1c2740" : "#0e1729", fontSize: 12, borderRadius: 8 },
        },
      },
    },
  });
}

export default createAppTheme("light");
