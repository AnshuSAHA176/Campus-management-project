import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function StudentLogout() {
  const navigate = useNavigate();

  useEffect(() => {
    const logout = async () => {
      const refreshToken = localStorage.getItem("refreshToken");

      try {
        if (refreshToken) {
          await axios.post(`${import.meta.env.VITE_BASE_URL}/logout/`, {
            refresh: refreshToken,
          });
        }
      } catch (err) {
        console.log("-----------LOGOUT API ERROR--------", err);
      } finally {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("role");
        navigate("/student-login", { replace: true });
      }
    };

    logout();
  }, [navigate]);

  return (
    <div className="h-screen flex items-center justify-center bg-black">
      <div className="w-10 h-10 border-4 border-[#292929] border-t-[#F0642B] rounded-full animate-spin"></div>
    </div>
  );
}
