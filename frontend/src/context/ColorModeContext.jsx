import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";

import { createAppTheme } from "../theme.js";

const STORAGE_KEY = "bankflow_color_mode";

const ColorModeContext = createContext({ mode: "light", toggleColorMode: () => {} });

/**
 * Holds the light or dark choice, remembers it in localStorage, and mirrors it onto
 * the <html> element so the CSS variables in index.css follow the same mode.
 */
export function ColorModeProvider({ children }) {
  const [mode, setMode] = useState(() => localStorage.getItem(STORAGE_KEY) || "light");

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, mode);
    document.documentElement.setAttribute("data-theme", mode);
    document.documentElement.style.colorScheme = mode;
  }, [mode]);

  const theme = useMemo(() => createAppTheme(mode), [mode]);
  const value = useMemo(
    () => ({
      mode,
      toggleColorMode: () => setMode((current) => (current === "light" ? "dark" : "light")),
    }),
    [mode]
  );

  return (
    <ColorModeContext.Provider value={value}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export function useColorMode() {
  return useContext(ColorModeContext);
}
