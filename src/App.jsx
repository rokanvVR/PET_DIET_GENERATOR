import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

function App() {
  const [page, setPage] = useState("login");
  const token = localStorage.getItem("token");

  if (token) {
    return <Dashboard setPage={setPage} />;
  }

  return (
    <>
      {page === "login" && <Login setPage={setPage} />}
      {page === "register" && <Register setPage={setPage} />}
    </>
  );
}

export default App;