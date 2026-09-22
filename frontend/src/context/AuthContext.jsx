import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import authService from "../services/authService";
import { tokenStore } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [booting, setBooting] = useState(true);

  const loadUser = useCallback(async () => {
    const profile = await authService.profile();
    setUser(profile.user);
    return profile;
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      if (!tokenStore.getAccess()) {
        setBooting(false);
        return;
      }
      try {
        const profile = await authService.profile();
        if (active) setUser(profile.user);
      } catch {
        tokenStore.clear();
        if (active) setUser(null);
      } finally {
        if (active) setBooting(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  const login = useCallback(
    async (credentials) => {
      await authService.login(credentials);
      return loadUser();
    },
    [loadUser]
  );

  const register = useCallback((payload) => authService.register(payload), []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({
      user,
      booting,
      login,
      register,
      logout,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === "ADMIN",
      reloadProfile: loadUser,
      setUser,
    }),
    [user, booting, login, register, logout, loadUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return context;
}
