import React from "react";
import { Route, Routes } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import StudentLogin from "./pages/StudentLogin.jsx";
import StudentRegister from "./pages/StudentRegister.jsx";
import TeacherLogin from "./pages/TeacherLogin.jsx";
import StudentHome from "./pages/StudentHome.jsx";
import TeacherHome from "./pages/TeacherHome.jsx";
import StudentLogout from "./pages/StudentLogout.jsx";
import TeacherLogout from "./pages/TeacherLogout.jsx";
import StudentProtectWrapper from "./pages/StudentProtectWrapper.jsx";
import StudentProfile from "./pages/StudentProfile.jsx";
import TeacherProtectWrapper from "./pages/TeacherProtectWrapper.jsx";
import TeacherProfile from "./pages/TeacherProfile.jsx";

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/student-login" element={<StudentLogin />} />
        <Route path="/teacher-login" element={<TeacherLogin />} />
        <Route path="/student-register" element={<StudentRegister />} />
        <Route
          path="/student-home"
          element={
            <StudentProtectWrapper>
              <StudentHome />
            </StudentProtectWrapper>
          }
        />
        <Route
          path="/teacher-home"
          element={
            <TeacherProtectWrapper>
              <TeacherHome />
            </TeacherProtectWrapper>
          }
        />

        <Route
          path="/student-profile"
          element={
            <StudentProtectWrapper>
              <StudentProfile />
            </StudentProtectWrapper>
          }
        />

        <Route
          path="/teacher-profile"
          element={
            <TeacherProtectWrapper>
              <TeacherProfile />
            </TeacherProtectWrapper>
          }
        />

        <Route
          path="/student/logout"
          element={
            <StudentProtectWrapper>
              <StudentLogout />
            </StudentProtectWrapper>
          }
        />
        <Route
          path="/teacher/logout"
          element={
            <TeacherProtectWrapper>
              <TeacherLogout />
            </TeacherProtectWrapper>
          }
        />
      </Routes>
    </div>
  );
}
