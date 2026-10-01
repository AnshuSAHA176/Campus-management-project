import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { teacherDataContext } from "../context/TeacherContext";
import axios from "axios";

export default function TeacherProtectWrapper({ children }) {
  const navigate = useNavigate();

  const { teacher, setTeacher } = useContext(teacherDataContext);

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const verifyTeacher = async () => {
      const accessToken = localStorage.getItem("accessToken");
      const refreshToken = localStorage.getItem("refreshToken");

      if (!accessToken || !refreshToken) {
        navigate("/teacher-login", { replace: true });
        return;
      }

      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BASE_URL}/teacher_profile/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        );

        // Access token is valid
        if (response.status === 200) {
          setTeacher(response.data);
          setIsLoading(false);
        }
      } catch (err) {
        // Access token expired
        if (err.response?.status === 401) {
          try {
            const refreshResponse = await axios.post(
              `${import.meta.env.VITE_BASE_URL}/refresh/`,
              {
                refresh: refreshToken,
              },
            );

            const newAccessToken = refreshResponse.data.access;

            localStorage.setItem("accessToken", newAccessToken);

            // Retry profile request with new access token
            const profileResponse = await axios.get(
              `${import.meta.env.VITE_BASE_URL}/teacher_profile/`,
              {
                headers: {
                  Authorization: `Bearer ${newAccessToken}`,
                },
              },
            );

            if (profileResponse.status === 200) {
              setTeacher(profileResponse.data);
              setIsLoading(false);
            }
          } catch (refreshError) {
            console.log("Refresh token failed:", refreshError);

            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");

            navigate("/teacher-login", { replace: true });
          }
        } else {
          console.log(err);

          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");

          navigate("/teacher-login", { replace: true });
        }
      }
    };

    verifyTeacher();
  }, [navigate, setTeacher]);

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-black">
        <div className="w-10 h-10 border-4 border-[#292929] border-t-[#F0642B] rounded-full animate-spin"></div>
      </div>
    );
  }

  return <>{children}</>;
}
