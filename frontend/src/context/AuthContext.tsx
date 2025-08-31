// src/context/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import API from "../api/axios"; // centralized axios instance

type User = {
  username: string;
};

type AuthContextType = {
  access: string | null;
  refresh: string | null;
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  // initialize from localStorage if available
  const [access, setAccess] = useState<string | null>(localStorage.getItem("access"));
  const [refresh, setRefresh] = useState<string | null>(localStorage.getItem("refresh"));
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem("user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  // 🔑 login function
  const login = async (username: string, password: string) => {
    const res = await API.post("token/", { username, password });

    setAccess(res.data.access);
    setRefresh(res.data.refresh);
    const newUser = { username };
    setUser(newUser);

    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
    localStorage.setItem("user", JSON.stringify(newUser));
  };

  // 📝 register function
  const register = async (username: string, email: string, password: string) => {
    await API.post("register/", { username, email, password });
    // auto-login after successful register
    await login(username, password);
  };

  // 🚪 logout function
  const logout = () => {
    setAccess(null);
    setRefresh(null);
    setUser(null);
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
  };

  // keep tokens & user synced with localStorage
  useEffect(() => {
    if (access) localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
    if (user) localStorage.setItem("user", JSON.stringify(user));
  }, [access, refresh, user]);

  return (
    <AuthContext.Provider value={{ access, refresh, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
