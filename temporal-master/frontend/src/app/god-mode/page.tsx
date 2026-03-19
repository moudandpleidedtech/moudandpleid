"use client";

import { useState } from "react";
import AdminDashboard from "@/components/Admin/AdminDashboard";

export default function GodModePage() {
  const envSecret = process.env.NEXT_PUBLIC_ADMIN_SECRET ?? "";
  const [input, setInput] = useState("");
  const [secret, setSecret] = useState(envSecret);
  const [error, setError] = useState("");

  // If the env var provides the secret, skip the gate entirely
  if (secret) {
    return <AdminDashboard adminSecret={secret} />;
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) {
      setError("Introduce el código de acceso.");
      return;
    }
    setError("");
    setSecret(input.trim());
  }

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#0A0A0F",
        fontFamily: "'Courier New', monospace",
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          border: "1px solid #BD00FF",
          borderRadius: 8,
          padding: "2.5rem 3rem",
          display: "flex",
          flexDirection: "column",
          gap: "1.25rem",
          minWidth: 340,
          boxShadow: "0 0 32px #BD00FF44",
        }}
      >
        <h1
          style={{
            color: "#BD00FF",
            fontSize: "1.4rem",
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            margin: 0,
            textAlign: "center",
          }}
        >
          ⚡ GOD MODE
        </h1>
        <p style={{ color: "#888", fontSize: "0.8rem", margin: 0, textAlign: "center" }}>
          Acceso restringido — Introduce el código de seguridad
        </p>

        <input
          type="password"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="X-Admin-Secret"
          autoFocus
          style={{
            background: "#111",
            border: "1px solid #333",
            borderRadius: 4,
            color: "#E0E0E0",
            fontFamily: "inherit",
            fontSize: "1rem",
            padding: "0.6rem 0.9rem",
            outline: "none",
          }}
        />

        {error && (
          <p style={{ color: "#FF4444", fontSize: "0.8rem", margin: 0 }}>{error}</p>
        )}

        <button
          type="submit"
          style={{
            background: "#BD00FF",
            border: "none",
            borderRadius: 4,
            color: "#fff",
            cursor: "pointer",
            fontFamily: "inherit",
            fontSize: "0.95rem",
            fontWeight: 700,
            letterSpacing: "0.1em",
            padding: "0.65rem",
            textTransform: "uppercase",
          }}
        >
          Acceder
        </button>
      </form>
    </main>
  );
}
