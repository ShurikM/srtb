import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// src/components/LoginPage.tsx
import { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Input } from "./ui/input";
export default function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const handleLogin = async () => {
        setError("");
        try {
            const res = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });
            if (!res.ok)
                throw new Error("Login failed");
            const data = await res.json();
            console.log("Token:", data.token);
            // store token or redirect
        }
        catch (e) {
            setError(e.message);
        }
    };
    return (_jsx("div", { className: "min-h-screen flex items-center justify-center bg-gray-100", children: _jsx(Card, { className: "w-full max-w-sm p-6", children: _jsxs(CardContent, { className: "space-y-4", children: [_jsx("h2", { className: "text-xl font-semibold text-center", children: "Login" }), _jsx(Input, { placeholder: "Username", value: username, onChange: (e) => setUsername(e.target.value) }), _jsx(Input, { placeholder: "Password", type: "password", value: password, onChange: (e) => setPassword(e.target.value) }), error && _jsx("p", { className: "text-red-600 text-sm", children: error }), _jsx(Button, { className: "w-full", onClick: handleLogin, children: "Sign In" })] }) }) }));
}
