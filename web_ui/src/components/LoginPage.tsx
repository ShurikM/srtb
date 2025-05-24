import { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Input } from "./ui/input";
import { login } from "../api";

export default function LoginPage({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("password");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");
    try {
      const ok = await login(username, password);
      if (!ok) throw new Error("Login failed");
      onLogin();
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-sm p-6">
        <CardContent className="space-y-4">
          <h2 className="text-xl font-semibold text-center">Login</h2>
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {error && <p className="text-red-600 text-sm">{error}</p>}
          <Button className="w-full" onClick={handleLogin}>
            Sign In
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
