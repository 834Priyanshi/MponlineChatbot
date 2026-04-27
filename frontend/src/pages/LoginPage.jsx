import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../services/api";

const initialRegisterState = {
  email: "",
  password: "",
};

function LoginPage() {
  const navigate = useNavigate();
  const { setSession } = useAuth();
  const [mode, setMode] = useState("login");
  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [registerData, setRegisterData] = useState(initialRegisterState);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const redirectAfterAuth = (user) => {
    navigate(user.role === "admin" || user.role === "expert" ? "/dashboard" : "/chat");
  };

  const resetMessages = () => {
    setNotice("");
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    resetMessages();
    setLoading(true);

    try {
      if (mode === "login") {
        const { data } = await api.post("/auth/login", loginData);
        setSession(data.access_token, data.user);
        redirectAfterAuth(data.user);
      } else {
        const { data } = await api.post("/auth/register", registerData);
        setSession(data.access_token, data.user);
        redirectAfterAuth(data.user);
      }
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div>
          <p className="eyebrow">AI + RAG</p>
          <h2>MPOnline FAQ Chatbot</h2>
          <p className="muted">
            Sign in with your email and password. New users can register with just email and password.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="form-grid">
          {mode === "register" ? (
            <>
              <input
                placeholder="Email"
                type="email"
                value={registerData.email}
                onChange={(event) =>
                  setRegisterData((current) => ({ ...current, email: event.target.value }))
                }
                required
              />
              <input
                placeholder="Password"
                type="password"
                value={registerData.password}
                onChange={(event) =>
                  setRegisterData((current) => ({ ...current, password: event.target.value }))
                }
                required
              />
            </>
          ) : (
            <>
              <input
                placeholder="Email"
                type="email"
                value={loginData.email}
                onChange={(event) =>
                  setLoginData((current) => ({ ...current, email: event.target.value }))
                }
                required
              />
              <input
                placeholder="Password"
                type="password"
                value={loginData.password}
                onChange={(event) =>
                  setLoginData((current) => ({ ...current, password: event.target.value }))
                }
                required
              />
            </>
          )}

          {notice && <p className="success-text">{notice}</p>}
          {error && <p className="error-text">{error}</p>}

          <button className="primary-button" disabled={loading} type="submit">
            {loading
              ? "Please wait..."
              : mode === "login"
              ? "Login"
              : "Register"}
          </button>
        </form>

        <div className="auth-switch-row">
          {mode === "register" ? (
            <>
              <span>Already have an account?</span>
              <button
                onClick={() => {
                  setMode("login");
                  resetMessages();
                }}
                type="button"
              >
                Login
              </button>
            </>
          ) : (
            <>
              <span>Don't have an account?</span>
              <button
                onClick={() => {
                  setMode("register");
                  resetMessages();
                }}
                type="button"
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default LoginPage;